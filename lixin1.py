from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

chrome87 = {
    "Host": "mcenter.lixin.edu.cn",
    "Connection": "keep-alive",
    "Content-Length": "65",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.141 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://mcenter.lixin.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://mcenter.lixin.edu.cn/index_sso.jsp",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}
health_dict = {0: "健康", 1: "疑似", 2: "确诊"}
school_id = {
    "信息管理学院": "615",
    "统计与数学学院": "616",
    "财税与公共管理学院": "605",
    "未命名学院": "000",
}
sid_url = "https://mcenter.lixin.edu.cn/r/jd"
chrome87_plus_instance = {
    "Host": "mcenter.lixin.edu.cn",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.141 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "iframe",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}


class DailyReport:
    def __init__(self, username: str, at_school: bool, location: str, ad_code: str, covid_patient: int,
                 teacher_id: str, school_name: str, class_name: str, name: str):
        """
        Initialize a web scrapy for SLU daily report.
        :param username: [string] student ID
        :param at_school: [true/false] if you're at school
        :param location: [string] options, "在沪"(in Shanghai), "在中高风险地区"(in middle- & high-risk locations),
            "在其它地区"(in other locations)
        :param ad_code: [string] the first 4 digits of China administrative division code (different from postal code).
            Quick check: Shanghai "3101", your hometown as the first 4 digits of citizenship ID.
            For more details: http://preview.www.mca.gov.cn/article/sj/xzqh/2020/2020/202101041104.html
        :param covid_patient: [int] options, 0 (health), 1 (suspected covid patient), 2 (covid patient).
        :param teacher_id: [str] ID of your instructor in SLU
            Notes: You can check it in WeCom contact.
        :param school_name: [str] name of your school
            Supported: 统计与数学学院, 信息管理学院, 财税与公共管理学院
        :param class_name: [str] name of your class
        :param name: [str] your name
        """
        self.username = username
        self.at_school = at_school
        self.location = location
        self.postal_code = ad_code
        self.health = health_dict[covid_patient]
        self.teacher_id = teacher_id
        self.school_name = school_id[school_name]
        self.class_name = class_name
        self.name = name

        self.sess = requests.Session()
        self.sess.trust_env = False

        self.user_info = {
            "userid": username,
            "cmd": "CLIENT_USER_LOGIN",
            "deviceType": "pc",
            "sid": "",
            "lang": "cn",
        }

    def run(self):
        json_response = self.sess.post(sid_url, data=self.user_info, headers=chrome87, verify=False)
        sid = json_response.json()['data']['sid']
        process_instance_url = f"https://mcenter.lixin.edu.cn/r/w?sid={sid}&cmd" \
                               "=CLIENT_BPM_WORKLIST_PROCESSINST_CREATE&processDefId" \
                               "=obj_533a8e5d84f84749907d0c350d9ce97c&processGroupId" \
                               "=obj_3d1d30b4f1ba4960bc1a6a4980af42c8&title=%25E6%25AF%258F%25E6%2597%25A5" \
                               "%25E4%25B8%2580%25E6%258A%25A5"
        chrome87_plus_instance["Referer"] = f"https://mcenter.lixin.edu.cn/r/w?sid={sid}&cmd=CLIENT_DW_PORTAL&appId" \
                                            "=com.awspaas.user.apps.dailyreport&processGroupId" \
                                            "=obj_3d1d30b4f1ba4960bc1a6a4980af42c8&dwViewId" \
                                            "=obj_b483ade9a3e141fc911a8ccb0de9c29b"
        process_instance_response = self.sess.get(process_instance_url, headers=chrome87_plus_instance)
        pir_bs_tree = BeautifulSoup(process_instance_response.text)
        process_inst_id = pir_bs_tree.find("input", id="processInstId", type="hidden").attrs['value']
        form_def_id = pir_bs_tree.find("input", id="formDefId", type="hidden").attrs['value']
        process_def_id = pir_bs_tree.find("input", id="processDefId", type="hidden").attrs['value']

        form_data = {
            "ZHBNOW": "0", "ZHB": "0", "MQJC": "0", "KZZD": None, "SWBZ": "", "XWBZ": "", "BZ": "",
            "ISSAME": "", "SORTNUM": "29", "XW_TJTW": "", "XW_XWTW": None, "SW_TJTW": "", "SWTW": None,
            "SFZX": None, "SFCS": None, "SF": self.postal_code, "ZGFXDQSF": None, "DQJZS": None,
            "STZK": self.health, "BSRQ": date.today().__str__(), "ROLE": "学生", "FDY": self.teacher_id,
            "BJ": self.class_name, "BM": self.school_name, "XM": self.name, "GH": self.username, "ISREPORT": "0",
        }

        old_form_data = {
            "ZHBNOW": "0", "ZHB": "0", "MQJC": "0", "KZZD": None, "SWBZ": "", "XWBZ": "", "BZ": "",
            "ISSAME": "", "SORTNUM": "29", "XW_TJTW": "", "XW_XWTW": "", "SW_TJTW": "", "SWTW": "",
            "SFZX": None, "SFCS": None, "SF": "", "ZGFXDQSF": None, "DQJZS": None, "STZK": "",
            "BSRQ": date.today().__str__(), "ROLE": "学生", "FDY": self.teacher_id, "BJ": self.class_name,
            "BM": self.school_name,
            "XM": self.name, "GH": self.username, "ISREPORT": "0"
        }
        if self.location == "在中高风险地区":
            form_data["ZGFXDQSF"] = "0"
            old_form_data["ZGFXDQSF"] = "0"
        else:
            form_data["ZGFXDQSF"] = ""
            old_form_data["ZGFXDQSF"] = ""

        if self.location == "在沪":
            form_data['SFCS'] = "31|1"
            form_data["DQJZS"] = "在沪"
            old_form_data['SFCS'] = "|0"
            old_form_data["DQJZS"] = "在其它地区"
        else:
            form_data['SFCS'] = "|0"
            form_data["DQJZS"] = "在其它地区"
            old_form_data['SFCS'] = "31|1"
            old_form_data["DQJZS"] = "在沪"

        if self.at_school:
            form_data['SFZX'] = "在校"
            old_form_data['SFZX'] = "不在校"
            if datetime.now().hour >= 12:
                form_data["XW_XWTW"] = "0"
                form_data["SWTW"] = ""
                form_data['KZZD'] = "TRUE下午在校"
                old_form_data['KZZD'] = "TRUE下午不在校"
            else:
                form_data["XW_XWTW"] = ""
                form_data["SWTW"] = "0"
                form_data['KZZD'] = "TRUE上午在校"
                old_form_data['KZZD'] = "TRUE上午不在校"
        else:
            form_data['SFZX'] = "不在校"
            old_form_data['SFZX'] = "在校"
            if datetime.now().hour >= 12:
                form_data["XW_XWTW"] = "0"
                form_data["SWTW"] = ""
                form_data['KZZD'] = "TRUE下午不在校"
                old_form_data['KZZD'] = "TRUE下午在校"
            else:
                form_data["XW_XWTW"] = ""
                form_data["SWTW"] = "0"
                form_data['KZZD'] = "TRUE上午不在校"
                old_form_data['KZZD'] = "TRUE上午在校"
        report_data = {
            "sid": sid,
            "cmd": "CLIENT_BPM_FORM_PAGE_P_SAVE_DATA",
            "processInstId": process_inst_id,
            "taskInstId": "",
            "openState": "0",
            "currentPage": "1",
            "formDefId": form_def_id,
            "formData": str(form_data),
            # location for boId, boDefId
            "oldFormData": str(old_form_data),
            "isCreate": "true",
            "commentInfo": {
                "isSelected": "false", "isValidateForm": "true", "commentOption": "", "commentId": "",
                "isCommentCreate": "false", "hasFiles": "false", "processDefId": process_def_id,
            },
            "isTransact": "false",
            "isValidateForm": "true",
        }
        report_result = self.sess.post(sid_url, data=report_data)
        return report_result.json()

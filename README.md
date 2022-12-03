# SLU Daily Report
 上海立信会计金融学院COVID-19流行病防治每日一报的自动化脚本

![](https://img.shields.io/badge/tests-2021.1.18%20%E2%9C%94-green)

## 简介

**学生2021版**

学校要求学生每日汇报健康状况. 本软件为解决填报时经常忘记和低效的问题, 自动化完成这个报告.

## 安装

1. 在Linux操作系统上下载本软件, 在`main.py`文件中填写个人信息.
2. 运行:
 ```bash
 cd ${installed_path}
 pip install -r requirements
 ```
3. 使用`screen`创建新进程, 运行`python main.py`.

[改进] 开发者招募中, 请更新至使用 crontab 定时任务的方法.

## 用法

填写个人信息的指示: (注意, 表单的字段在不断改变, 希望开发者积极维护)

| 参数名          | 数据格式   | 描述                                                         |
| --------------- | --------- | ------------------------------------------------------------ |
| username        | string    | 学号                                                         |
| at_school       | bool      | 是否在校                                                      |
| at_shanghai     | string    | 选项: "在沪", "在中高风险地区", "在其它地区"                    |
| ad_code         | string    | 所在地, 4位行政区码, 例如上海市"3101". 详情参见: http://preview.www.mca.gov.cn/article/sj/xzqh/2020/2020/202101041104.html |
| covid_patient   | int       | 选项: 0(健康), 1(疑似患者), 2 (确诊患者).                      |
| teacher_id      | string    | 辅导员工号 (可在"企业微信"联系人中查看)                         |
| school_name     | string    | 学院名称, 现仅支持: 统计与数学学院, 信息管理学院, 财税与公共管理学院 |
| class_name      | string    | 班级名称                                                      |
| name            | string    | 您的姓名                                                      |


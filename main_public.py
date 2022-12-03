from datetime import datetime
from time import sleep

from lixin1 import DailyReport

my_reports = [
    DailyReport(
        username="201910101", at_school=True, location="在沪", ad_code="3101",
        covid_patient=0, teacher_id="20000000", school_name="信息管理学院",
        class_name="班级名称", name="张三丰"
    ),

]
while 1:
    if datetime.now().hour == 8:
        for report in my_reports:
            result = report.run()
            print(report.name, result)
        sleep(3600*23)  # 23 hours
    elif datetime.now().hour == 7:
        sleep(3600)  # 1 hours
    else:
        sleep(3600)  # 1 hours

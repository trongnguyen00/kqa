import pandas as pd
import time
from pathlib import Path
from datetime import datetime
from robot.api import logger
from cdrouter import CDRouter
from cdrouter.packages import Package
from cdrouter.jobs import Job
from cdrouter.results import Result
from cdrouter.devices import Device
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

host="http://192.168.150.240"
username="KVINQA"
password="kaon1234"
package_name_tet="QA/General/IPv4(DHCP)_TRONG"
session = CDRouter(host, username=username, password=password)

# session.packages.get_by_name(package_name_tet)
# print(vars(session.packages.get_by_name(package_name_tet)))

id_package=session.packages.get_by_name(package_name_tet)

# print(vars(session.results.get(20250514094343).options))

print(vars(session.results.summary_stats(id=20250514094343)))

result_obj = session.results.iter_list()
# print(vars(result_obj))
for test in result_obj:
    if test.package_name == package_name_tet:
        print(f"Result ID: {test.id}, Package Name: {test.package_name}, Device Name: {test.device_name}, Package_Id: {test.package_id}, Result Status: {test.status}")
        # You can access other attributes of the test object as needed
        # For example, to print all attributes of the test object:
        #
    # print(vars(test))

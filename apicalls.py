import requests
import json 
from functions import db_select 

URL = "http://127.0.0.1:8000"
#URL = "https://risk-assess-sys.herokuapp.com/"


r2 = requests.get(URL+'/report').json()
print(r2)

"""
header = {"Content-Type" : "application/json"}
data = {'file_name':'testdata/testdata.csv'}
r1 = requests.post(URL+'/prediction', headers=header, data = json.dumps(data)).json()


r2 = requests.get(URL+'/scoring').json()
r3 = requests.get(URL+'/summarystats').json()
r4 = requests.get(URL+'/diagnostics').json()
r5 = requests.get(URL+'/apireturns').content.decode('utf8').strip()


#combine all API responses
with open(r5,"w") as f:
    f.write("API Responses\n")
    f.write('------------------------------------------------\n')
    f.write("Test data predictions\n")
    f.write(str(r1['data']))
    f.write('\n------------------------------------------------\n')

    f.write("F1 score for production model\n")
    f.write(str(r2['data']))
    f.write('\n------------------------------------------------\n')

    f.write("Summary stats for each feature\n")
    f.write("Feature - Mean - Median - Std\n")
    for row in r3['data']:
        f.write(f"{row[0]} - {row[1]} - {row[2]} - {row[3]}\n")
    f.write('\n------------------------------------------------\n')


    f.write("% of missing data per column\n")
    for row in r4['missing_data']:
        f.write(f"{row[0]} - {row[1]}\n")
    f.write('\n------------------------------------------------\n')

    f.write("Execution times\n")
    for row in r4['execution_time']:
        f.write(f"{row[0]} - {row[1]}\n")
    f.write('\n------------------------------------------------\n')
    f.write("List of outdated packages: package name - installed version - newest available version\n")
    for row in r4['outdated_packages']:
        f.write(f"{row}")
"""


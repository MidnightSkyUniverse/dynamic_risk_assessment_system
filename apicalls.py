import requests
import json 

URL = "http://127.0.0.1:8000"

header = {
            "Content-Type" : "application/json",
        }
data = {'file_name':'testdata/testdata.csv'}
r1 = requests.post(URL+'/prediction', headers=header, data = json.dumps(data)).json()

r2 = requests.get(URL+'/scoring').json()
r3 = requests.get(URL+'/summarystats').json()
r4 = requests.get(URL+'/diagnostics').json()


#combine all API responses
with open("apireturns.txt","w") as f:
    f.write("API Responses\n")
    f.write('------------------------------------------------\n')
    f.write('------------------------------------------------\n')
    f.write("Test data predictions\n")
    f.write(str(r1['data']))
    f.write('\n------------------------------------------------\n')

    f.write("F1 score for the model\n")
    f.write(str(r2['data']))
    f.write('\n------------------------------------------------\n')

    f.write("Summary stats for each feature\n")
    for row in r3['data']:
        f.write(str(row)+'\n')
    f.write('------------------------------------------------\n')


    f.write("% of missing data per column\n")
    f.write(str(r4['missing_data']))
    f.write('\n------------------------------------------------\n')
    f.write("Execution times\n")
    f.write(str(r4['execution_time']))
    f.write('\n------------------------------------------------\n')
    f.write("List of outdated packages: package name - installed version - newest available version\n")
    for row in r4['outdated_packages']:
        f.write(row+'\n')




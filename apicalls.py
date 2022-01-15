import requests

URL = "http://127.0.0.1:8000"


response1 = requests.post(URL+'/prediction', {'file_name':'xxx'}).content#testdata/testdata.csv'})#.content
print(response1)

#response = requests.get(URL+'/scoring').content

#response2 = requests.get(URL+'/summarystats').content

#response3 = requests.get(URL+'/diagnostics').content



#combine all API responses
#responses = #combine reponses here

#write the responses to your workspace



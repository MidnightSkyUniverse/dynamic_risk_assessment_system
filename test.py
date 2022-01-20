import subprocess
import json

output = subprocess.check_output(["heroku", "config:get", "DATABASE_URL", "-a", "risk-assess-sys"]).decode('utf8').strip()
print(output)


with open('postgreSQL.json', 'r') as f:
    DATABASE_URL = json.load(f)['DATABASE_URL']

print(DATABASE_URL)


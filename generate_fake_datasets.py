import random
import string
import pandas as pd
from statistics import mean, median, stdev

def get_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str

df = pd.read_csv("sourcedata/dataset1.csv").drop('corporation',axis=1)
print("col: min - max / mean - median")
for col in df.columns.values:
    #print( f"{df[col].min()} - {df[col].max()}")
    print (f"{col}: {df[col].mean()} - {df[col].median()} - {df[col].std()}")
    print("\n\n")


# lastmonth_activity (0,98765), mean=2895, median=99, std=13891
# lastyear_activity (0,10983), mean=1133, median=422, std=2118
# number_of_employees (1, 3782), mean=242, median = 22.5, std=601


corporation = [get_random_string() for x in range(0,1000)]
exited = [random.randint(0,1) for x in range(0,1000)]

r1 = [random.randint(10000,100000) for x in range(100,0) ]
r2 = [random.randint(5000,10000) for x in range(1,290) ]
r3 = [random.randint(0,5000) for x in range(1,600) ]
#print (f"{mean(r1+r2+r3)} - {median(r1+r2+r3)} - {stdev(r1+r2+r3)}")
lastmonth_activity = r1+r2+r3
random.shuffle(lastmonth_activity)

r1 = [random.randint(1000,9000) for x in range(1,30) ]
r2 = [random.randint(150,1000) for x in range(1,450) ]
r3 = [random.randint(0,150) for x in range(1,420) ]
#print (f"{mean(r1+r2+r3)} - {median(r1+r2+r3)} - {stdev(r1+r2+r3)}")
lastyear_activity = r1+r2+r3
random.shuffle(lastyear_activity)

r1 = [random.randint(0,2000) for x in range(1,20) ]
r2 = [random.randint(0,450) for x in range(1,300) ]
r3 = [random.randint(0,25) for x in range(1,680) ]
#print (f"{mean(r1+r2+r3)} - {median(r1+r2+r3)} - {stdev(r1+r2+r3)}")
number_of_employees = r1+r2+r3
random.shuffle(number_of_employees)

data = []
for x,y,z,v,e in zip(corporation, lastmonth_activity, lastyear_activity, number_of_employees,exited):
    data.append({'corporation': x, 'lastmonth_activity': y, 'lastyear_activity': z,'number_of_employees': v, 'exited': e})

df2 = pd.DataFrame(data)
#print(df2)
df2.to_csv("sourcedata/dataset13.csv",index=False)

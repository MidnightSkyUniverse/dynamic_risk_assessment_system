import subprocess
import json
import matplotlib.pyplot as plt
from functions import db_select

def draw_f1():
    f1_scores = db_select("SELECT f1_score from f1;")
    f1list = [f[0] for f in f1_scores]
    print(f1list)
   
    plt.plot(f1list)
    f = plt.figure(figsize=(18,8),edgecolor='red') 
    plt.savefig('models/figure.png',format='png')

if __name__ == '__main__':
    draw_f1()

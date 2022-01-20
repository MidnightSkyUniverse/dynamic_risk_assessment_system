import pickle
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions
from functions import process_data
from reportlab.pdfgen import canvas

###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

test_data_path = os.path.join(config['test_data_path']) 
test_file = config['test_file']

output_model_path = config['output_model_path']

def pdf_generate(text):
    """
    Generate report including information about performance of the model
    """
    c = canvas.Canvas(output_model_path + "report.pdf")
    c.drawString(100,750,text)
    c.save()

def cf_matrix(file_name):
    """
    Confusion matrix
    """
    predictions = model_predictions(file_name)
    X, y = process_data(file_name)
    cf_matrix = metrics.confusion_matrix(y, predictions)

    # This code is taken form : https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea
    group_names = ["True Neg","False Pos","False Neg","True Pos"]
    
    group_counts = ["{0:0.0f}".format(value) for value in cf_matrix.flatten()]

    group_percentages = ["{0:.2%}".format(value) for value in
                     cf_matrix.flatten()/np.sum(cf_matrix)]

    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]

    labels = np.asarray(labels).reshape(2,2)

    sns.heatmap(cf_matrix, annot=labels, fmt="", cmap='Reds')
    plt.savefig(output_model_path + 'confusionmatrix.png')

    

#if __name__ == '__main__':
#    score_model()

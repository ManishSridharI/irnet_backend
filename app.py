# -*- coding: utf-8 -*-

import os
import pandas as pd
from flask import Flask, jsonify, render_template, request

#os.environ['GCLOUD_PROJECT'] = 'hackteam-cloudthree'
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:\GCP Hackathon\hackteam-cloudthree-100b006f1091.json"

#import json


app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "hello": "world"
    })

@app.route('/datasets')
def datasets_info():
    data_folder = '/app/IRnet-main/data'

    # Manual mapping of dataset to drug, update as needed
    drug_mapping = {
        "Gide2019_PD1_Melanoma_RNASeq": "DrugA",
        "IMvigor210": "DrugB",
        "Kim2018_PD1_Gastric_RNASeq": "DrugC",
        "Liu2019_Melanoma_RNAseq": "DrugD",
        "Auslander" : "DrugA",
        "Gide" : "DrugA",
        "Gide2019_PD1+CTLA4_Melanoma_RNASeq" : "DrugA",
        "Riaz2017_PD1_Melanoma_RNASeq_Ipi.Naive" : "DrugA"
        # Add more mappings as necessary
    }

    # Iterate over each directory in the data folder
    for dataset_name in os.listdir(data_folder):
        dataset_path = os.path.join(data_folder, dataset_name)
        if os.path.isdir(dataset_path):

            # Retrieve the corresponding drug from the mapping, default to "Unknown" if not found

            datasets_info.append({
                "dataset_name": dataset_name,
                "number_of_patients": 49,
                "drug": "a"
            })

    return jsonify(datasets_info)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 9900)))
    
# from flask import Flask, send_from_directory

# app = Flask(__name__, static_folder='/home/mizy9/IRnet-web/IRnet_frontend/build', static_url_path='')

# @app.route('/')
# def index():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/<path:path>')
# def static_files(path):
#     return send_from_directory(app.static_folder, path)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=9900)

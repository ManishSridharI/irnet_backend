# -*- coding: utf-8 -*-

import os
import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # Import CORS

#os.environ['GCLOUD_PROJECT'] = 'hackteam-cloudthree'
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:\GCP Hackathon\hackteam-cloudthree-100b006f1091.json"

#import json


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "hello": "world"
    })

@app.route('/prediction_info', methods=['POST'])
def prediction_info():
    # Get JSON data from the request
    data = request.json

    # Here you would typically store the data or perform operations based on it
    # For demonstration purposes, we'll just return a success message
    return jsonify({"message": "Data received successfully", "receivedData": data})


@app.route('/datasets')
def datasets_info():
    data_folder = '/app/IRnet-main/data'
    datasets =[]
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

            clinic_files = [f for f in os.listdir(dataset_path) if 'clinic' in f]
            if clinic_files:
                # Assuming you're interested in the first matching file
                clinic_file_path = os.path.join(dataset_path, clinic_files[0])
                # Count the number of lines (patients) in the found clinic file
                with open(clinic_file_path, 'r') as f:
                    num_patients = sum(1 for _ in f)

            # Retrieve the corresponding drug from the mapping, default to "Unknown" if not found
            drug = drug_mapping.get(dataset_name, "Unknown")
            datasets.append({
                "dataset_name": dataset_name,
                "number_of_patients": num_patients-1,
                "drug": drug
            })

    return jsonify(datasets)

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

# -*- coding: utf-8 -*-

import os
import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # Import CORS
import mysql.connector
from flaskext.mysql import MySQL
#import subprocess
from IRnet_main import predict
#from werkzeug.utils import secure_filename

#import json
# Define allowed hosts
ALLOWED_HOSTS = [
    'http://trbil.missouri.edu', 
    'http://digbio-g2pdeep.rnet.missouri.edu',
    'http://digbio-g2pdeep.rnet.missouri.edu:9090',
    'http://digbio-g2pdeep.rnet.missouri.edu:9090/',
    'http://g2pdeep.org',
    'http://127.0.0.1', 
    'http://127.0.0.1:9090/',
]

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:9090"}})


# db_config = {
#     'host': 'digbio-db1.rnet.missouri.edu',
#     'user': 'KBCommons',
#     'password': 'KsdbsaKNm55d3QtvtX44nSzS_',
#     "port": 3306,
#     'db': 'irnet'
# }
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'KBCommons'
app.config['MYSQL_DATABASE_PASSWORD'] = 'KsdbsaKNm55d3QtvtX44nSzS_'
app.config['MYSQL_DATABASE_DB'] = 'irnet'
app.config['MYSQL_DATABASE_HOST'] = 'digbio-db1.rnet.missouri.edu'
mysql.init_app(app)

@app.route('/')
def home():
    return jsonify({
        "hello": "world"
    })

@app.route('/test', methods=['GET'])
def test_info():
    # Get JSON data from the request
    #data = request.json
   
    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("SELECT * FROM drug_info;")
    result = cursor.fetchall()

    return jsonify(result)

@app.route('/drug_info', methods=['POST'])
def drug_info():
    # Get JSON data from the request
    data = request.json
   
    conn = mysql.connect()
    cursor =conn.cursor()

    job_id = data['jobId']
    card_value = data['cardValue']

    query = "INSERT INTO drug_info VALUES (%s, %s)"
    cursor.execute(query, (job_id, card_value))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Data received and stored successfully"})

@app.route('/dataset_info', methods=['POST'])
def dataset_info():
    # Get JSON data from the request
    data = request.json

    conn = mysql.connect()
    cursor =conn.cursor()
    job_id = data['jobId']
    dataset_name = data['dataset']['dataset_name']


    query = "INSERT INTO dataset_info VALUES (%s, %s)"
    cursor.execute(query, (job_id, dataset_name))
    conn.commit()
    cursor.close()
    conn.close()

    # Here you would typically store the data or perform operations based on it
    # For demonstration purposes, we'll just return a success message
    return jsonify({"message": "Data received successfully"})

@app.route('/file_upload', methods=['POST'])
def file_upload():
    # Get JSON data from the request
    if 'gene_counts' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['gene_counts']
    job_id = request.form['jobId']
    dataset_name = request.form['dataset_name']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and dataset_name:
       # filename = secure_filename(file.filename)
        save_path = f'/app/IRnet_main/data/{dataset_name}'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file.save(os.path.join(save_path, 'gene_counts.txt'))

        conn = mysql.connect()
        cursor =conn.cursor()


        query = "INSERT INTO dataset_info VALUES (%s, %s)"
        cursor.execute(query, (job_id, dataset_name))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Data received successfully"})
    else:
        return jsonify({"error": "Invalid data"}), 400

    # Here you would typically store the data or perform operations based on it
    # For demonstration purposes, we'll just return a success message
    return jsonify({"message": "Data received successfully"})

@app.route('/job_id')
def job_id():
    # Get JSON data from the request
    conn = mysql.connect()
    cursor =conn.cursor()

    query = "SELECT IFNULL(MAX(job_id), 0) FROM drug_info"
    cursor.execute(query)
    highest_job_id_drug = cursor.fetchone()[0]

    query = "SELECT IFNULL(MAX(job_id), 0) FROM dataset_info"
    cursor.execute(query)
    highest_job_id_dataset = cursor.fetchone()[0]

    query = "SELECT IFNULL(MAX(job_id), 0) FROM prediction_info"
    cursor.execute(query)
    highest_job_id_prediction = cursor.fetchone()[0]

    highest_job_id = max(highest_job_id_drug, highest_job_id_dataset, highest_job_id_prediction)

    cursor.close()
    conn.close()

    return jsonify({"highest_job_id": highest_job_id})

@app.route('/run_prediction', methods=['GET','POST'])
def run_prediction():
    # Get JSON data from the request
    data = request.json

    conn = mysql.connect()
    cursor =conn.cursor()
    job_id = data['jobId']

    query = "SELECT drug FROM drug_info WHERE job_id = %s"
    cursor.execute(query, (job_id))
    drug_info = cursor.fetchone()

    query = "SELECT dataset_name FROM dataset_info WHERE job_id = %s"
    cursor.execute(query, (job_id))
    dataset_info = cursor.fetchone()
    dataset_name = dataset_info[0]

    query = "SELECT IFNULL(MAX(pathway_relation_tableid), 0) FROM prediction_info"
    cursor.execute(query)
    relation_id = cursor.fetchone()[0] + 1

    query = "SELECT IFNULL(MAX(pathway_weight_tableid), 0) FROM prediction_info"
    cursor.execute(query)
    weight_id = cursor.fetchone()[0] + 1

    query = "SELECT IFNULL(MAX(prediction_results_tableid), 0) FROM prediction_info"
    cursor.execute(query)
    results_id = cursor.fetchone()[0] + 1

    # query = "INSERT INTO prediction_info (job_id, prediction_results_tableid, pathway_weight_tableid, pathway_relation_tableid) VALUES (%s, %s, %s, %s)"
    # cursor.execute(query, (job_id, results_id, weight_id, relation_id))
    conn.commit()
    cursor.close()
    conn.close()
    input_path = f'/app/IRnet_main/data/{dataset_name}/gene_counts.txt'
    output_path = './prediction_results/'
   # predict.main(input_path, output_path, drug_info[0], job_id, results_id, weight_id, relation_id)
    try:
        predict.main(input_path, output_path, drug_info[0], job_id, results_id, weight_id, relation_id)
        return jsonify({"message": "Prediction run successfully"})
    except Exception as e:
        return jsonify({"message": "Failed to run prediction", "error": str(e)})

    # Here you would typically store the data or perform operations based on it
    # For demonstration purposes, we'll just return a success message
    return jsonify(drug_info)


@app.route('/datasets')
def datasets_info():
    data_folder = '/app/IRnet_main/data'
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

@app.route('/prediction_results/<job_id>', methods=['GET'])
def get_prediction_results(job_id):
    conn = mysql.connect()
    cursor =conn.cursor()
    try:
        # Assume the data structure in the table is simple for demonstration
        query = f"SELECT prediction_results_tableid from prediction_info where job_id = {job_id}"
        cursor.execute(query)
        table_id = cursor.fetchone()

        table_name = f"prediction_results_{table_id[0]}"
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchall()
        #data = [dict(row) for row in result]
        #return jsonify(result)
        transformed_results = [{
            "Patient ID": row[0],  # assuming row[0] is the patient identifier
            "Predicted score": float((row[1])),  # assuming row[1] is the score
            "Predicted ICI response": bool(int(row[2]))  # assuming row[2] is the predicted ICI response, stored as '0' or '1'
        } for row in result]

        return jsonify(transformed_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/node_results/<job_id>/<patient_id>', methods=['GET'])
def get_node_results(job_id, patient_id):
    conn = mysql.connect()
    cursor =conn.cursor()
    try:
        # Assume the data structure in the table is simple for demonstration
        query = f"SELECT pathway_weight_tableid from prediction_info where job_id = {job_id}"
        cursor.execute(query)
        table_id = cursor.fetchone()

        table_name = f"pathway_weights_{table_id[0]}"
        query = f"""SELECT Pathway,Weight FROM {table_name} WHERE Patient = '{patient_id}'"""
        cursor.execute(query)
        result = cursor.fetchall()
        transformed_results = [{
            'Patient': row[0], 
            'Weight': float((row[1]))  
        } for row in result]

        return jsonify(transformed_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/edge_results/<job_id>/<patient_id>', methods=['GET'])
def get_edge_results(job_id, patient_id):
    conn = mysql.connect()
    cursor =conn.cursor()
    try:
        # Assume the data structure in the table is simple for demonstration
        query = f"SELECT pathway_relation_tableid from prediction_info where job_id = {job_id}"
        cursor.execute(query)
        table_id = cursor.fetchone()

        table_name = f"pathway_relations_{table_id[0]}"
        query = f"""SELECT Source,Target,Interaction_Score FROM {table_name} WHERE Patient_ID = '{patient_id}'"""
        cursor.execute(query)
        result = cursor.fetchall()
        transformed_results = [{
            'source': row[0], 
            'target': row[1],  
            'interaction_score': float((row[2]))
        } for row in result]

        return jsonify(transformed_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 9900)))
    
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

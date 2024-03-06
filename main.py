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

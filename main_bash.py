from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
from PIL import Image
import os
import shutil
from shutil import make_archive
import glob
from pathwaymodule import cfg

app = Flask(__name__)
CORS(app)

input_path_ = ''

@app.route('/upload_image', methods=['POST'])
def upload_image():
    #clearing data
    if os.path.exists('./static'):
        shutil.rmtree('./static')
    if os.path.exists('./elem_rele.zip'):
        os.remove('./elem_rele.zip')
        
    try:
        image_data = request.files.get('image')  # Get the image data from the FormData
        print("image_data",image_data)
        upload_path = request.form.get('uploadPath')  # Get the upload path
        image_name = request.form.get('imageName')# Get the image name
        cfg.input_path_ = upload_path + './' + image_name
        
        UPLOAD_FOLDER = upload_path # Replace with your desired upload folder
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        
        if not image_data or not upload_path or not image_name:
            return 'Missing data', 400
        
        os.makedirs(upload_path, exist_ok=True)
        img = Image.open(image_data)
        img.save(image_name)
        shutil.move(('./'+image_name), upload_path)

        return 'Image uploaded and saved successfully'
    
    except Exception as e:
        return 'Error uploading image: {}'.format(str(e))


@app.route('/predict', methods=['POST'])
def predict():
    print('Predict endpoint accessed')
    data = request.get_json()
    print(data)
    cmd = data.get('cmd')  # Assuming the JSON contains a "cmd" field
    
    try:
        # Run the command and capture the output
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        output = result.stdout
        error_output = result.stderr

        response_data = {
            "output": output,
            "error_output": error_output
        }
        print('successfull predict')
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_element_relation', methods=['GET'])
def get_element_relation():
    img_name = request.args.get('imgName')
    print('image_name in python: ',img_name)
    if os.path.exists('./ext_images/ext_images'):
        shutil.rmtree('./ext_images/ext_images')
        """source_folder='./ext_images'
        destination_folder='./ext_images/ext_images'
        source_path = os.path.join(source_folder, img_name)
        destination_path = os.path.join(destination_folder, img_name)
        shutil.move(source_path, destination_path)"""
        print('Successfully moved from python code')
    shutil.make_archive('elem_rele','zip', './ext_images')
    if os.path.exists('./elem_rele.zip'):
        print("ZIP file created")
        return send_file('./elem_rele.zip', as_attachment=True)
    else:
        print("ZIP Not created")

if __name__ == '__main__':
    app.run(host='localhost', port=5000)

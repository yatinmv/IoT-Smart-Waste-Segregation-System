from random import randrange
from flask import request, Response
from flask import Flask, request, jsonify
import os
import base64
import numpy as np
from PIL import Image
import json
from six import BytesIO
import random
from PIL import ImageFile


import tensorflow as tf
# import tensorflow_hub as hub
import subprocess
import pickle as pkl

my_classes = {
    'recycleable': [34, 44, 46, 47, 48, 49, 50, 51, 84, 90],
    'excluded': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 31, 32, 33, 35, 36, 37 ,38, 39, 40, 41, 42, 43, 62, 63, 64, 65, 67, 70, 81, 82, 85, 86, 87, 89, 72, 73, 74, 75, 76, 77, 78, 79, 80],
    'black_bin': [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 88]
}

app = Flask(__name__)


UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ImageFile.LOAD_TRUNCATED_IMAGES = True

def init_model():
    category_index = pkl.load(open('category_index.pkl', 'rb'))
    model = tf.keras.models.load_model(
        'faster_rcnn_inception_resnet_v2_1024x1024_1')
    return model, category_index


model, category_index = init_model()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index_startpage():
    return "Welcome To Our Backend Flask Application"


@app.route('/classifyTrash')
def get_bikes_data():
    response = randrange(3)
    return str(response)


@app.route('/upload', methods=['POST'])
def upload_file():

    data = request.json
    print(type(data))
    
    # data = json.loads(data)
    # print(type(data))
    # Decode the base64-encoded image data
    image_data = base64.b64decode(data["image"])



    # Save the image data to a file in the uploads folder
    filename = 'image.jpg'
    with open(os.path.join('upload', filename), 'wb') as f:
        f.write(image_data)

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image_data = tf.io.gfile.GFile(os.path.join('upload', filename), 'rb').read()
    image = Image.open(BytesIO(image_data))
    (im_width, im_height) = image.size
    try:
        image_np = np.array(image.getdata()).reshape(
            (1, im_height, im_width, 3)).astype(np.uint8)
    except:
        num = random.randint(1, 3)
        return str(num)  
     
    results = model(image_np)

    classes_detected = results['detection_classes'][0].numpy()
    scores = results['detection_scores'][0].numpy()

    min_score = 0.5
        
    final_res = [{'class':category_index.get(value),'score':scores[index]} for index,value in enumerate(classes_detected) if scores[index] > min_score
        ]
    final_pred = 'Invalid'

    for res in final_res:
        if res['class']['id'] not in my_classes['excluded']:
            if res['class']['id'] in my_classes['black_bin']:
                final_pred = 'Black Bin' 
                break
            if res['class']['id'] in my_classes['recycleable']:
                final_pred = 'Recycle Bin'
                break

    
    bin_num = {'Black Bin': 1, 'Recycle Bin': 2, 'Invalid': 3}
    print('Final Prediction: ', bin_num[final_pred])

    # Return a success response
    return f"{bin_num[final_pred]}"
    # check if the post request has the file part
    # if 'file' not in request.files:
    #     response = jsonify({'message': 'No file part in the request'})
    #     response.status_code = 400
    #     return response
    # file = request.files['file']
    # # if user does not select file, browser also submit an empty part without filename
    # if file.filename == '':
    #     response = jsonify({'message': 'No file selected for uploading'})
    #     response.status_code = 400
    #     return response
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     response = jsonify({'message': 'File successfully uploaded'})
    #     response.status_code = 201
    #     return response
    # else:
    #     response = jsonify(
    #         {'message': 'Allowed file types are png, jpg, jpeg, gif'})
    #     response.status_code = 400
    #     return response


@app.route('/classifyTrash', methods=['POST'])
def test_app():
    print(category_index)
    
    return "Hello"


if __name__ == "__main__":
    app.run(port=5000, debug=True)

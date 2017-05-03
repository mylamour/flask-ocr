#!/usr/bin/env python
#coding:utf-8

"""
  * Created by mour on 2017/4/28.
"""

from flask import Flask
import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template,redirect,make_response,url_for
from werkzeug.utils import secure_filename
from pre_img import process_image
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

_VERSION = 1  # API version

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path="./uploads/{}".format(filename)
            print ("file was uploaded in {} ".format(path))
            rec_string = process_image(path=path)
            return jsonify({"output": rec_string})
    elif request.method == 'GET':
        return render_template('dropimage.html')
    else:
        return jsonify({"error": "哪里出错了，不过我也不知道哪里出错了，刷个新试试吧"})

@app.route('/ocrit', methods=['POST'])
def ocr():
    try:
        url = request.json['image_url']
        if url.split('.')[-1] in ['jpg','png','tif']:
            rec_string = process_image(url=url)
            return jsonify({"output": rec_string })
        else:
            return jsonify({"error": "Not Support file types, please"})
    except:
        return jsonify({"error": "we only support [jpg, ,jpeg, png ,tif] or url like {'image_url': 'some_jpeg_url'}"})


@app.errorhandler(500)
def internal_error(error):
    print(str(error))  # ghetto logging

@app.errorhandler(404)
def not_found_error(error):
    print(str(error))

@app.errorhandler(405)
def not_allowed_error(error):
    print(str(error))

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    #app.debug = True
    app.run(host="0.0.0.0",port = int(8080))

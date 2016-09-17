from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
from classifierFactory import *
from scipy import misc

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

classifier = getKNNClassifier()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/api/classify/<filepath>', methods=['GET'])
def classifyImageAPI(filepath):
    filename = os.path.join("uploads",secure_filename(filepath))
    imagearr = misc.imread(filename)
    imclass = classifier.classifyImage(imagearr)
    return imclass


@app.route('/api/classify', methods=['POST'])
def uploadImageAPI():
    # check if the post request has the file part
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != ''  and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename
    return "No file uploaded", 4


@app.route('/classify/<filepath>', methods=['GET'])
def classifyImage(filepath):
    filename = os.path.join("uploads",secure_filename(filepath))
    imagearr = misc.imread(filename)
    imclass = classifier.classifyImage(imagearr)
    return render_template('classification.html',imclass=imclass)


@app.route('/', methods=['GET', 'POST'])
def uploadImage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("classify/"+filename)
    return render_template('index.html')


if __name__ == "__main__":
    app.run('0.0.0.0',1708)
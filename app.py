from flask import Flask, render_template, flash, request, redirect, url_for
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from flask import send_from_directory
from PIL import Image
import uuid

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file multipart
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Give the filename a unique ID
            site_type = request.form.get('site-type')
            file_id = str(uuid.uuid1())+"-"+site_type+"-"+filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_id))
            return redirect(url_for('download_file', name=file_id))
    return render_template('index.html')


@app.route('/uploads/<name>')
def download_file(name):

    flat = Image.open('static/uploads/' + name)

    # Check which mockup is required
    if "d48" in name:
        mockup = Image.open('static/mockups/wide-situ.jpg')
        area = (276,146,1670,843)
        size = (1394, 697)
    elif "d6" in name:
        mockup = Image.open('static/mockups/portrait-situ.jpg')
        area = (699,99,1217,875)
        size = (518, 776)
    elif "d96" in name:
        mockup = Image.open('static/mockups/superwide-situ.jpg')
        area = (285,334,1707,678)
        size = (1422, 344)

    # Resize uploaded image to fit mockup
    flat.thumbnail(size)
    # Paste uploaded image into mockup
    mockup.paste(flat, area)
    # Save new image and return it
    mockup.save(os.path.join(app.config['UPLOAD_FOLDER'], name+'situ.jpg'))
    return send_from_directory(app.config["UPLOAD_FOLDER"], name+'situ.jpg')

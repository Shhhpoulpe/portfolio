from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from fastai.vision.all import *
import pathlib
from pathlib import Path
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

plt = platform.system()
if plt == 'Linux': pathlib.WindowsPath = pathlib.PosixPath
learn = load_learner(Path('./static/models/export_safe.pkl'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def wtc_predict(filename):
    pred,pred_idx,probs = learn.predict(f'{UPLOAD_FOLDER}{filename}')
    pourcentage = round(float(probs[pred_idx])*100,2)
    resultat = f"{pred} et j'en suis sur à {pourcentage} %"
    return resultat

@app.route("/")
def home():
    return render_template(
        "index.html"
    )     

@app.route('/wtc')
def wtc():
    return render_template('wtc.html')
 
@app.route('/wtc', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("Pas d'image sélectionnée")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'{wtc_predict(filename)}')
        return render_template('wtc.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
# if __name__ == "__main__":
#     app.run()
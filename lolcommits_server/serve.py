import os

from flask import Flask, Response, jsonify, request, redirect
from flask import render_template, send_from_directory, url_for
from werkzeug import secure_filename


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(MODULE_DIR, "uploads/")

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recent.json')
def recent():
    images = sorted(
        os.listdir(app.config['UPLOAD_FOLDER']),
        key=lambda p: os.path.getctime(
            os.path.join(app.config['UPLOAD_FOLDER'], p)
        )
    )
    if len(images):
        image = images[-1]
    else:
        image = 'default.jpg'
    return jsonify({'image': '/uploads/' + image})


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return Response(status=201)
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)

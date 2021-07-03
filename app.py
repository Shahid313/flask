import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from vid2pdf import getpdff
from werkzeug.utils import secure_filename
from flask import send_file



app = Flask(__name__)

UPLOAD_FOLDER = './videos'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#Homepage for showing list of friends
@app.route("/")
def index():
    return render_template("index.html")


#Adding new friends to the list
@app.route("/getpdf", methods=["POST"])
def getpdf():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        pdfname = getpdff(filepath, '#ff8100')
        # return send_file(pdfname, as_attachment=True)
        return render_template("index.html", pdfname=pdfname)


if __name__ == "__main__":
    app.run(debug=True)
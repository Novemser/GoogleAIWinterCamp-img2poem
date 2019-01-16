from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import sys
# include parent dir
sys.path.append('../')

app = Flask(__name__)

s = "static/uploads"

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  
        upload_path = os.path.join(basepath, s ,secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('index.html')
    
@app.route('/index')
def show_index():
    full_filename = 'static/uploads/Screenshot_from_2018-12-28_19-41-28.png'
    return render_template("img.html", user_image = full_filename)

if __name__ == '__main__':
    app.run(debug=True)
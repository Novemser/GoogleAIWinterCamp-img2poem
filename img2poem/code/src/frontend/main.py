from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import sys
# include parent dir
sys.path.append('./')
from object_detection import object_detection_api

import nn_process
print ('Loading Extracting Feature Module...')
extract_feature = nn_process.create('extract_feature')
print ('Loading Generating Poem Module...')
generate_poem = nn_process.create('generate_poem')

def get_poem(image_file):
    """Generate a poem from the image whose filename is `image_file`

    Parameters
    ----------
    image_file : str
        Path to the input image

    Returns
    -------
    str
        Generated Poem
    """
    # Check whether the file exists
    assert os.path.exists(image_file), FileNotFoundError(
            'File `{}` not found.'.format(image_file))
    assert not os.path.isdir(image_file), FileNotFoundError(
            'The path should be a filename instead of `{}`.'.format(image_file))
    img_feature = extract_feature(image_file)
    return generate_poem(img_feature)

app = Flask(__name__)
full_filename = 'static/uploads/Screenshot_from_2018-12-28_19-41-28.png'

s = "static/uploads"

@app.route('/api', methods=['POST', 'GET'])
def dododo():
    basepath = os.path.dirname(__file__)
    object_detection_api.process(full_filename)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        s_path = os.path.join(s ,secure_filename(f.filename))
        upload_path = os.path.join(basepath, s_path)
        f.save(upload_path)
        object_detection_api.process(upload_path)
        poems = get_poem(upload_path)
        result = ''
        if isinstance(poems, list):
            for p in poems:
                result = result + p.replace('\n', ',')

        return render_template('index.html', user_image = s_path, poem = result)
    return render_template('index.html', user_image = '', poem = 'please upload')

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
    return render_template("img.html", user_image = full_filename)

if __name__ == '__main__':
    app.run(debug=True)
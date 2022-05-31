from flask import Flask, render_template, url_for, redirect, request, flash, Response
import os
from werkzeug.utils import secure_filename
from access_Control import access_control, load_known
from capture_Data import WebCam, stop

load_known() #load our database before launching our server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "unknown")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = image_dir

webcam = WebCam()

@app.route('/')
def hello_page():
    return render_template('home_page.html')

@app.route('/uploads/')
def uploaded_file():
    return access_control()

@app.route('/captured/')
def photo_captured():
    webcam.save_photo()
    return access_control()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#if use decides to upload an image
@app.route('/upload-image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        #if user does not select file, browser also
        #submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(image_dir, filename))
            return redirect(url_for('uploaded_file')) #redirect to the function that services the upload
    return render_template('upload_image.html')


def gen(camera):
    while True:
        if stop:
            continue
        frame = camera.get_frame()
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/capture-image') #if use selects to upload a file
def capture_image():
    return render_template('capture_image.html')


@app.route('/video_feed') #Note does not open on Internet Explorer
def video_feed():
    return Response(gen(webcam), mimetype='multipart/x-mixed-replace; boundary=frame')

#helps us debug AKA dont need to restart server
if __name__ == "__main__":
    app.run(debug=True)



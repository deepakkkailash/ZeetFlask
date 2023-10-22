from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from Test import make_binary, create_response
from s3userupload import upload_user_S3

app = Flask(__name__)

# Specify the upload folder
UPLOAD_FOLDER = 'UserUploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files)
    # Check if a file was submitted
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file'

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #The below code first uploads the uploaded image locally onto the system and then calls the function make_binary that makes sure that the image is converted into b
        #binary format and then it returns the binary image onto temp. Now with create_response(temp) the response is created
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload_user_S3("UserUploads/"+filename)
        temp = make_binary("UserUploads/"+filename)
        val = create_response(temp)
        return render_template("output.html",output=val)

    else:
        return 'Invalid file extension'


if __name__ == "__main__":
    app.run(port=8888,debug=True)

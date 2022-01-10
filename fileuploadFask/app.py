from flask import Flask, json, request, jsonify
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
 
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024

ALLOWED_EXTENSIONS = set(['txt'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Homepage'
 
@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    filetype = request.args.get("filetype")
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
    for file in files:      
        if not allowed_file(file.filename):
            errors[file.filename] = 'Invalid Extension Error'
            code = 1180

        if file.filename == 'aa.txt': #not aware of file name so used as a.txt
            errors[file.filename] = 'Invalid File Name Error'
            code = 1181
            
        if os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) == app.config['MAX_CONTENT_LENGTH']:
            errors[file.filename] = 'Invalid Max size allowed' #max size allowed 16kb
            code = 1182

        if os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) == 0:
            errors[file.filename] = 'File is empty'
            code = 1185
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Successful transaction.'})
        resp.status_code = 0
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = code
        return resp
 
if __name__ == '__main__':
    app.run(debug=True)
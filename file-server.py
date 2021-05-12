from flask import Flask, request, url_for, redirect
import os
 
# Files stored in
UPLOAD_FOLDER = 'static/'
 
# Allowed files extensions for upload
ALLOWED_EXTENSIONS = set(['pdf', 'txt', 'png', 'jpg', 'csv'])
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
 
# Check file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
 
@app.route('/', methods=['GET','POST'])
def index():
 
    # If a post method then handle file upload
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect('/')
        file = request.files['file']
 
        if file.filename == '':
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 
 
    # Get Files in the directory and create list items to be displayed to the user
    file_list = ''
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        # Create link html
        link = url_for('static', filename=f) 
        file_list = file_list + '<li><a href="%s">%s</a></li>' % (link, f)
 
    # Return HTML, navigation and file upload
    return_html = '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
            <input type=file name=file><br>
            <input type=submit value=Upload>
    </form>
    <hr>
    <h1>Files</h1>
    <ol>%s</ol>
    ''' % file_list
 
    return return_html
 
 
if __name__ == '__main__':
    app.run(debug=True)

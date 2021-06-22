import requests
import time
import shutil
import os

# Allowed files extensions for upload
ALLOWED_EXTENSIONS = set(['pdf', 'txt', 'png', 'jpg', 'csv'])

FILE_UPLOAD_ENDPOINT = "http://localhost:5000/upload"
UPLOAD_DIR = "upload_folder/"
OLD_FILES_DIR = UPLOAD_DIR + "old/"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

while True:
    print("Scanning files from dir " + UPLOAD_DIR)
    for file_name in os.listdir(UPLOAD_DIR):
        if(allowed_file(file_name)):
            print("Uploading file " + file_name)
            files = { "file" : (file_name, open(UPLOAD_DIR + file_name, 'rb')) }
            r = requests.post(FILE_UPLOAD_ENDPOINT, files=files)
            if r.status_code == 200:
                print("Request succeed")
                shutil.move(os.path.join(UPLOAD_DIR, file_name), OLD_FILES_DIR)
            if r.status_code == 400:
                print("Bad request, client sent malformed / missing data")
            if r.status_code == 500:
                print("Internal server error")
            
    print("Waiting for the next round of scan")
    time.sleep(60) # Delay for 1 minute (60 seconds)

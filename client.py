import requests
import time
import os
import threading

# Allowed files extensions for upload
ALLOWED_EXTENSIONS = set(['pdf', 'txt', 'png', 'jpg', 'csv'])
FILE_UPLOAD_ENDPOINT = "http://localhost:5000/"
UPLOAD_DIR = "upload_folder/"
OLD_FILES_DIR = UPLOAD_DIR + "old/"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def client_thread(filename):
    if not filename:
        return
    files = { "file" : (filename, open(UPLOAD_DIR + filename, 'rb')) }
    try:
        r = requests.post(FILE_UPLOAD_ENDPOINT, files=files, timeout=30)
    except requests.Timeout:
        buff = "Request Timeout"
    except:
        buff = "Request Error"
    else:
        if r.status_code == 200:
            buff = "Request succeed"
            os.remove(os.path.join(UPLOAD_DIR, filename))
        if r.status_code == 400:
            buff = "Bad request, client sent malformed / missing data"
        if r.status_code == 500:
            buff = "Internal server error"
    finally:
        print("Uploading file " + " - " + filename + ":" + buff)
        return

while True:
    print("Scanning files from dir " + UPLOAD_DIR)
    print("Files: " + str(len(os.listdir(UPLOAD_DIR))))
    files = os.listdir(UPLOAD_DIR)
    threads = list()
    while files:
        for i in range(5):
            file_name = files.pop() if files else ""
            if(allowed_file(file_name) and file_name):
                thread = threading.Thread(target=client_thread,args=(file_name,), daemon=True)
                threads.append(thread)
                thread.start()
        
        for thread in threads:
            thread.join()
    print("Waiting for the next round of scan")
    time.sleep(60) # Delay for 1 minute (60 seconds)

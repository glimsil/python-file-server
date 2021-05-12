# python-file-server
Sample of simple file server in python

### Installing dependencies
To install, just type:

    pip3 install -r requirements.txt

### Run
Start the rest server typing:
    python3 file-server.py

It will serve at localhost:5000

### Testing
You can test it just by accessing `localhost:5000` where you can navigate through folders and files or also upload files via UI. You can also upload files via API.

You can run the python client example, typing:
```
    python3 client.py
```
The client scans the upload_folder every 1 minute and send all files (matching the allowed extension check) to the file server
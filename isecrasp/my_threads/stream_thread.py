import pyrebase
import json
import os
import cv2
import pickle
import time
import subprocess
from .variables import config_path, temp_path, dtthreads_path, dev_id, cred_path

with open('{}/firebaseconfig.json'.format(cred_path)) as f:
    config = f.read()

config = json.loads(config)

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def stream_handler():
    def my_stream_handler(message):
        try:
            data = message['data']['current']
        except:
            data = message['data']
        print(message)
        if data == "activate_security":
            cam = cv2.VideoCapture(0)
            with open(config_path, 'rb') as file:
                data = pickle.load(file)
            ret, frame = cam.read()
            data['first_frame'] = frame
            data['Security_Status'] = True
            with open(config_path, 'wb') as file:
                pickle.dump(data, file)
            cam.release()
            print('security activated')
        elif data == 'disable_security':
            with open(config_path, 'rb') as file:
                data = pickle.load(file)
            data['Security_Status'] = False
            data['first_frame'] = None
            with open(config_path, 'wb') as file:
                pickle.dump(data, file)
            print('security deactivated')
        elif data == 'qp':
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            cv2.imwrite('{}/out.png'.format(temp_path), frame)
            cam.release()
            subprocess.Popen(['python3', dtthreads_path, 'QP'])
        elif data == "stream_start":
            print('yep')
            with open(config_path, 'rb') as file:
                data = pickle.load(file)
            data['stream'] = True
            with open(config_path, 'wb') as file:
                pickle.dump(data, file)
        elif data == "stream_stop":
            with open(config_path, 'rb') as file:
                data = pickle.load(file)
            data['stream'] = "stop"
            with open(config_path, 'wb') as file:
                pickle.dump(data, file)
    my_stream = db.child('devices').child(dev_id).child('action').stream(my_stream_handler)

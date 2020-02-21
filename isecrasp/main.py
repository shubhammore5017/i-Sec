from my_threads import stream_handler
from my_threads.stream_thread import db
from my_threads import camera_handler
from my_threads import live_stream_handler
from my_threads import config_path, dev_id
from threading import Thread
import time
import socket
import pickle
import os

try:
    from my_threads import sensor_handler
except ImportError:
    pass


def isconnected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


while True:
    if not isconnected():
        pass
    elif isconnected():
        break
    else:
        pass

getData = db.child('devices').child(dev_id).get()

while True:
    print(getData.val())
    if getData.val() is None:
        data = {'action': {'current': 'Null'}, 'address': {'ip': None},
                'config': {'security_status': False,
                           'threat_status': False}, 'activation': {'activated': 'False', 'token': 0}}
        db.child('devices').child(dev_id).set(data)
        getData = db.child('devices').child(dev_id).get()
    elif getData.val()['activation']['activated'] == True:
        break
    elif getData.val()['activation']['activated'] == 'False':
        getData = db.child('devices').child(dev_id).get()
        pass
    else:
        pass

print('initializing configuration')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
with open(config_path, 'wb') as f:
    config_var = {
        'Security_Status': False,
        'ip': ip,
        'threat_status': False,
        'first_frame': None,
        'stream': False
    }
    pickle.dump(config_var, f)
db.child('devices').child(dev_id).child('address').set({'ip': ip})
print('starting stream thread')
stream_thread = Thread(name='stream-thread', target=stream_handler)
stream_thread.daemon = True
stream_thread.start()
print('stream thread started')
try:
    print('staring sensor thread')
    sensor_thread = Thread(name='sensor-thread', target=sensor_handler)
    sensor_thread.daemon = True
    sensor_thread.start()
    print('sensor thread started')
except Exception:
    print('unable to start')
print('starting camera thread')
camera_thread = Thread(name='camera-thread', target=camera_handler)
camera_thread.daemon = True
camera_thread.start()
print('camera thread started')
print('starting live stream thread')
live_stream_thread = Thread(name='live-thread', target=live_stream_handler)
live_stream_thread.daemon = True
live_stream_thread.start()
print('live stream thread started')
while True:
    time.sleep(100)

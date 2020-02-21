import time
from signal import pause
from gpiozero import MotionSensor
import pickle
import subprocess
import os
from .variables import config_path, dtthreads_path

pir = MotionSensor(23)
time.sleep(3)


def sensor_handler():
    previous = None
    while True:
        try:
            with open(config_path, 'rb') as f:
                data = pickle.load(f)
                print(data['Security_Status'], data['threat_status'], pir.motion_detected)
                print()
        except :
            continue
        if data['Security_Status'] and not data['threat_status'] and pir.motion_detected:
            try:
                with open(config_path, 'wb') as g:
                    data['threat_status'] = True
                    pickle.dump(data, g)
                if previous is None:
                    os.system('python3 '+'{} ALERT'.format(dtthreads_path))
                    previous = time.time() + 120
                elif previous > time.time():
                    pass
                elif time.time() > previous:
                    os.system('python3 ' + '{} ALERT'.format(dtthreads_path))
                    previous = time.time() + 120
            except :
                continue
        time.sleep(0.1)

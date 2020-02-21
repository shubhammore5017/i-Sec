import cv2
import time
import pickle
import subprocess
import os
from .variables import config_path, temp_path, dtthreads_path


def camera_handler():
    while True:
        try:
            with open(config_path, 'rb') as file:
                data = pickle.load(file)
        except:
            continue
        if data['Security_Status'] and data['threat_status']:
            static_back = None
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if static_back is None:
                bkc = data['first_frame']
                bkc_gray = cv2.cvtColor(bkc, cv2.COLOR_BGR2GRAY)
                bkc_gray = cv2.GaussianBlur(bkc_gray, (21, 21), 0)
                static_back = bkc_gray
            diff_fram = cv2.absdiff(static_back, gray)
            thresh_frame = cv2.threshold(diff_fram, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for countour in cnts:
                if cv2.contourArea(countour) < 10000:
                    continue
                (x, y, w, h) = cv2.boundingRect(countour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imwrite('{}/out.png'.format(temp_path), frame)
            cam.release()
            subprocess.Popen(['python3', dtthreads_path, 'IMG'])
            data['threat_status'] = False
            try:
                with open(config_path, 'wb') as file:
                    pickle.dump(data, file)
            except:
                continue
        time.sleep(1)

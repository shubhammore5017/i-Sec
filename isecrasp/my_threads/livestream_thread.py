import os
from subprocess import Popen, PIPE
import time
from .variables import config_path, dev_id, passwd
import pickle
import signal


def live_stream_handler():
    while True:
        try:
            with open(config_path, 'rb') as file:
                data = pickle.load(file)
        except:
            continue
        if data['stream'] is True:
            print('starting')
            command = 'service mjpeg-streamer start'.split()
            p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
            sudo_prompt = p.communicate(passwd + '\n')[1]
            proc = Popen(['ssh', '-R', dev_id + ':80:localhost:8080', 'serveo.net'])
            data['stream'] = "wait"
            with open(config_path, 'wb') as file:
                pickle.dump(data, file)
        elif data['stream'] == "stop":
            try:
                data['stream'] = False
                with open(config_path, 'wb') as file:
                    pickle.dump(data, file)
                proc.send_signal(signal.SIGINT)
                command = 'service mjpeg-streamer stop'.split()
                p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
                sudo_prompt = p.communicate(passwd + '\n')[1]
            except:
                continue
        elif not data['stream']:
            continue
        time.sleep(0.1)

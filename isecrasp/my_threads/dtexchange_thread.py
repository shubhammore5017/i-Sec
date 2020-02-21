import pickle
import os
import sys
import requests
from variables import temp_path, config_path, dev_id

url = "https://i-sec.cf/api/raspapi/{}/{}"


ftype = sys.argv[1]

if ftype == 'IMG':
    mfile = open('{}/out.png'.format(temp_path), 'rb')
    files = {'file': mfile}
    requests.post(url.format(dev_id, 'IMG'), files=files)
    os.remove('{}/out.png'.format(temp_path))
elif ftype == 'ALERT':
    print('giving alert')
    requests.post('https://i-sec.cf/api/alert/{}'.format(dev_id))
elif ftype == 'QP':
    mfile = open('{}/out.png'.format(temp_path), 'rb')
    files = {'file': mfile}
    requests.post(url.format(dev_id, 'QP'), files=files)
    os.remove('{}/out.png'.format(temp_path))



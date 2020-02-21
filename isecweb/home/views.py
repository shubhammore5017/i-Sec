from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Device
import pyrebase
import json
from django.contrib import messages
from secrets import token_hex
from base64 import b64encode
import pyqrcode
from api.models import Chat_Logs, files
import os
# directory = os.getenv('firebaseconfig.json')
with open('firebaseconfig.json') as f:
    config = f.read()
config = json.loads(config)
firebase = pyrebase.initialize_app(config)

db = firebase.database()


def dev_reg_test(user):
	b = user.device_set.all().count()
	if b == 0:
		return False
	else:
		return True

def index(request):
    return render(request, 'home/index.html')


@login_required(login_url='/auth/')
@user_passes_test(dev_reg_test, login_url='/devreg/')
def home(request):
    return render(request, 'home/home.html')
    # return render(request)

@login_required(login_url='/auth/')
@user_passes_test(dev_reg_test, login_url='/devreg/')
def telegram_reg(request):
	

	data = Device.objects.filter(user=request.user).get()
	if request.method == "POST":
		number = request.POST.get('number')
		data.mobile_number = number
		data.save()
		return redirect('home-page')
	image = pyqrcode.create(data.dev_reg_id)
	image.png(request.user.username+'.png', scale=8)
	with open(request.user.username+'.png', 'rb') as f:
		image = f.read()
	image = b64encode(image)
	image = image.decode('utf-8')
	mime = "image/png"
	uri = "data:%s;base64,%s" % (mime, image)
	context = {'uri': uri}
	return render(request, 'home/telegram_reg.html', context)


def dev_reg(request):
	if dev_reg_test(request.user) == True:
		return redirect('home-page')
	if request.method == "POST":
		id = request.POST.get('devid')
		response = db.child('devices').child(id).get()
		if response.val() is None:
			messages.warning(request, 'Invalid Device Id')
		else:
			token = token_hex(16)
			db.child('devices').child(id).child('activation').update({"activated":True, "token":token})
			Device.objects.create(user=request.user, dev_id=id, dev_reg_id=token).save()
			messages.success(request, 'Device Successfully Registered')
			return redirect('home-page')
	return render(request, 'home/dev_reg.html')

@login_required(login_url='/auth/')
@user_passes_test(dev_reg_test, login_url='/devreg/')
def chat_logs(request):
	data = Chat_Logs.objects.all()
	context = {'datatables':True, 'data':data}
	return render(request, 'home/chat_logs.html', context)


def media(request):
	device = Device.objects.get(user=request.user)
	img = device.files_set.filter().order_by('-id')
	context = {'img':img}
	return render(request, 'home/images.html', context)
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Chat_Logs, files
from home.models import Device
import telebot
from telebot import types
from io import BytesIO
from PIL import Image
import requests
from pyzbar.pyzbar import decode
import datetime
import os
import requests
import pyrebase
token = '1021159267:...'
bot = telebot.TeleBot(token)
with open('firebaseconfig.json') as f:
    config = f.read()
config = json.loads(config)
firebase = pyrebase.initialize_app(config)
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('...', '...', 'ap-southeast-1')
db = firebase.database()
import urllib

# Create your views here.

def sendmsg(message, number):
    url = "https://www.fast2sms.com/dev/bulk"
    headers = {'authorization': "...",'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
    payload = {'sender_id': 'FSTSMS', 'message': message, 'language': 'english', 'route': 'p', 'numbers': number}
    payload = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    response = requests.request("POST", url, data=payload, headers=headers)
    return response


# def sendmsg(msg, number):
#     request = CommonRequest()
#     request.set_accept_format('json')
#     request.set_domain('sms-intl.ap-southeast-1.aliyuncs.com')
#     request.set_method('POST')
#     request.set_version('2018-05-01')
#     request.set_action_name('SendMessageToGlobe')
#     request.add_query_param('To', '91'+number)
#     request.add_query_param('From', 'Karan JAdhav')
#     request.add_query_param('Message', msg)
#     response = client.do_action(request)

def index(request):
    return HttpResponse('200 ok')

@csrf_exempt
def teleapi(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        update_id = data['update_id']
        message_id = data['message']['message_id']
        from_id = data['message']['from']['id']
        from_name = data['message']['from']['first_name'] + " " +data['message']['from']['last_name']
        markup = types.ReplyKeyboardMarkup()
        qpbtn = types.KeyboardButton('Quick Pic')
        morebtn = types.KeyboardButton('More -->')
        actbtn = types.KeyboardButton('Activate Seccurity')
        deactbtn = types.KeyboardButton('DeActivate Security')
        backbtn = types.KeyboardButton('<-- Back')
        if 'text' in data['message']:
            text = data['message']['text']
            if text == '/start':
                msg = 'Send The Qr Code To Connect....'                
                bot.send_message(chat_id=from_id, text=msg , reply_to_message_id=message_id)    
            elif text == '':
                pass
            elif text == 'Quick Pic':
                device = Device.objects.get(telegram_id=from_id)
                db.child('devices').child(device.dev_id).child("action").update({"current": "qp"})
                markup.add(qpbtn, morebtn)
                bot.send_message(chat_id=from_id, text="You Will Receive Pic Soon." , reply_to_message_id=message_id, reply_markup=markup)
                chat_logs = Chat_Logs.objects.create(update_id=update_id, message_id=message_id, from_id=from_id, text=text, tele_user=from_name)
                chat_logs.save()
                db.child('devices').child(device.dev_id).child("action").update({"current": "Null"})
            elif text == 'Activate Seccurity':
                device = Device.objects.get(telegram_id=from_id)
                db.child('devices').child(device.dev_id).child("action").update({"current": "activate_security"})
                markup.add(backbtn)
                bot.send_message(chat_id=from_id, text="Security Activated" , reply_to_message_id=message_id, reply_markup=markup)
                chat_logs = Chat_Logs.objects.create(update_id=update_id, message_id=message_id, from_id=from_id, text=text, tele_user=from_name)
                chat_logs.save()
                db.child('devices').child(device.dev_id).child("action").update({"current": "Null"})
                db.child('devices').child(device.dev_id).child("config").update({"security_status": True})
            elif text == 'DeActivate Security':
                device = Device.objects.get(telegram_id=from_id)
                db.child('devices').child(device.dev_id).child("action").update({"current": "disable_security"})
                markup.add(backbtn)
                bot.send_message(chat_id=from_id, text="Security DeActivated" , reply_to_message_id=message_id, reply_markup=markup)
                chat_logs = Chat_Logs.objects.create(update_id=update_id, message_id=message_id, from_id=from_id, text=text, tele_user=from_name)
                chat_logs.save()
                db.child('devices').child(device.dev_id).child("action").update({"current": "Null"})
                db.child('devices').child(device.dev_id).child("config").update({"security_status": False})
            elif text == 'More -->':
                device = Device.objects.get(telegram_id=from_id)
                resp = dict(db.child('devices').child(device.dev_id).get().val())
                # bot.send_message(chat_id=from_id, text=str(resp) , reply_to_message_id=message_id)
                if resp['config']['security_status'] == False:
                    markup.add(actbtn, backbtn)
                    bot.send_message(chat_id=from_id, text="Here Are Some More Options" , reply_to_message_id=message_id, reply_markup=markup)
                else:                    
                    markup.add(deactbtn, backbtn)
                    bot.send_message(chat_id=from_id, text="Here are Some More Options" , reply_to_message_id=message_id, reply_markup=markup)
            elif text == "<-- Back":
                markup.add(qpbtn, morebtn)
                bot.send_message(chat_id=from_id, text="At Home VIew" , reply_to_message_id=message_id, reply_markup=markup)                
            else:
                chat_logs = Chat_Logs.objects.create(update_id=update_id, message_id=message_id, from_id=from_id, text=text, tele_user=from_name)
                chat_logs.save()
                bot.send_message(chat_id=from_id, text='i replied to the text: '+text , reply_to_message_id=message_id)
        elif 'photo' in data['message']:
            path = bot.get_file(data['message']['photo'][1]['file_id'])
            path = path.file_path
            url = 'https://api.telegram.org/file/bot{}/{}'.format(token, path)
            bytecode = requests.get(url)
            img = Image.open(BytesIO(bytecode.content))
            try:
                qr = decode(img)
                data = qr[0][0]
                data = data.decode("utf-8")
                sel_dev = Device.objects.filter(dev_reg_id=data).get()
                if sel_dev.telegram_id == 0:
                    sel_dev.telegram_id = int(from_id)
                    sel_dev.save()
                    markup.add(qpbtn, morebtn)
                    bot.send_message(chat_id=from_id, text='data saved' , reply_to_message_id=message_id)
                    msg = 'You Are Connected As User: {}'.format(sel_dev.user.username)
                    bot.send_message(chat_id=from_id, text=msg , reply_to_message_id=message_id, reply_markup=markup)
                else:
                    bot.send_message(chat_id=from_id, text='Your Account Is already Registered' , reply_to_message_id=message_id)                    
            except:     
                bot.send_message(chat_id=from_id, text='Send A Valid QR code' , reply_to_message_id=message_id)
        else:
            pass
        return HttpResponse('200 ok')
    else:
        return HttpResponse('Only POST request Allowed')

@csrf_exempt
def receive(request, devid, ftype):
    if request.method == 'POST':
        if ftype == 'IMG':
            device = Device.objects.get(dev_id=devid)
            bot.send_photo(device.telegram_id, request.FILES['file'])
            # save_file = files.objects.create(device=device, media=request.FILES['file'])
            # filepath = 'storage/'+devid+'/images/'+str(datetime.datetime.now())+'.png'
            # with open(filepath, 'wb') as f:
                # f.write(request.FILES['file'].read())
            device.files_set.create(media=request.FILES['file'])
            device.save()
            return HttpResponse('ok')
        if ftype == 'QP':
            device = Device.objects.get(dev_id=devid)
            bot.send_photo(device.telegram_id, request.FILES['file'])
            # filepath = 'storage/'+devid+'/images/'+str(datetime.datetime.now())+'.png'
            # with open(filepath, 'wb') as f:
                # f.write(request.FILES['file'].read())
            device.files_set.create(media=request.FILES['file'])
            device.save()
            return HttpResponse('ok')
    else:
        return HttpResponse('Only POST request allowed')

@csrf_exempt
def alert(request, devid):
    if request.method == "POST":
        device = Device.objects.get(dev_id=devid)
        uid = device.telegram_id
        # markup = telebot.types.ReplyKeyboardMarkup()
        # btn1 = telebot.types.KeyboardButton('')
        # markup.add(btn1)
        sendmsg("ALERT: Someone is in Your HOME", device.mobile_number)
        bot.send_message(uid, "ALERT: Someone is in Your HOME")
        return HttpResponse('done')
    else:
        return HttpResponse('only post request allowed')

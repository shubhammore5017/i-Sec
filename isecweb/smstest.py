#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('<accessKeyId>', '<accessSecret>', 'ap-southeast-1')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('sms-intl.ap-southeast-1.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2018-05-01')
request.set_action_name('SendMessageToGlobe')

request.add_query_param('RegionId', "ap-southeast-1")

response = client.do_action(request)
# python2:  print(response) 
print(str(response, encoding = 'utf-8'))


from django.db import models
from home.models import Device
# Create your models here.

class Chat_Logs(models.Model):
    update_id = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    message_id = models.IntegerField()
    from_id = models.IntegerField()
    tele_user = models.CharField(max_length=200)
    text = models.CharField(blank=True, null=True, max_length=200)

class files(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    media = models.ImageField(upload_to='images/')
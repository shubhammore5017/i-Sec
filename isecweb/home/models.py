from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dev_id = models.CharField(max_length=200)
    dev_reg_id = models.CharField(max_length=200)
    telegram_id = models.IntegerField(default=0)
    mobile_number = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username




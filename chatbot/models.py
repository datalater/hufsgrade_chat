from __future__ import unicode_literals
from django.db import models

# Create your models here.
class kakao_user(models.Model):

    user_key = models.CharField(max_length=50)
    step = models.IntegerField(default=0)
    hufs_id = models.CharField(max_length=25)
    hufs_pwd = models.CharField(max_length=50)

    def __str__(self):
        return self.user_key

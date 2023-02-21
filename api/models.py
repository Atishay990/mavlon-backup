from datetime import datetime
import django
from django.db import models
from django.contrib.auth.models import User

class SalesforceData(models.Model):
    userid = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200, null=True)
    refresh_token = models.CharField(max_length=200, null=True)
    instance_url = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank = True)

    def __str__(self):
        return "%s" % (self.userid)

class EmailTrack(models.Model):
    user_detail = models.ForeignKey(SalesforceData,on_delete=models.CASCADE, default=123)
    email_uid = models.CharField(max_length=500,primary_key = True)
    to = models.EmailField(blank = True, null=True)
    subject = models.CharField(max_length=500,null=True,blank =True)
    clicks = models.IntegerField(default = 0)
    
    def __str__(self):
        return "%s" % (self.subject)

class EmailLinkTrack(models.Model):
    email_track = models.ForeignKey(EmailTrack,on_delete = models.CASCADE,default=123)
    link_name = models.CharField(max_length=500)
    link_clicks = models.IntegerField(default = 0)
    clickedAt = models.DateTimeField(default = django.utils.timezone.now)


    def __str__(self):
        return "%s" % (self.link_name)


class EventData(models.Model):
    user_detail = models.ForeignKey(SalesforceData,on_delete=models.CASCADE, default=123)
    status =  link = models.CharField(max_length=500,null=True,blank = True)
    email_uid = models.CharField(max_length=500, blank = True, null = True)
    to = models.EmailField(blank = True, null=True)
    subject = models.CharField(max_length=500,null=True,blank = True)
    city = models.CharField(max_length=500,null=True,blank = True)
    region = models.CharField(max_length=500,null=True,blank = True)
    country = models.CharField(max_length=500,null=True,blank = True)
    openAt = models.DateTimeField(default = django.utils.timezone.now)
    link = models.CharField(max_length=500,null=True,blank = True)
    valid = models.IntegerField(default = 1)
    def __str__(self):
        return "%s" % (self.subject)

    
from django.http import HttpResponse
from rest_framework import viewsets, views
import base64
from rest_framework import viewsets, views
from pytracking import Configuration
from pytracking.django import OpenTrackingView, ClickTrackingView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.shortcuts import redirect,render
from api.models import EmailTrack, EmailLinkTrack, EventData
from django.contrib.auth.models import User
from api.models import SalesforceData
import json
import requests
import base64
from rest_framework.permissions import IsAuthenticated
from django.core import serializers

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def trackingPixelhook(request):
    data = json.loads(request.body)
    print(data)
    userid = data['userId']
    ip = data['context']['ip']
    user_profile = SalesforceData.objects.filter(userid = userid)[0]
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()

    if EmailTrack.objects.filter(email_uid = data['properties']['email_uid']).exists():
        email_track = EmailTrack.objects.filter(email_uid = data['properties']['email_uid'])[0]
        
        event_data = EventData()
        event_data.user_detail = user_profile
        event_data.status = 'open'
        event_data.email_uid = data['properties']['email_uid']
        event_data.to = data['properties']['email']
        event_data.subject = data['properties']['subject']
        event_data.city = response.get("city")
        event_data.region = response.get("region")
        event_data.country = response.get("country_name")
        event_data.openAt = data['receivedAt']
        if(email_track.clicks==0):
            event_data.valid = 0
        
        event_data.save()
        EmailTrack.objects.filter(email_uid = data['properties']['email_uid']).update(to=data['properties']['email'],subject = data['properties']['subject'],clicks= email_track.clicks+1)
      
        

    else:
        return HttpResponse("Email data not found in DB")
    return HttpResponse("Email opened")

def trackingLinkClick(request):
    base64_string =request.GET['data']
    base64_bytes = base64_string.encode("ascii")
  
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    data = json.loads(sample_string)
    url = data['url']
    uid = data['uid']
    userid = data['userid']
    email_track = EmailTrack.objects.filter(email_uid = uid)[0]
    user_profile = SalesforceData.objects.filter(userid = userid)[0]
    if EmailLinkTrack.objects.filter(email_track = email_track,link_name = url).exists():
        l = EmailLinkTrack.objects.filter(email_track = email_track,link_name = url)[0]
        EmailLinkTrack.objects.filter(email_track = email_track,link_name = url).update(link_clicks = l.link_clicks+1)
    else:
        l = EmailLinkTrack()
        l.email_track = email_track
        l.link_name = url
        l.link_clicks = 1 
        l.save()
    event_data = EventData()
    event_data.user_detail = user_profile
    event_data.email_uid = uid
    event_data.to = data['to']
    event_data.subject = data['subject']
    event_data.status = 'click'
    event_data.link = url
    event_data.save()

    print("link tracked, user clicked on link = "+ url)
    response = redirect(url)
    return response



class EventView(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self,request):
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        events = EventData.objects.filter(user_detail = user, valid = 1).order_by('-openAt')
        data = serializers.serialize('json', events)
        return Response(data)

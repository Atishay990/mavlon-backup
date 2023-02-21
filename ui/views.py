from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, views
import base64
from django.conf import settings
from rest_framework import viewsets, views
from django.core import serializers
from api.models import EventData
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
from api.models import EmailTrack, EmailLinkTrack
from django.contrib.auth.models import User
from api.models import SalesforceData
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from microsoft_authentication.auth.auth_decorators import microsoft_login_required
import json
import requests
from django.contrib.auth.decorators import login_required
from microsoft_authentication.auth.auth_utils import (
    get_token_from_code,
    get_user,
)
from django.contrib.auth import login, authenticate, logout
from django.db.models import Sum

@microsoft_login_required()
def index(request):
    print("Email dashboard page")
    user = User.objects.get(email = request.user.email)
    if not SalesforceData.objects.filter(user=user).exists():
        return render(request,'ui/welcome.html')

    user_profile = SalesforceData.objects.filter(user=user)[0]
    events = EmailTrack.objects.filter(user_detail = user_profile,clicks__gt = 1)
    link_click_events = EmailLinkTrack.objects.filter(email_track__user_detail= user_profile)
    print(link_click_events)
    clicks = []
    opens = []
    for event in events:
        opens.append(event)
        clicked = EmailLinkTrack.objects.filter(email_track = event).aggregate(Sum('link_clicks'))
        clicks.append(clicked['link_clicks__sum'])
    
    data = zip(opens,clicks)
    return render(request,'ui/index.html',{'data':data,'click_events':link_click_events})


def auth(request):
    # data = serializers.serialize('json', events)
    if request.user.is_authenticated:
        return redirect('index')
    return render(request,'ui/sign-in.html')
    
@microsoft_login_required()
def home(request):
    # data = serializers.serialize('json', events)
    return render(request,'ui/index.html')


def loginSuccessful(request):
    print("iske andaya ayaaaaaaaaaaaaaaa")
    result = get_token_from_code(request)
    ms_user = get_user(result['access_token'])
    email = ms_user['userPrincipalName']
    firstName = ms_user['givenName']
    lastName = ms_user['surname']
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        user = User(username=email, email=email, first_name = firstName, last_name = lastName)
        user.save()

    login(request, user)

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL or "/admin")


def logout_view(request):
    logout(request)
    return redirect('auth')

@microsoft_login_required()
def salesforce_connected(request):
      return render(request,'ui/salesforce.html')
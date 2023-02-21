from rest_framework import viewsets, views
from rest_framework.response import Response
from api.serializers import AccountSerializer, LeadSerializer, EmailSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.conf import settings


from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from salesforce_oauth.utils import get_or_create_user
from datetime import datetime, tzinfo

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count

from salesforce_oauth.oauth import OAuth
from rest_framework.permissions import IsAuthenticated
from urllib.parse import urlparse, parse_qs
from django.http import JsonResponse
from api.models import SalesforceData, EmailTrack
import http
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
import msal
import requests
import string
import random
from microsoft_authentication.auth.auth_utils import (
    get_token_from_code,
    get_user,
)
import json
import base64
import uuid

def home(request):
    return render(request, "index.html")

class getEncodedToken(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self,request,subject,to):
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        data = {}
        data['writeKey'] = 'ncJhD4vvyYFYu4p1JFwpYV0gCBJAhS5G'
        # data['email_uid'] = str(uuid.uuid4())
        data['event'] = 'Email_Opened'
        data['userId'] = user.userid

        properties = {}
        properties['subject'] = subject
        properties['email'] = to
        properties['email_uid'] = str(uuid.uuid4())

        data['properties'] = properties

        jsonData = json.dumps(data)
        encoded = base64.b64encode(jsonData.encode('utf-8')) 
        e = EmailTrack()
        e.email_uid = properties['email_uid']
        e.user_detail = user
        e.save()
        return Response({"data":encoded,"uid":properties['email_uid']})



def microsoft_callback(request):
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




class getNewToken(views.APIView):
    def get(self, request, userid):
        refresh_token = (SalesforceData.objects.filter(userid=userid)[0]).refresh_token
        url = f"https://login.salesforce.com/services/oauth2/token"

        data = {
            "client_id": settings.SFDC_CONSUMER_KEY,
            "client_secret": settings.SFDC_CONSUMER_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = requests.post(url, data)
        SalesforceData.objects.filter(userid=userid).update(
            access_token=response.json()["access_token"]
        )
        return Response("Access token updated")



class LeadView(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, email):
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        endpoint = user.instance_url + "/services/data/v55.0/query?q=select id,email, firstname, lastname, company from lead where email='"+email+"' " 
        headers = {"Authorization": "Bearer " + user.access_token}
        res = requests.get(endpoint, headers=headers)
        print(res.json())
        return Response(res.json())

    def post(self, request, email):
        data = request.data
        # result = LeadSerializer(data).data
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        endpoint = user.instance_url + "/services/data/v55.0/sobjects/Lead"
        headers = {"Authorization": "Bearer " + user.access_token}
        res = requests.post(endpoint, headers=headers, json=data)
        return Response(res.json())

class ContactView(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, email):
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        endpoint = user.instance_url + "/services/data/v55.0/query?q=select id,email,firstname,lastname from contact where email='"+email+"' " 
        headers = {"Authorization": "Bearer " + user.access_token}
        res = requests.get(endpoint, headers=headers)
        print(res.json())
        return Response(res.json())

    def post(self, request, email):
        data = request.data
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        endpoint = user.instance_url + "/services/data/v55.0/sobjects/Contact"
        headers = {"Authorization": "Bearer " + user.access_token}
        res = requests.post(endpoint, headers=headers, json=data)
        return Response(res.json())

class AccountView(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, website):
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        endpoint = user.instance_url + "/services/data/v55.0/query?q=select id,website,name from account where website='"+website+"' " 
        headers = {"Authorization": "Bearer " + user.access_token}
        res = requests.get(endpoint, headers=headers)
        print(res.json())
        return Response(res.json())

    def post(self, request, website):
        data = request.data
        print(data)
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        endpoint = user.instance_url + "/services/data/v55.0/sobjects/Account"
        headers = {"Authorization": "Bearer " + user.access_token}
        res = requests.post(endpoint, headers=headers, json=data)
        return Response(res.json())


class EmailView(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request):
        data = {"name": "atishay"}
        results = AccountSerializer(data).data
        return Response(results)

    def post(self, request, type):
  
        data = json.loads(request.body.decode('utf-8'))
   
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        # token = '00D5i00000890uq!ARgAQI0TAUStfmL678xwQLepddDcVvQ4IiX6VVUlpuVOaAPACn1gy.xj2xiLoUyyI5D4i37Qrae_ZO.U_0dQ6pmJQvhmu8Wg'
        user = SalesforceData.objects.filter(access_token=token)[0]
        headers = {"Authorization": "Bearer " + user.access_token}
        if data["Incoming"] == True:
            fromId = data["from"]
            url = (
            user.instance_url
            + f"/services/data/v55.0/query?q=select Id from {type} where email='{fromId}'"
            )
         
            res = requests.get(url, headers=headers)
            print(res.json())
            fromId = res.json()["records"][0]["Id"]
            data.pop("from")
            url = user.instance_url + f"/services/data/v55.0/sobjects/EmailMessage/"
            res = requests.post(url, headers=headers, json=data)
            emailMessageId = res.json()["id"]

            emailMessageRelation = {
                "EmailMessageId": emailMessageId,
                "RelationId": fromId,
                "RelationType": "FromAddress",
            }
            url = (
                user.instance_url
                + f"/services/data/v55.0/sobjects/EmailMessageRelation/"
            )
            res = requests.post(url, headers=headers, json=emailMessageRelation)
            emailMessageStatusUpdate = {"Status": 1}
            url = (
                user.instance_url
                + f"/services/data/v55.0/sobjects/EmailMessage/{emailMessageId}/"
            )
            res = requests.patch(url, headers=headers, json=emailMessageStatusUpdate)

        else:
            toId = data["to"]
            url = (
                user.instance_url
                + f"/services/data/v55.0/query?q=select Id from {type} where email='{toId}'"
            )

            res = requests.get(url, headers=headers)
            toId = res.json()["records"][0]["Id"]
            arraylist = [toId]
            data.pop("to")
            data["ToIds"] = arraylist
            url = user.instance_url + f"/services/data/v55.0/sobjects/EmailMessage/"
            res = requests.post(url, headers=headers, json=data)
            emailMessageId = res.json()["id"]

            emailMessageRelation = {
                "EmailMessageId": emailMessageId,
                "RelationId": user.userid,
                "RelationType": "FromAddress",
            }
            url = (
                user.instance_url
                + f"/services/data/v55.0/sobjects/EmailMessageRelation/"
            )
            res = requests.post(url, headers=headers, json=emailMessageRelation)
            emailMessageStatusUpdate = {"Status": 3}
            url = (
                user.instance_url
                + f"/services/data/v55.0/sobjects/EmailMessage/{emailMessageId}/"
            )
            res = requests.patch(url, headers=headers, json=emailMessageStatusUpdate)
        
        return Response("Saved Successfully")

        

class EmailAccountView(views.APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        token = (request.META.get('HTTP_AUTHORIZATION')).split(' ')[1]
        user = SalesforceData.objects.filter(access_token=token)[0]
        headers = {"Authorization": "Bearer " + user.access_token}
        url = user.instance_url + f"/services/data/v55.0/sobjects/EmailMessage/"
        res = requests.post(url, headers=headers, json=data)
        return Response("Saved Successfully")
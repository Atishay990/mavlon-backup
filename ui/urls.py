from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf import settings

urlpatterns = [
    path("", views.index, name='index'),
    path("auth/", views.auth, name='auth'),
    path("home/",views.home,name = 'home_view'),
    path("login-successful",views.loginSuccessful,name = "login_successful"),
    path("logout/",views.logout_view,name = "logout_view"),
    path("salesforce-connected/",views.salesforce_connected,name = "salesforce_connected")
]

urlpatterns += static((settings.STATIC_URL), document_root=(settings.STATIC_ROOT))
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static((settings.MEDIA_URL), document_root=(settings.MEDIA_ROOT))
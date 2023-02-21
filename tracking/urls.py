from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("hook/", views.trackingPixelhook, name='tracking_pixel_hook'),
    path("link/", views.trackingLinkClick, name='tracking_link_click'),
    path("view/", views.EventView.as_view()),

]


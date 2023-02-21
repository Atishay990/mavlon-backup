from django.urls import include, path

from rest_framework import routers

from api.views import AccountView, LeadView, getNewToken, EmailView, ContactView, getEncodedToken, EmailAccountView
from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("account/<str:website>/", AccountView.as_view()),
    path("lead/<str:email>/", LeadView.as_view()),
    path("contact/<str:email>/", ContactView.as_view()),
    path("home/", views.home, name="home"),
    path("get-token/<str:userid>/", getNewToken.as_view()),
    path("email/<str:type>/", EmailView.as_view()),
    path("email-account/", EmailAccountView.as_view()),
    path("test/", views.microsoft_callback, name="callback"),
    path("email-token/<str:subject>/<str:to>/", getEncodedToken.as_view()),
]

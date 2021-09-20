from django.urls import path

from oauthapp.views import auth, tokenauth, signin, get_my

urlpatterns = [
    path('grant/', auth, name='grants'),
    path('tokenauth/', tokenauth, name='toen'),
    path('signin/', signin, name='signin'),
    path('about/', get_my, name='about')
]
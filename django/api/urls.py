from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # ex: /api/upload
    path('upload', views.upload, name='upload'),
    path('token-auth', obtain_auth_token, name='api_token_auth'),
]


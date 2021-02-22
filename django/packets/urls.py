from django.urls import path

from . import views

urlpatterns = [
    # ex: /environments/
    path('', views.index, name='index'),
    # ex: /environments/login
    path('login', views.user_login, name='user_login'),
    # ex: /environments/logout
    path('logout', views.logout_view, name='logout_view'),
    # ex: /environments/departamento
    path('<str:env>', views.environment, name='environment'),
    # ex: /environments/departamento/stats
    path('<str:env>/stats', views.stats, name='stats'),
    # ex: /environments/departamento/mac/nomemac
    path('<str:env>/mac/<str:mac>', views.mac, name='mac'),
    # ex: /environments/departamento/mac/nomemac/stats
    path('<str:env>/mac/<str:mac>/stats', views.stats_mac, name='stats_mac'),
    # ex: /environments/departamento/protocol/nomeprotocolo
    path('<str:env>/protocol/<str:protocol>', views.protocol, name='protocol'),
    # ex: /environments/departamento/mac/nomemac/protocol/nomeprotocolo
    path('<str:env>/mac/<str:mac>/protocol/<str:protocol>', views.packets, name='packets'),
]


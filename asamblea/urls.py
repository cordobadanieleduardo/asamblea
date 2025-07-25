from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    # path('user/',UserView.as_view(), name='user_list'),
    path('activar/<uidb64>/<token>/', activar_cuenta, name='activar_cuenta'),
    # path('enviar/', enviar_email_activacion, name='enviar_cuenta'),
    path('accounts/password/change/first-login/', FirstLoginPasswordChangeView.as_view(), name='password_change_first_login'),
    path('subir-csv/', subir_csv, name='subir_csv'),
    path('votar/', votar, name='votar'),
    path('resultado/', resultado, name='resultado'),
]

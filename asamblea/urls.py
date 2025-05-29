from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import *

urlpatterns = [
    path('user/',UserView.as_view(), name='categoria_list'),
    # path('categorias/new',CategoriaNew.as_view(), name='categoria_new'),
    # path('categorias/edit/<int:pk>',CategoriaEdit.as_view(), name='categoria_edit'),
    # path('categorias/delete/<int:pk>',CategoriaDel.as_view(), name='categoria_del'),
    path('activar/<uidb64>/<token>/', activar_cuenta, name='activar_cuenta'),
    path('enviar/', enviar_email_activacion, name='enviar_cuenta'),
    # path('password_change/', password_change, name='password_change'),
    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password/change/first-login/', FirstLoginPasswordChangeView.as_view(), name='password_change_first_login'),   
    # path("accounts/", include("django.contrib.auth.urls")),
    # path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/password/change/first-login/', FirstLoginPasswordChangeView.as_view(), name='password_change_first_login'),


]
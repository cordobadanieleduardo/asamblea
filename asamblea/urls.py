from django.urls import path

from .views import *

urlpatterns = [
    path('user/',UserView.as_view(), name='categoria_list'),
    # path('categorias/new',CategoriaNew.as_view(), name='categoria_new'),
    # path('categorias/edit/<int:pk>',CategoriaEdit.as_view(), name='categoria_edit'),
    # path('categorias/delete/<int:pk>',CategoriaDel.as_view(), name='categoria_del'),
    path('activar/<uidb64>/<token>/', activar_cuenta, name='activar_cuenta'),
    path('enviar/', enviar_email_activacion, name='enviar_cuenta'),
]
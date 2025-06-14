from django.db import models

from django.conf import settings

# from django.contrib.auth.models import User
# from django_userforeignkey.models.fields import UserForeignKey


class ClaseModelo(models.Model):
    # Borrado logico
    estado = models.BooleanField(default=True)
    # FECHA CREACION
    fc = models.DateTimeField(auto_now_add=True, verbose_name='F. creación')
    # FECHA CREACION
    fm = models.DateTimeField(auto_now=True, verbose_name='F. modificación')
    # USUARIO CREACION
    uc = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='plancha_usuario', verbose_name='Usuario creación')
    # USUARIO CREACION
    um = models.IntegerField(blank=True,null=True, verbose_name='Usuario creación')

    class Meta:
        abstract=True
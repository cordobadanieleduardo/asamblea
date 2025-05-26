from django.db import models

from django.contrib.auth.models import User
# from django_userforeignkey.models.fields import UserForeignKey


class ClaseModelo(models.Model):
    # Borrado logico
    estado = models.BooleanField(default=True)
    # FECHA CREACION
    fc = models.DateTimeField(auto_now_add=True)
    # FECHA CREACION
    fm = models.DateTimeField(auto_now=True)
    # USUARIO CREACION
    uc = models.ForeignKey(User, on_delete=models.CASCADE)
    # USUARIO CREACION
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract=True
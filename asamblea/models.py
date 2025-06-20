from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from bases.models import ClaseModelo
from django.utils import timezone
from pytz import timezone as pytz_timezone


class Puesto(models.Model):
    comuna_name = models.CharField(max_length=30, verbose_name='Localidad',null=True, blank=True)
    mun_name = models.CharField(max_length=30, verbose_name='Municipio')
    dpto_name = models.CharField(max_length=30, verbose_name='Departamento')
    curulCHOICES=((8,"8"), (14,"14"),(17,"17"),)
    num_curul=models.IntegerField(default=8,choices=curulCHOICES,verbose_name='¿N° Curules?')
    fecha = models.DateTimeField(verbose_name='F. votación',null=True, blank=True)
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de inicio',null=True, blank=True)
    fecha_fin = models.DateTimeField(verbose_name='Fecha cierre',null=True, blank=True)
    
    class Meta:
        verbose_name="Puesto"
        verbose_name_plural="Puestos"

    def __str__(self):
        return f"{self.pk} - {self.dpto_name} - {self.mun_name} - {self.comuna_name}"

class Lista(models.Model):
    name=models.CharField(max_length=120, verbose_name='Nombre')
    mostrar=models.BooleanField(default=True)

    class Meta:
        verbose_name="Lista"
        verbose_name_plural="Listas"
        ordering=['name']

    def __str__(self):
        return f"{self.name}"

class Plancha(ClaseModelo):
    name=models.CharField(max_length=120, verbose_name='Nombre')
    mostrar=models.BooleanField(default=True, verbose_name='Visualizar')
    imagen=models.ImageField(upload_to='opciones_voto/',null=True,blank=True, verbose_name='Imagen')
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Puesto,on_delete=models.CASCADE,null=True,blank=True, verbose_name='Ubicación')

    class Meta:
        verbose_name="Plancha"
        verbose_name_plural="Planchas"
        ordering=['name']

    def __str__(self):
        return f"{self.name} {self.location if self.location else 'No registra' } "

class Voto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Plancha, on_delete=models.CASCADE)
    fecha_voto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','opcion',)  # Evita que un usuario vote más de una vez

    def __str__(self):
        return f"{self.user.username} votó por {self.opcion.name} de {self.opcion.location.dpto_name} {self.opcion.location.mun_name} {self.opcion.location.comuna_name}"

class Militante(AbstractUser):
    username=models.CharField(max_length=12,unique=True)
    email=models.EmailField(max_length=120,unique=True)
    must_change_password=models.BooleanField(default=False, verbose_name='Debe cambiar contraseña')
    plancha=models.ForeignKey(Plancha,on_delete=models.CASCADE,null=True,blank=True)
    send_email=models.BooleanField(default=False, verbose_name='se envió correo')
    list=models.ForeignKey(Lista,on_delete=models.CASCADE,null=True,blank=True, verbose_name='Lista')
    position = models.IntegerField(default=0, verbose_name='Posición')
    gCHOICES=(("M","Masculino"), ("F","Femenino"), ("O","Otro"),)
    sex=models.CharField(max_length=10,choices=gCHOICES,verbose_name='Género',null=True,blank=True)
    location = models.ForeignKey(Puesto,on_delete=models.CASCADE,null=True,blank=True, verbose_name='Ubicación')
    is_active = models.BooleanField(default=False,verbose_name='Es Activo')
    
    class Meta:
        verbose_name_plural="Militantes"
        verbose_name="Militante"
        constraints=[
            models.UniqueConstraint(fields=['username','email'],name='unique_username_email')
        ]

    def save(self, *args, **kwargs):
        self.email = str(self.email.lower()).strip()
        self.first_name = str(self.first_name).strip()
        self.last_name = str(self.last_name).strip()        
        super().save(*args, **kwargs)  # Sin return
    
    def __str__(self):
        return f"{self.username} - {self.email}"

class Registro(models.Model):
    columna1 = models.CharField(max_length=255)
    columna2 = models.IntegerField()
    columna3 = models.CharField()
    # Agrega más campos según tu CSV

    def __str__(self):
        return self.columna1

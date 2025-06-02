from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User,AbstractUser
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.exceptions import ValidationError

from bases.models import ClaseModelo


# Create your models here.

# class UserProfile(models.Model):
#     bio=models.TextField(blank=True)
#     # avatar=models.ImageField(upload_to='avatars/',blank=True,null=True)

#     def __str__(self):
#         return f"Profile of user {self.id}"

class Plancha(ClaseModelo):
    name=models.CharField(max_length=120)
    # email=models.EmailField(max_length=150)
    mostrar=models.BooleanField(default=True)
    imagen=models.ImageField(upload_to='opciones_voto/')
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name="Plancha"
        verbose_name_plural="Planchas"
        ordering=['name']

    def __str__(self):
        return f"{self.name}"

class Voto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Plancha, on_delete=models.CASCADE)
    fecha_voto = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','opcion',)  # Evita que un usuario vote más de una vez

    def __str__(self):
        return f"{self.user.username} votó por {self.opcion.name}"

class Militante(AbstractUser):
    username=models.CharField(max_length=12,unique=True)
    email=models.EmailField(max_length=120,unique=True)
    must_change_password=models.BooleanField(default=False)
    plancha=models.ForeignKey(Plancha,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name_plural="Militantes"
        verbose_name="Militante"
        constraints=[
            models.UniqueConstraint(fields=['username','email'],name='unique_username_email')
        ]

    def __str__(self):
        return f"{self.username} - {self.email}"
        # return f"{self.username} - {self.email} - {" Placha: "+ self.plancha.name if self.plancha.name else " sin plancha"}"
    
    # def clean(self):
    #     # Validación para email (ya lo maneja User por defecto con unique=True)
    #     # Si quieres una validación adicional o un mensaje personalizado,puedes hacerlo aquí
    #     pass


    # def save(self,*args,**kwargs):
    #     pass
    #     # if Militante.objects.filter(username=self.username,email=self.email).exists():
    #     #     raise ValidationError("El número de cédula y email ya está en uso.")
    #     if Militante.objects.filter(username=self.username).exists():
    #         raise ValidationError("El número de cédula ya está en uso.")
    #     if Militante.objects.filter(email=self.email).exists():
    #         raise ValidationError("El correo electrónico ya está en uso.")
    #     ##super().save(*args,**kwargs)

class Registro(models.Model):
    columna1 = models.CharField(max_length=255)
    columna2 = models.IntegerField()
    columna3 = models.CharField()
    # Agrega más campos según tu CSV

    def __str__(self):
        return self.columna1





# class Candidato(ClaseModelo):
#     name=models.CharField(max_length=12)
#     plancha=models.ForeignKey(Plancha,on_delete=models.CASCADE,null=True,blank=True)
        
#     class Meta:
#         verbose_name="candidato"
#         verbose_name_plural="candidatos"
#         ordering=['name']

#     def __str__(self):
#         return self.name

# # Señal para crear/actualizar el perfil cuando se crea/actualiza un usuario
# @receiver(post_save,sender=User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         Militante.objects.create(user=instance)

# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwargs):
#     instance.profile.save()



# class Usuario(models.Model):
#     # Fields
#     #id=models.AutoField(primary_key=True)
#     # username=models.CharField(max_length=12)
#     # email=models.EmailField()
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     MilitanciaCHOICES=(
#         ("Militante","Militante"),
#     )
#     militancia=models.CharField(
#         max_length=10,choices=MilitanciaCHOICES,default="Militante"
#     )
#     # primer_nombre=models.CharField(max_length=100,default=None,null=True)
#     # segundo_nombre=models.CharField(max_length=100,default=None,null=True)
#     # primer_apellido=models.CharField(max_length=100,default=None,null=True)
#     # segundo_apellido=models.CharField(max_length=100,default=None,null=True)
#     tipodoc=models.CharField(max_length=100)
#     documento_identidad=models.CharField(max_length=100)
    
#     # genero=models.CharField(max_length=100,default="",null=True)
#     # identidad_genero=models.CharField(max_length=100,default="",null=True)
#     # orientacion_sexual=models.CharField(max_length=100,default="",null=True)
#     # grupo_etnico=models.CharField(max_length=100,default="",null=True)
#     # grupo_poblacional=models.CharField(max_length=100,default="",null=True)
#     # comision=models.CharField(max_length=100,default="",null=True)
#     # centro_pensamiento=models.CharField(max_length=100,default="",null=True)
#     # telefono=models.CharField(max_length=100,default="",null=True)
#     # email_secundario=models.CharField(max_length=100,default="",null=True)
#     # telefono_secundario=models.CharField(max_length=100,default="",null=True)
#     # twitter=models.CharField(max_length=500,default="",null=True)
#     # facebook=models.CharField(max_length=500,default="",null=True)
#     # instagram=models.CharField(max_length=500,default="",null=True)
#     # otrared=models.CharField(max_length=500,default="",null=True)
#     # fnacimiento=models.DateField(null=True)
#  #   ocupacion=models.ForeignKey('usuarios.Ocupacion',on_delete=models.CASCADE,default=None,null=True)
#     direccion=models.CharField(max_length=255,default="",null=True)
#     pais=models.CharField(max_length=100,default="",null=True)
#     departamento=models.CharField(max_length=100,default="",null=True)
#     municipio=models.CharField(max_length=100,default="",null=True)
#     # cod_departamento=models.CharField(max_length=100,default="",null=True)
#     # cod_municipio=models.CharField(max_length=100,default="",null=True)
#     # comuna=models.CharField(max_length=100,default="",null=True)
#     # cod_comuna=models.CharField(max_length=100,default="",null=True)
#    # circunscripcion=models.ForeignKey("territorio.Circunscripcion",on_delete=models.CASCADE,default=None,null=True)
#     # ver_doc_privado=models.BooleanField(default=False,null=True)
#     # vida_politica=models.TextField(default='[]',null=True)
#     # formacion_academica=models.TextField(default='[]',null=True)
#     # experiencia_laboral=models.TextField(default='[]',null=True)
#     # experiencia_social=models.TextField(default='[]',null=True)
#     # logros_reconocimientos=models.TextField(default='[]',null=True)
#     # antecedentes_penales=models.TextField(default='[]',null=True)
#     # redes=models.TextField(default='[]',null=True)
#     # referencia_personal=models.TextField(default='[]',null=True)
#     # referencia_pav=models.TextField(default='[]',null=True)
#     # renuente_pav=models.BooleanField(default=False,null=True)
#     # inhabilitado=models.BooleanField(default=False,null=True)

#     # def get_full_name(self):
#     #     return self.get_full_name()
#         # return (self.primer_nombre + ' ' if self.primer_nombre else '') + (self.segundo_nombre + ' ' if self.segundo_nombre else '') + (self.primer_apellido + ' ' if self.primer_apellido else '') + (self.segundo_apellido if self.segundo_apellido else '')

#     # def nombre_departamento(self):
#     #     departamentos=Puesto.objects.values_list('cod_dpto','dpto_name').distinct()
#     #     for codigo,nombre in departamentos:
#     #         if str(self.departamento) == codigo:
#     #             return nombre
#     #     return 'Desconocido'exit

#     # def nombre_municipio(self):
#     #     municipios=Puesto.objects.values_list('cod_mun','mun_name').distinct()
#     #     for codigo,nombre in municipios:
#     #         if str(self.municipio) == codigo:
#     #             print(nombre)
#     #             return nombre
#     #     return 'Desconocido'

#     class Meta:
#         verbose_name_plural="Usuarios"
#         verbose_name="Usuario"
#         constraints=[
#             models.UniqueConstraint(fields=['username'],name='unique_username'),
#             models.UniqueConstraint(fields=['email'],name='unique_email'),
#         ]
#     def __str__(self):
#         return str(self.documento_identidad) + "-" + self.get_full_name()
    
#     # def save(self):
#     #     self.direccion=self.direccion.lower()
#     #     super(Usuario,self).save()


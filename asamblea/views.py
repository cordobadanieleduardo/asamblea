import sys

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.db.models import Count, Sum

from django.contrib import messages

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import threading

from django.template import loader
import csv

from .models import Militante
from .forms import *

from bases.views import SinPrivilegios


# class UserView(SinPrivilegios, generic.ListView):
#     # permission_required = "asamblea.view_categoria"
#     model = Militante
#     template_name = "asamblea/user_list.html"
#     context_object_name = "obj"



## Crear una vista para enviar correos de activación

# def enviar_email_activacion(usuario):
#     token = default_token_generator.make_token(usuario)
#     uid = urlsafe_base64_encode(force_bytes(usuario.pk))
#     # print('Usuario no encontrado.....', usuario)
#     # print('Usuario no encontrado.....', usuario.last_login)
    
#     # try:
#     #     user = get_object_or_404(Militante, pk=usuario.pk)
#     # except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#     #     user = None
#     #     print('Usuario no encontrado', user)
    
#     # print('Usser', usuario)
        
#     if usuario is not None:
#         # deactivar flag en el perfil
#         # usuario.is_active = False
#         usuario.send_email = True
#         usuario.save()
        
#         # print("guardó", usuario)
    
#     activate_url = f"http://{settings.DOMINIO}{reverse('asamblea:activar_cuenta', kwargs={'uidb64': uid, 'token': token})}"
#     user_display = usuario.email

#     # mensaje = f"Hola {usuario.username}, activa tu cuenta haciendo clic en el siguiente enlace: {activate_url}"

#     # send_mail(
#     #     'Activa tu cuenta',
#     #     mensaje,
#     #     'desarrollotecnologico@partidoverde.org.co',  # Remitente
#     #     [usuario.email],  # Destinatario
#     #     fail_silently=False,
#     # )

#     # from_email_user = settings.EMAIL_HOST_USER
#     # to_email = usuario.email
#     context={'user_display': user_display, 'activate_url': activate_url}
#     # html_body = render_to_string('usuarios/email_confirmation_message.html', context)
#     # email_subject = '¡Tu solicitud debe ser activada con tú correo!'
#     # email = EmailMultiAlternatives(email_subject, html_body, from_email_user, [to_email])
#     # email.content_subtype = "html"  # Agregar esta línea para que el contenido sea HTML
#     # email.send()

#     # # contexto = {'user_display': usuario, 'activate_url': url_activacion}
#     html_content = render_to_string('usuarios/email_confirmation_message.html', context)
#     text_content = f"Hola {usuario.username}, activa tu cuenta en el siguiente enlace: {activate_url}"

#     email = EmailMultiAlternatives(
#         subject="Activa tu cuenta",
#         body=text_content,
#         from_email=settings.EMAIL_HOST_USER,
#         to=[usuario.email]
#     )
#     email.attach_alternative(html_content, "text/html")  # Adjuntar versión HTML
#     email.send()
    
#     envio= EmailEnviado.objects.get(user=usuario.email)
#     if envio: 
#         envio = EmailEnviado.objects.update(count=envio.count+1)
#     else:
#         envio =  EmailEnviado.objects.create(user=usuario, count=1)
#     print("Correo de activación enviado.", usuario)
#     print("Correo registro.", envio)


# def password_change(request):
#     # if request.user.is_authenticated:
#     print(request.user)
#     if request.user.must_change_password:
#         return redirect('password_change_first_login')
#     return redirect('bases:home')


def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(Militante, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # if usuario.must_change_password:
        #     # login(request, usuario)    
        #     # return redirect('asamblea:password_change_first_login')
        #     return redirect('asamblea:password_change_first_login')
        # Activar flag en el perfil
        user.is_active = True
        user.must_change_password = True
        user.save()
        
        
        # Loguear automáticamente al usuario
        #login(request, usuario)        
        
        mensaje = f"Hola {user.get_short_name}, su cuenta está activa"
        context = {'segment': 'index', 'usuario': user, 'mensaje': mensaje, }
        html_template = loader.get_template('usuarios/email_militancia.html')
        return HttpResponse(html_template.render(context, request))
        
        # return redirect('bases:login')    
    else:
        html_template = loader.get_template('usuarios/email_confirm.html')
        return HttpResponse(html_template.render({},request))
    
# class CustomLoginView(LoginView):    
#     def get_success_url(self):
        
#         print('oeeeeee----')

#     #     user = self.request.user
#     #     # if hasattr(user, 'profile') and user.must_change_password:
#     #     # if user.must_change_password:
#     #     #     return reverse_lazy('asamblea:password_change_first_login')
#     #     if user.is_authenticated:
#     #         return reverse_lazy('bases:home')
#     #     return reverse_lazy('bases:home')
#     def form_valid(self, form):
#         print('CustomLoginView----')
        
# @receiver(user_logged_in)
# def enviar_correo_al_iniciar_sesion(sender, request, user, **kwargs):
#     print('por aqui en receiver logeo----', user)
#     if not user.send_email:
#         print('por aqui en enviar correo----')
        
#         hilo = threading.Thread(target=enviar_email_activacion, args=(user,))
#         hilo.start()
#         # messages.info()
        
#         # mensaje = f"Hola {user.get_short_name}, su cuenta está activa"
#         # context = {'segment': 'index', 'usuario': user, 'mensaje': mensaje, }
#         # html_template = loader.get_template('usuarios/email.html')
#         # return HttpResponse(html_template.render(context, request))
        

#         # enviar_email_activacion(user)

class FirstLoginPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_first_login.html'
    success_url = reverse_lazy('bases:home')  

    # def get_success_url(self):
        
    #     print('por aqui---- get suce')
    #     return redirect('bases:home')
    def form_valid(self, form):
        
        print('por aca ----')
        response = super().form_valid(form)
        # Opcional: marcar algo en el perfil del usuario si es su primer login
        # Desactivar la bandera
        user = self.request.user
        user.must_change_password = False
        # user.is_active = True
        user.save()
                
        return response

# from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect, render


@login_required
def subir_csv(request):
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo_csv = request.FILES['archivo_csv']
        datos = []

        # Procesar el archivo CSV
        try:
            decoded_file = archivo_csv.read().decode('utf-8').splitlines()
            
            if not archivo_csv.name.endswith('.csv'):
                return HttpResponse("Error: El archivo debe ser un CSV.")
            
            # Verificar si el archivo está vacío
            if not decoded_file:
                # raise ValueError("El archivo CSV está vacío.")
                return HttpResponse("Error: El archivo CSV está vacío.")


            reader = csv.reader(decoded_file)
            filas = 3
            # Validar que el archivo tenga al menos 15 filas (14 encabezados + 1 de datos)
            if sum(1 for _ in reader) < filas:
                return HttpResponse(f"Error: El archivo CSV debe tener al menos {filas} filas.")

            # Reiniciar el lector para procesar los datos
            archivo_csv.seek(0)
            decoded_file = archivo_csv.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)


            # Saltar las primeras 1 filas (encabezado)
            for _ in range(1):
                next(reader)
                
            # Guardar los datos en la base de datos
            for fila in reader:
                # if len(fila) < 3:
                #     return HttpResponse("Error: Algunas filas tienen menos de 3 columnas.")

                try:
                    # print('----',fila)
                    Registro.objects.create(
                        columna1=fila[0],
                        columna2=int(fila[1]),  # Conversión si aplica
                        columna3=fila[2]  # Ajusta formatos según tu modelo
                    )
                except ValueError as e:
                    return HttpResponse(f"Error de formato en los datos: {str(e)}")
                except IndexError:
                    return HttpResponse("Error: Hay filas con menos columnas de las esperadas.")



            # return HttpResponse("Datos guardados exitosamente!")

            #  Reiniciar el lector para procesar los datos
            archivo_csv.seek(0)
            decoded_file = archivo_csv.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Leer el resto de los datos
            for fila in reader:
                datos.append(fila)

            return render(request, 'file_up/resultado.html', {'datos': datos})

        except UnicodeDecodeError:
            return HttpResponse("Error al decodificar el archivo. Asegúrate de que esté en formato UTF-8.")
        except csv.Error:
            return HttpResponse("Error en el formato del archivo CSV.")
        except Exception as e:
            return HttpResponse(f"Error al procesar el archivo: {str(e)}")

    return render(request, 'file_up/subir_csv.html')


@login_required
def votar(request):
    # Verificar si el usuario ya votó
    if Voto.objects.filter(user=request.user).exists():
        # return HttpResponse("Ya has votado.")
        return HttpResponseRedirect(reverse('asamblea:resultado'))

    opciones = Plancha.objects.filter(mostrar=True)
    if request.method == 'POST':
        opcion_id = request.POST.get('opcion_id')
        try:
            opcion = get_object_or_404(Plancha, pk=opcion_id)
        except (TypeError, ValueError, OverflowError, Plancha.DoesNotExist):
            opcion = None

        if opcion:
            Voto.objects.create(user=request.user, opcion=opcion)
            # ✅ Redirección a una vista de confirmación o resultados
            return HttpResponseRedirect(reverse('asamblea:resultado'))
    return render(request, 'votar/votar.html', {'opciones': opciones})

@login_required
def resultado(request):
    
    conteo =  Voto.objects.values('opcion__name').annotate(total_votos=Count('id')).order_by('-total_votos')
    
    total_votos = sum(item['total_votos'] for item in conteo)
    print(f"Total de votos: {total_votos}")
 
    datos = (
        conteo
    )
    print(conteo)
    print()
    print(conteo.count())

    labels = [d['opcion__name'] for d in datos]
    valores = [d['total_votos'] for d in datos]

    return render(request, 'votar/resultado.html', {
        'labels': labels,
        'valores': valores,
        'datos': conteo,
        'total_votos':total_votos,
    })

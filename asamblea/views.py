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

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView


from django.template import loader
import csv

from .models import Militante
from .forms import *

from bases.views import SinPrivilegios


class UserView(SinPrivilegios, generic.ListView):
    # permission_required = "asamblea.view_categoria"
    model = Militante
    template_name = "asamblea/user_list.html"
    context_object_name = "obj"



## Crear una vista para enviar correos de activación

def enviar_email_activacion(usuario):
    token = default_token_generator.make_token(usuario)
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    
    hosts = settings.DOMINIO
    
    activate_url = f"http://{hosts}{reverse('asamblea:activar_cuenta', kwargs={'uidb64': uid, 'token': token})}"
    user_display = usuario.email

    # mensaje = f"Hola {usuario.username}, activa tu cuenta haciendo clic en el siguiente enlace: {activate_url}"

    # send_mail(
    #     'Activa tu cuenta',
    #     mensaje,
    #     'desarrollotecnologico@partidoverde.org.co',  # Remitente
    #     [usuario.email],  # Destinatario
    #     fail_silently=False,
    # )

    # from_email_user = settings.EMAIL_HOST_USER
    # to_email = usuario.email
    context={'user_display': user_display, 'activate_url': activate_url}
    # html_body = render_to_string('usuarios/email_confirmation_message.html', context)
    # email_subject = '¡Tu solicitud debe ser activada con tú correo!'
    # email = EmailMultiAlternatives(email_subject, html_body, from_email_user, [to_email])
    # email.content_subtype = "html"  # Agregar esta línea para que el contenido sea HTML
    # email.send()

    # # contexto = {'user_display': usuario, 'activate_url': url_activacion}
    html_content = render_to_string('usuarios/email_confirmation_message.html', context)
    text_content = f"Hola {usuario.username}, activa tu cuenta en el siguiente enlace: {activate_url}"

    email = EmailMultiAlternatives(
        subject="Activa tu cuenta",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[usuario.email]
    )
    #email.attach_alternative(html_content, "text/html")  # Adjuntar versión HTML
    email.send()

    print("Correo de activación enviado.")

def password_change(request):
    # if request.user.is_authenticated:
    print(request.user)
    if request.user.must_change_password:
        return redirect('password_change_first_login')
    return redirect('bases:home')


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
    
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        # if hasattr(user, 'profile') and user.must_change_password:
        if user.is_authenticated:
            return reverse_lazy('home')
        if user.must_change_password:
            return reverse_lazy('asamblea:password_change_first_login')
        return reverse_lazy('home')


class FirstLoginPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_first_login.html'
    success_url = reverse_lazy('bases:home')  

    def form_valid(self, form):
        response = super().form_valid(form)
        # Opcional: marcar algo en el perfil del usuario si es su primer login
        # Desactivar la bandera
        user = self.request.user
        user.must_change_password = False
        user.is_active = True
        user.save()
        return response


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






# class CategoriaNew(SuccessMessageMixin,SinPrivilegios,\
#     generic.CreateView):
#     permission_required="inv.add_categoria"
#     model=Categoria
#     template_name="inv/categoria_form.html"
#     context_object_name = "obj"
#     form_class=CategoriaForm
#     success_url=reverse_lazy("inv:categoria_list")
#     success_message="Categoria Creada Satisfactoriamente"

#     def form_valid(self, form):
#         form.instance.uc = self.request.user
#         return super().form_valid(form)


# class CategoriaEdit(SuccessMessageMixin,SinPrivilegios, \
#     generic.UpdateView):
#     permission_required="inv.change_categoria"
#     model=Categoria
#     template_name="inv/categoria_form.html"
#     context_object_name = "obj"
#     form_class=CategoriaForm
#     success_url=reverse_lazy("inv:categoria_list")
#     success_message="Categoria Actualizada Satisfactoriamente"

#     def form_valid(self, form):
#         form.instance.um = self.request.user.id
#         return super().form_valid(form)

# class CategoriaDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):
#     permission_required="inv.delete_categoria"
#     model=Categoria
#     template_name='inv/catalogos_del.html'
#     context_object_name='obj'
#     success_url=reverse_lazy("inv:categoria_list")
#     success_message="Categoría Eliminada Satisfactoriamente"


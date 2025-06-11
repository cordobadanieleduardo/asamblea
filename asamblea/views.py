import sys

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail

from django.http import HttpResponse
# from django.views import generic
# from django.contrib import messages
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
# from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required #, permission_required

from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.db.models import Count #, Sum

# from django.contrib import messages

from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# import threading

from django.template import loader
import csv
import pandas as pd

from .models import Militante
from .forms import *


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
    

class FirstLoginPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_first_login.html'
    success_url = reverse_lazy('bases:home')  

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

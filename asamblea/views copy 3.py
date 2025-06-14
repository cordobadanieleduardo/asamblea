from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #, permission_required

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Count
from collections import defaultdict
from django.db.models import Case, When, Value, IntegerField


from django.template import loader
import csv

from .models import Militante
from .forms import *


def activar_cuenta(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=get_object_or_404(Militante, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        # if usuario.must_change_password:
        #     # login(request, usuario)    
        #     # return redirect('asamblea:password_change_first_login')
        #     return redirect('asamblea:password_change_first_login')
        # Activar flag en el perfil
        user.is_active=True
        user.must_change_password=True
        user.save()
        
        
        # Loguear automáticamente al usuario
        #login(request, usuario)        
        
        mensaje=f"Hola {user.get_short_name}, su cuenta está activa"
        context={'segment': 'index', 'usuario': user, 'mensaje': mensaje, }
        html_template=loader.get_template('usuarios/email_militancia.html')
        return HttpResponse(html_template.render(context, request))
        
        # return redirect('bases:login')    
    else:
        html_template=loader.get_template('usuarios/email_confirm.html')
        return HttpResponse(html_template.render({},request))
    

class FirstLoginPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name='registration/password_change_first_login.html'
    success_url=reverse_lazy('bases:home')  

    def form_valid(self, form):
        
        print('por aca ----')
        response=super().form_valid(form)
        # Opcional: marcar algo en el perfil del usuario si es su primer login
        # Desactivar la bandera
        user=self.request.user
        user.must_change_password=False
        # user.is_active=True
        user.save()
                
        return response

@login_required
def subir_csv(request):
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo_csv=request.FILES['archivo_csv']
        datos=[]

        # Procesar el archivo CSV
        try:
            decoded_file=archivo_csv.read().decode('utf-8').splitlines()
            
            if not archivo_csv.name.endswith('.csv'):
                return HttpResponse("Error: El archivo debe ser un CSV.")
            
            # Verificar si el archivo está vacío
            if not decoded_file:
                # raise ValueError("El archivo CSV está vacío.")
                return HttpResponse("Error: El archivo CSV está vacío.")


            reader=csv.reader(decoded_file)
            filas=3
            # Validar que el archivo tenga al menos 15 filas (14 encabezados + 1 de datos)
            if sum(1 for _ in reader) < filas:
                return HttpResponse(f"Error: El archivo CSV debe tener al menos {filas} filas.")

            # Reiniciar el lector para procesar los datos
            archivo_csv.seek(0)
            decoded_file=archivo_csv.read().decode('utf-8').splitlines()
            reader=csv.reader(decoded_file)


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
            decoded_file=archivo_csv.read().decode('utf-8').splitlines()
            reader=csv.reader(decoded_file)

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

    # print('user', request.user.location)
    # opciones=Plancha.objects.filter(
    #     mostrar=True,
    #     location=request.user.location,
    # ).order_by('id')
    
    opciones=Plancha.objects.none()  # Retorna un queryset vacío
    mostrarBotonVotar=False
    if request.user.location:
        opciones=Plancha.objects.filter(
            mostrar=True,
            location=request.user.location
        ).order_by('id')
    
    grupos=defaultdict(list)
    for o in opciones:
        # militantes=Militante.objects.filter(plancha_id=o.pk).order_by('position')  # Ordenar         
        militantes=Militante.objects.filter(plancha_id=o.pk
            ).annotate(
                prioridad=Case(
                    When(position=0, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField())
        ).order_by('prioridad', 'position')

        for u in militantes:
            grupos[o.name].append(u)
        mostrarBotonVotar= True


    # usuario_por_plancha=list(grupos.values())
    # grupo_usuario_por_plancha=list(grupos.keys())
    
    departamento=''
    municipio=''
    localidad=''
    
    if request.user.location:
        departamento=request.user.location.dpto_name
        municipio=request.user.location.mun_name
        localidad=request.user.location.comuna_name

    # print('Plancha Dos')
    # print(grupos.get('Plancha Dos'))
    
    
    # print('Plancha Uno')
    # print(grupos.get('Plancha Uno'))

    # print(grupo_usuario_por_plancha)
               

    if request.method == 'POST':
        opcion_id=request.POST.get('opcion_id')
        try:
            opcion=get_object_or_404(Plancha, pk=opcion_id)
        except (TypeError, ValueError, OverflowError, Plancha.DoesNotExist):
            opcion=None

        if opcion:
            Voto.objects.create(user=request.user, opcion=opcion)
            # ✅ Redirección a una vista de confirmación o resultados
            return HttpResponseRedirect(reverse('asamblea:resultado'))
        
    return render(request, 'votar/votar.html',
                  {'opciones': opciones,
                #    'usuario_por_plancha':usuario_por_plancha,
                #    'grupo_usuario_por_plancha': grupo_usuario_por_plancha,
                   'grupos': dict(grupos),
                   'departamento':departamento,
                    'municipio':municipio,
                    'localidad':localidad,
                    'mostrarBotonVotar':mostrarBotonVotar,
                   })

from django.db.models import F
from django.db.models import Count, FloatField, ExpressionWrapper
import math
from decimal import Decimal
from django.db.models import Count, F, FloatField, ExpressionWrapper, Func


@login_required
def resultado(request):
    
    # # Verificar si el usuario no votó no deje ver resutlados
    # if not Voto.objects.filter(user=request.user).exists():
    #     # return HttpResponse("Ya has votado.")
    #     return HttpResponseRedirect(reverse('bases:home'))
    
    
    departamento=''
    municipio=''
    localidad=''
    curules=1
    
    if request.user.location:
        departamento=request.user.location.dpto_name
        municipio=request.user.location.mun_name
        localidad=request.user.location.comuna_name
        # curules=Puesto.objects.filter(dpto_name=departamento,mun_name=municipio,comuna_name=localidad).first().num_curul
        curules=Voto.objects.filter(opcion__location=request.user.location).first().opcion.location.num_curul
        
    conteo=Voto.objects.filter(
                opcion__location=request.user.location
            ).values('opcion__name'
            ).annotate(
                total_votos=Count('id'),                
            ).order_by('-total_votos')
    
    l=request.user.location
    # print(f"Localizacion : {l}")
    print(f"curules : {curules}")

    votos_blanco = 2
    
    
    sum_votos=sum(item['total_votos'] for item in conteo)
    sum_votos = sum_votos + votos_blanco
    cociente_electoral=sum_votos / curules
    
    
    print(f"Total de votos: {sum_votos}")
 
    print(f"Votos blanco: {votos_blanco}")

 
    # conteo=conteo.values('opcion__name'
    #         ).annotate(
    #             total_votos=Count('id'),
    #             cociente=F('total_votos') * 1.0 / cociente_electoral,  # Evita errores de tipo
    #             # residuo= F('cociente') % 1
    #              residuo=ExpressionWrapper((F('total_votos') / cociente_electoral) % 1, output_field=FloatField())  # Corrección aquí
                                 
    #         ).order_by('-total_votos')
 
 
    # conteo = conteo.values('opcion__name').annotate(
    #     total_votos=Count('id'),
    #     cociente=ExpressionWrapper(Count('id') // cociente_electoral, output_field=FloatField()),  # División decimal
    #     residuo=F('total_votos') % sum_votos
    #     # residuo= ExpressionWrapper((Count('id') / cociente_electoral)- int(Count('id') / cociente_electoral), output_field=FloatField())    # Módulo
    # ).order_by('-total_votos')


    # conteo = conteo.values('opcion__name').annotate(
    #     total_votos=Count('id'),
    #     cociente=ExpressionWrapper(Count('id') / cociente_electoral, output_field=FloatField()),  # División decimal
    #     residuo=ExpressionWrapper((F('total_votos') / sum_votos) - F('total_votos') / sum_votos, output_field=FloatField())  # La clave está aquí
    # ).order_by('-total_votos')



    conteo = conteo.values('opcion__name').annotate(
        total_votos=Count('id'),
        cociente=ExpressionWrapper(F('total_votos') / cociente_electoral, output_field=FloatField()),
        residuo=ExpressionWrapper(F('total_votos') / cociente_electoral - Func(F('total_votos') / cociente_electoral, function='FLOOR'), output_field=FloatField())  # Corrección aquí
    ).order_by('-total_votos')
 
    # Truncar el cociente antes de enviarlo al template
    for item in conteo:
        item['cociente'] = int(item['cociente'])

    datos=(conteo)
    print(conteo)
    print()
    print(conteo.count())

    # conformacion de listas 
    
    opciones=Plancha.objects.none()  # Retorna un queryset vacío
    grupos=defaultdict(list)
    if request.user.location:
        opciones=Plancha.objects.filter(
            mostrar=True,
            location=request.user.location
        ).order_by('id')
    
    for o in opciones:
        militantes=Militante.objects.filter(plancha_id=o.pk
            ).annotate(
                prioridad=Case(
                    When(position=0, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField())
        ).order_by('prioridad', 'position')

        for u in militantes:
            grupos[o.name].append(u)
        
 
    labels=[d['opcion__name'] for d in datos]
    valores=[d['total_votos'] for d in datos]
    
    print('labels',labels)
    print('valores',valores)

    listas=[d['opcion__name'] for d in grupos.keys()]

    print('listas',listas)
    print('valores',valores)

    return render(request, 'votar/resultado.html', {
        'labels': labels,
        'valores': valores,
        'datos': conteo,
        'total_votos':sum_votos,
        'departamento':departamento,
        'municipio':municipio,
        'localidad':localidad,
        'curules':curules,
        'cociente_electoral':cociente_electoral,
        'votos_blanco':votos_blanco,
        'grupos': dict(grupos),
    })

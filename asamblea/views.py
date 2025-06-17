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
from django.db.models import F, Count, FloatField, ExpressionWrapper, Case, When, Value, IntegerField,Func
from collections import defaultdict

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
    
from decimal import Decimal, ROUND_HALF_UP

@login_required
def resultado(request):
    
    # # Verificar si el usuario no votó no deje ver resutlados
    # if not Voto.objects.filter(user=request.user).exists():
    #     # return HttpResponse("Ya has votado.")
    #     return HttpResponseRedirect(reverse('bases:home'))
    
    
    departamento=''
    municipio=''
    localidad=''
    fecha = ''
    curules=1
    
    if request.user.location:
        departamento=request.user.location.dpto_name
        municipio=request.user.location.mun_name
        localidad=request.user.location.comuna_name
        fecha=request.user.location.fecha

        # curules=Puesto.objects.filter(dpto_name=departamento,mun_name=municipio,comuna_name=localidad).first().num_curul
        iscurules=Voto.objects.filter(opcion__location=request.user.location).first()
        if iscurules:
            curules=iscurules.opcion.location.num_curul
        
    conteo=Voto.objects.filter(
                opcion__location=request.user.location
            ).values('opcion__name'
            ).annotate(
                total_votos=Count('id'),                
            ).order_by('-total_votos')
    # print('conteo ', conteo)
            
    # plancha=Plancha.objects.filter(mostrar=True,location=request.user.location).order_by('id')
    # militantes=Militante.objects.filter(plancha=plancha)
    # militantes_habilitados=Militante.objects.filter(location=request.user.location,is_staff=False)
    # total_mili_por_ubicion= militantes_habilitados.count()
    

    # lista_sufragio = [ x.user.username for x in Voto.objects.filter(opcion__location=request.user.location)]
    
    # militantes_no_votaron=militantes_habilitados.exclude(username__in=lista_sufragio)

    # for m in militantes_no_votaron:
    #     print('militantes_no_votaron ',m.username)
    
    # militantes_en_blanco= militantes_en_blanco.exclude()
    # print('total_mili_por_ubicion ',total_mili_por_ubicion)
    # print('militantes_no_votaron ',militantes_no_votaron.count())

    # print('lista_voto ',lista_voto)
    # print('lista_sufragio ',len(lista_sufragio))
    # votos_blanco = militantes_no_votaron.count()
    votos_blanco = 0
    for c in conteo:
        if c['opcion__name'] == 'Voto en blanco':
            votos_blanco = votos_blanco+ c['total_votos']

    # print(conteo)
    # print('votos_blanco', votos_blanco)

    # print('lista_sufragio ', total_mili_por_ubicion - militantes_no_votaron.count())
    
    sum_votos=(sum(item['total_votos'] for item in conteo)) - votos_blanco
    # sum_votos = total_mili_por_ubicion - militantes_no_votaron.count()
    total_votos_validos=sum_votos + votos_blanco
    # cociente_electoral= round(total_votos_validos / curules,2)
    cociente_electoral= Decimal(str(total_votos_validos / curules))
    redondeado = cociente_electoral.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # print(redondeado)  # 1543.68
    cociente_electoral = redondeado
    
    print(f"cociente_electoral: {cociente_electoral}")
    print(f"sum_votos: {sum_votos}")
    print(f"Total de votos: {total_votos_validos}")
    print(f"Votos blanco: {votos_blanco}")
    print(f"Curules: {curules}")

    conteo = conteo.values('opcion__name').annotate(
        total_votos=Count('id'),
        cociente=ExpressionWrapper(F('total_votos') / cociente_electoral, output_field=FloatField()),
        residuo=ExpressionWrapper(F('total_votos') / cociente_electoral - Func(F('total_votos') / cociente_electoral, function='FLOOR'), output_field=FloatField())  # Corrección aquí
    ).order_by('-total_votos')
 
    # # Truncar el cociente antes de enviarlo al template
    # for item in conteo:
    #     item['cociente'] = int(item['cociente'])

    # Truncar el cociente antes de enviarlo al template
    for item in conteo:
        item['cociente'] = (item['cociente'])

    datos=(conteo)
    # print(conteo)
    # print(conteo.count())

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

    # for key in dict(grupos):
    #     # print(key, "->", grupos[key])
    #     print(key)
    
    conformacion_lista=[]
    if(labels and len(labels)>0):
        lista = [ x.get_full_name() for x in grupos[labels[0]]]
        # print('Lista',lista)
        # Verificar si existe una posición específica antes de acceder
        if lista and 0 <= 0 < len(lista):  # Se evalúa como True si no está vacía
            # print('Cabeza de lista ',lista[0])
            conformacion_lista.append(lista[0])
        if lista and 0 <= 1 < len(lista):  # Se evalúa como True si no está vacía
            # print('Cabeza de lista 2 ',lista[1])
            conformacion_lista.append(lista[1])
      
    # print( ' sgunda lista '.strip())
    # print('lllll', labels[1:])
    for l in labels[1:]:
        lista = [ x.get_full_name() for x in grupos[l]]        
        # Verificar si existe una posición específica antes de acceder
        if lista and 0 <= 0 < len(lista):  # Se evalúa como True si no está vacía
            conformacion_lista.append(lista[0])

    # print( ' tercer  '.strip())
    
    lista_uno = []
    if(labels and len(labels)>0 and 0 <= 0 < len(labels)):
        lista_uno = [ x.get_full_name() for x in grupos[labels[0]]]
        lista_uno =  lista_uno[2:]
        # conformacion_lista.append(lista_uno[0])
    # print( ' lista uno  '.strip(),  lista_uno)
    
    lista_dos = []
    if(labels and len(labels)>0 and 0 <= 1 < len(labels)):
        lista_dos = [ x.get_full_name() for x in grupos[labels[1]]]
        lista_dos =  lista_dos[1:]
        # conformacion_lista.append(lista_dos[0])

    # print( ' lista dos  '.strip(),  lista_dos)
        
    # Intercalar listas
    lista_intercalada = [item for pair in zip(lista_uno, lista_dos) for item in pair]

    # print('lista_intercalada', lista_intercalada)

    # suma_listas = []
    # # Imprimir posición e ítem
    for i, item in enumerate(conformacion_lista + lista_intercalada):
        print(f"Posición {i+1}: {item}")

    suma_listas = [(i+1, item) for i, item in enumerate(conformacion_lista + lista_intercalada)]
    
    return render(request, 'votar/resultado.html', {
        'labels': labels,
        'valores': valores,
        'datos': conteo,
        'total_votos':sum_votos,
        'total_votos_validos':total_votos_validos,
        'departamento':departamento,
        'municipio':municipio,
        'localidad':localidad,
        'fecha':fecha,
        'curules':curules,
        'cociente_electoral':cociente_electoral,
        'votos_blanco':votos_blanco,
        'grupos': dict(grupos),
        'suma_listas': suma_listas
    })

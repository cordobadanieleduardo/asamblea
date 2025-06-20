from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import threading

from datetime import datetime

from asamblea.models import Voto, Puesto



## from .models import *

class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class MustChangePasswordMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'must_change_password'):
            if request.user.must_change_password:
                return redirect('asamblea:password_change_first_login')
        return super().dispatch(request, *args, **kwargs)

# from pytz import timezone as pytz_timezone



class Home(LoginRequiredMixin, MustChangePasswordMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'
    
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        ya_voto= Voto.objects.filter(user=self.request.user).exists()
        context["isVoto"] = ya_voto
        context["isTiempo"] = False

        print('ya_voto', ya_voto)
       
        if l:=self.request.user.location:            
            if p:=Puesto.objects.filter(pk= l.pk).first() :
                full_name = "%s %s %s" % (p.dpto_name, p.mun_name, p.comuna_name if p.comuna_name else '' )
                context["location"] = full_name.strip()
                context["fecha_inicio"] = p.fecha_inicio
                context["fecha_fin"] = p.fecha_fin
                

                # # Fecha almacenada o proporcionada
                # inicio = p.fecha_inicio
                # fin = p.fecha_fin
                # zona_local = pytz_timezone("America/Bogota")

                # fecha_iniciar_naive = datetime(p.fecha_inicio.year, p.fecha_inicio.month, p.fecha_inicio.day,hour= int(p.fecha_inicio.hour),minute=int(p.fecha_inicio.minute), tzinfo=pytz.utc)
                # fecha_final_naive = datetime(p.fecha_fin.year, p.fecha_fin.month, p.fecha_fin.day, hour= int(p.fecha_fin.hour), minute= int(p.fecha_fin.minute),tzinfo=pytz.utc)

                # Convertir a "aware" usando la zona actual
                # zona_local = timezone.get_current_timezone()
                # zona_local = pytz_timezone("America/Bogota")
                # fecha_iniciar = timezone.make_aware(fecha_iniciar_naive, zona_local)
                # fecha_final = timezone.make_aware(fecha_final_naive, zona_local)


                # fecha_iniciar = fecha_iniciar_naive.astimezone(timezone.get_current_timezone())
                # fecha_final = fecha_final_naive.astimezone(timezone.get_current_timezone())


                fecha_iniciar = p.fecha_inicio.astimezone(timezone.get_current_timezone())
                fecha_final = p.fecha_fin.astimezone(timezone.get_current_timezone())

                # # Fecha actual del sistema
                # f=timezone.now()
                # fecha_actual_naive = datetime(f.year, f.month, f.day,hour= int(f.hour),minute=int(f.minute),second= int(f.second))
                # fecha_actual = timezone.make_aware(fecha_actual_naive, zona_local)

                # Mostrar para depurar
                # print("f",f)
                # print("inicio",inicio)
                # print("fin",fin)
              
                                    


                # zona_bogota = pytz_timezone("America/Bogota")

                # # Convertir un datetime naive a aware con zona Bogotá
                # fecha_aware = timezone.make_aware(datetime(2025, 6, 19, 12, 12), zona_bogota)

                # Obtener la fecha actual en Bogotá (si estás usando timezone.now, ya respeta settings.py)
                fecha_actual = timezone.now().astimezone(timezone.get_current_timezone())
                
                
                    # Comparación
                if  fecha_iniciar <= fecha_actual <= fecha_final and not ya_voto :
                    context["isVoto"] = False
                    context["isTiempo"] = True
                    context["mensaje"] = "¡Recuerde que tiene 30 minutos para ejercer su derecho al voto!"
                elif  fecha_iniciar >= fecha_actual <= fecha_final and not ya_voto :
                    context["isVoto"] = False
                    context["isTiempo"] = True
                    context["mensaje"] = "¡No ha empezado la votación!"
                
                else:
                    print("Se le acabó el tiempo ",self.request.user )
                    context["isVoto"] = True
                    context["isTiempo"] = False
                    context["mensaje"] = "¡Se terminó el tiempo de votación!"


            
            
                # print("zona_local",zona_local)
                # print("inico", p.fecha_inicio)
                # print("f", p.fecha_fin)
            
            
                # print("fecha_iniciar_naive",fecha_iniciar_naive)
                # print("fecha_final_naive",fecha_final_naive)
            
                print("fecha_iniciar",fecha_iniciar)
                print("fecha_actual",fecha_actual)
                print("fecha_final", fecha_final)
                print("Fecha en Bogotá:", fecha_actual.strftime("%Y-%m-%d %H:%M:%S"))
                
                # print('/*/*/*', p.fecha_inicio)
                               

        return context
    
class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"
    
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username ',username, 'password ',password )
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:                
                hilo = threading.Thread(target=enviar_email_activacion, args=(user,))
                hilo.start()
                return render(request, 'bases/login.html', {'info': f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.'})
            # elif user.must_change_password:
            #     return redirect('asamblea:password_change_first_login')
            else:
                login(request, user)
                return redirect('bases:home')
        else:
            return render(request, 'bases/login.html', {'error': f'Credenciales incorrectas o no existe usuario {username} activo'})

    return render(request, 'bases/login.html')


def enviar_email_activacion(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
        
    if user is not None and not user.send_email:
      
    
        activate_url = f"http://{settings.DOMINIO}{reverse('asamblea:activar_cuenta', kwargs={'uidb64': uid, 'token': token})}"
        user_display = user.email


        context={'user_display': user_display, 'activate_url': activate_url}
        html_content = render_to_string('usuarios/email_confirmation_message.html', context)
        text_content = f"Hola {user.username}, activa tu cuenta en el siguiente enlace: {activate_url}"

        email = EmailMultiAlternatives(
            subject="Activación cuenta Asambleas CMJ / CLJ",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")  # Adjuntar versión HTML
        email.send()

        user.send_email = True
        user.save()
        print("Correo de activación enviado.", user)


from django.utils import timezone

def formatear_fecha_local(fecha_obj, formato="%Y-%m-%d %H:%M:%S"):
    """
    Convierte un datetime a la zona horaria local y lo devuelve formateado.
    :param fecha_obj: Un objeto datetime (puede ser naive o aware)
    :param formato: Cadena de formato al estilo strftime
    :return: Cadena de texto con la fecha en zona local y formato deseado
    """
    if timezone.is_naive(fecha_obj):
        fecha_obj = timezone.make_aware(fecha_obj, timezone.get_current_timezone())
    fecha_local = fecha_obj.astimezone(timezone.get_current_timezone())
    return fecha_local.strftime(formato)
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

from asamblea.models import Voto



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

class Home(LoginRequiredMixin, MustChangePasswordMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'
    
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["isVoto"] = Voto.objects.filter(user=self.request.user).exists()
        return context
    
class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"
    
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:                
                hilo = threading.Thread(target=enviar_email_activacion, args=(user,))
                hilo.start()
                
                # request.session['info'] = f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.'
                # return redirect('bases:envio')  # Redirigir sin reenviar el formulario

                # return HttpResponseRedirect(reverse('bases:envio',{'info':f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.' }))
                # return render(request, 'bases/activate_account.html', {'info': f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.'})
                # return redirect('asamblea:envio', {'info': f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.'})
                # return redirect(request.get_absolute_url())  # Redirigir a la página del objeto

                return render(request, 'bases/login.html', {'info': f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.'})
                # return render(request, 'bases/activate_account.html', {'info': f'Se ha enviado un correo de activación. Revisa tu correo {user.email}. Debes activar tu cuenta e iniciar sesión nuevamente.'})
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
            subject="Activa tu cuenta",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")  # Adjuntar versión HTML
        email.send()

        
        # envio= EmailEnviado.objects.filter(user=user).first()
        # if envio: 
        #     envio = EmailEnviado.objects.update(user,count=envio.count+1)
        # else:
        #     envio = EmailEnviado.objects.create(user=user, count=1)
            
          # deactivar flag en el perfil   # user.is_active = False
        user.send_email = True
        user.save()
        print("Correo de activación enviado.", user)
        # print("Correo registro.", envio)

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

from django.template import loader


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
    activate_url = f"http://127.0.0.1:8000{reverse('asamblea:activar_cuenta', kwargs={'uidb64': uid, 'token': token})}"
    user_display = usuario.email

    mensaje = f"Hola {usuario.username}, activa tu cuenta haciendo clic en el siguiente enlace: {activate_url}"

    send_mail(
        'Activa tu cuenta',
        mensaje,
        'desarrollotecnologico@partidoverde.org.co',  # Remitente
        [usuario.email],  # Destinatario
        fail_silently=False,
    )

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




def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = get_object_or_404(Militante, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
       # login(request, usuario)
        mensaje = f"Hola {usuario.get_short_name}, su cuenta está activa"
        context = {'segment': 'index', 'usuario': usuario, 'mensaje': mensaje, }
        html_template = loader.get_template('usuarios/email_militancia.html')
        return HttpResponse(html_template.render(context, request))
    else:
        context = {}
        html_template = loader.get_template('usuarios/email_confirm.html')
        return HttpResponse(html_template.render(context, request))

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


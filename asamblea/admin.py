from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from django.shortcuts import redirect
import pandas as pd
from .models import Militante, Plancha , Voto, Lista, Puesto
from django import forms



# Register your models here.


class VotoInline(admin.StackedInline):
    model = Voto
    can_delete = False
    verbose_name_plural = "Votos"
    extra = 0
    readonly_fields = ('fecha_voto',)
    autocomplete_fields = ['opcion']
    show_change_link = True

class UsuarioAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'id':
                field.required = False
    class Meta:
        model = Militante
        fields = "__all__"


# class CustomUserAdmin(admin.ModelAdmin):
class CustomUserAdmin(BaseUserAdmin):
    model = Militante
    list_display =  BaseUserAdmin.list_display + ('is_active','send_email','must_change_password','location__dpto_name','location__mun_name','location__comuna_name','sex','plancha','position','votos_emitidos',)  # Campos visibles en el listado
    search_fields = ('username', 'email', 'first_name', 'last_name','location__dpto_name','location__mun_name','location__comuna_name','plancha__name',)  # Campos por los que puedes buscar
    ordering = ('username',)  # Ordenar por nombre de usuario
    list_filter = ('is_staff', 'is_active', 'location__dpto_name','location__mun_name','location__comuna_name','plancha__name',)  # Filtros en la barra lateral
    autocomplete_fields = ['plancha','location']
    readonly_fields = ('username', 'email','is_staff','is_active','send_email','must_change_password','groups', 'user_permissions',)
    
    # actions = ['exportar_excel']
    # form = UsuarioAdminForm
    # change_list_template = 'admin/importar_vu.html'
    
    def votos_emitidos(self, obj):
        return Voto.objects.filter(user=obj).count()
    votos_emitidos.short_description = "Votos emitidos"

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Atributos', {'fields': ('plancha','position','send_email','must_change_password',)}),
        ('Información Personal', {'fields': ('first_name', 'last_name','location','sex',)}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('is_staff','is_active','username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'sex', 'plancha','send_email','must_change_password','position',)}
        ),
    )
    
    # def importar_ventanilla_unica(self, request):
    #     print("importar_ventanilla_unica entro")
    #     for archivo_excel in request.FILES.getlist('archivo_excel'):
    #         # Leer el archivo Excel y obtener los números de identificación
    #         data_frame = pd.read_excel(archivo_excel)
    #         numeros_identificacion = data_frame['NUMERO_DOCUMENTO'].tolist()
    #         # Marcar los usuarios correspondientes como aprobados
    #         Militante.objects.filter(username__in=numeros_identificacion).update(is_active=True,)

    #     self.message_user(request, "Usuarios ventanilla única importados correctamente.")
    #     return redirect('/admin/asamblea/militante/')
    
    # def changelist_view(self, request, extra_context=None):
    #     print("changelist_view")
    #     if request.method == 'POST' and request.FILES.get('archivo_excel'):
    #         return self.importar_ventanilla_unica(request)
    #     # elif request.method == 'POST':
    #     #     return self.exportar_excel(request)
    #     return super().changelist_view(request, extra_context)
    
    # def exportar_excel(self, request, queryset):
    #     print("exportar_excel")
    #     data = list(queryset.values('username', 'email', 'is_active'))
    #     df = pd.DataFrame(data)
        
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename=usuarios.xlsx'
        
    #     df.to_excel(response, index=False)
    #     return response

    # importar_ventanilla_unica.short_description = "Importar Ventanilla Unica"
    # exportar_excel.short_description = "Exportar a Excel"


class PlanchaAdmin(admin.ModelAdmin):
    model = Plancha
    list_display =  ('name','location__dpto_name','location__mun_name','location__comuna_name', 'mostrar', 'fc',)
    search_fields = ('name','location__dpto_name','location__mun_name','location__comuna_name',)  # Campos por los que puedes buscar
    readonly_fields = ('fc', 'fm','fecha_inicio','fecha_fin')
    list_filter = ( 'location__dpto_name','location__mun_name','location__comuna_name','mostrar',) 
    autocomplete_fields = ('location',)
    
class VotoAdmin(admin.ModelAdmin):
    model = Voto
    list_display =  ('user__username','opcion__location__dpto_name','opcion__location__mun_name','opcion__location__comuna_name',)
    search_fields = ('user__username','opcion__location__dpto_name','opcion__location__mun_name','opcion__location__comuna_name',) 
    list_filter = ('opcion__name','opcion__location__dpto_name','opcion__location__mun_name','opcion__location__comuna_name',) 
    
class PuestoAdmin(admin.ModelAdmin):
    model = Puesto
    list_display =('comuna_name','mun_name','dpto_name','num_curul','fecha','fecha_inicio','fecha_fin',)
    search_fields = ('comuna_name','mun_name','dpto_name','num_curul',)
    list_filter =('dpto_name','mun_name','comuna_name','fecha_inicio','fecha_fin',) 
    


admin.site.register(Plancha, PlanchaAdmin)
# admin.site.register(Voto, VotoAdmin)
# admin.site.register(Lista)
admin.site.register(Puesto,PuestoAdmin)
admin.site.register(Militante, CustomUserAdmin)

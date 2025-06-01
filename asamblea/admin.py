from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Militante, Plancha #, Candidato

# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    model = Militante
    list_display = ('username', 'email', 'first_name', 'last_name','plancha' ,'is_staff', 'is_active')  # Campos visibles en el listado
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Campos por los que puedes buscar
    ordering = ('username',)  # Ordenar por nombre de usuario
    list_filter = ('is_staff', 'is_active','plancha')  # Filtros en la barra lateral

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Placha', {'fields': ('plancha',)}),
        ('Información Personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active','´plancha')}
        ),
    )


class PlanchaAdmin(admin.ModelAdmin):
    readonly_fields = ('fc', 'fm')
    


# class CandidatoAdmin(admin.ModelAdmin):
#     readonly_fields = ('fc', 'fm')
#     list_display = ('name', 'plancha')




admin.site.register(Plancha, PlanchaAdmin)
# admin.site.register(Candidato, CandidatoAdmin)
admin.site.register(Militante, CustomUserAdmin)





# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class UsuarioInline(admin.StackedInline):
#     model = Militante
#     can_delete = False
#     verbose_name_plural = "usuario"


# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [UsuarioInline]

    
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)



# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'profile')
#     search_fields = ('username', 'email')
#     list_filter = ('email',)

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'bio')


# #admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
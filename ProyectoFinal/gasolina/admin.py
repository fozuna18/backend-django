from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Gasolinerias, Precios, GasolineriaUsuario, Usuarios


# Register your models here.
admin.site.register(Gasolinerias)
admin.site.register(Precios)
admin.site.register(Usuarios, UserAdmin)
admin.site.register(GasolineriaUsuario)
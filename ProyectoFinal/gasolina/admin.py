from django.contrib import admin
from .models import Gasolinerias, Precios, TipoUsuarios, Usuarios, GasolineriaUsuario


# Register your models here.
admin.site.register(Gasolinerias)
admin.site.register(Precios)
admin.site.register(Usuarios)
admin.site.register(TipoUsuarios)
admin.site.register(GasolineriaUsuario)
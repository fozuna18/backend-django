from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# Create your models here.
class Gasolinerias(models.Model):
    id_gasolineria = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False)
    ubicacion = models.TextField(verbose_name='Ubicación', null=False)


class Precios(models.Model):
    id_precio = models.AutoField(primary_key=True, null=False)
    magna = models.FloatField(verbose_name='Magna', null=False, default=0)
    premium = models.FloatField(verbose_name='Premium', null=False, default=0)
    diesel = models.FloatField(verbose_name='Diesel', null=False, default=0)
    fecha = models.DateTimeField(verbose_name='Fecha de actualización', null=False)
    fk_id_gasolineria = models.ForeignKey(Gasolinerias, on_delete=models.CASCADE)


class Usuarios(AbstractUser):
    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="Email", unique=True)
    tipoUsuario_desc = models.CharField(max_length=50, verbose_name="Descripcion de tipo de usuario", null=False, default="cliente")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class GasolineriaUsuario(models.Model):
    fk_id_gasolineria = models.ForeignKey(Gasolinerias, on_delete=models.CASCADE)
    fk_id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
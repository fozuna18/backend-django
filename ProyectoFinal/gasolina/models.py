from django.db import models


# Create your models here.
class Gasolinerias(models.Model):
    id_gasolineria = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False)
    ubicacion = models.TextField(verbose_name='Ubicación', null=False)


class Precios(models.Model):
    id_precio = models.AutoField(primary_key=True, null=False)
    tipo_gasolina = models.CharField(max_length=45, verbose_name='Tipo Gasolina', null=False)
    precio = models.FloatField(verbose_name='Precio Gasolina', null=False)
    fecha = models.DateTimeField(verbose_name='Fecha de actualización', null=False)
    fk_id_gasolineria = models.ForeignKey(Gasolinerias, on_delete=models.CASCADE)


class TipoUsuarios(models.Model):
    id_tipoUsuario = models.AutoField(primary_key=True, null=False)
    descripcion = models.CharField(max_length=45, verbose_name='Descripción', null=False)


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, verbose_name='Nombre', null=False)
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos', null=False)
    email = models.EmailField(verbose_name='Correo', null=False)
    password = models.CharField(max_length=10, verbose_name='Contraseña', null=False)
    fk_id_tipoUsuario = models.ForeignKey(TipoUsuarios, on_delete=models.CASCADE)


class GasolineriaUsuario(models.Model):
    fk_id_gasolineria = models.ForeignKey(Gasolinerias, on_delete=models.CASCADE)
    fk_id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
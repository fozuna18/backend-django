import datetime
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from gasolina.models import Gasolinerias, Usuarios, Precios, GasolineriaUsuario, TipoUsuarios
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# CRUD GASOLINERA--------------------------------------------------------------------------------
# Crea y lee gasolinerias ligadas con el usuario
class Gasolineria(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# lista las gasolinerias ligadas al id del usuario enviado por get
    def get(self, request):
        id = request.GET['id']
        gasolinerias = list(Gasolinerias.objects.filter(gasolineriausuario__fk_id_usuario=id).values())
        datos = {
            'status_code': status.HTTP_200_OK,
            'message': 'ok',
            'resultado': gasolinerias
        }
        return JsonResponse(datos)

# Agrega una gasolineria que estará ligada al id del usuario quien tiene iniciado sesion
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        if request.method == 'POST':
            Gasolinerias.objects.create(nombre=jd['nombre'], ubicacion=jd['ubicacion'])
            GasolineriaUsuario.objects.create(fk_id_gasolineria=Gasolinerias.objects.last(),
                                              fk_id_usuario=Usuarios.objects.get(id_usuario=jd['id_usuario']))

            Precios.objects.create(magna=0, premium=0, diesel=0, fecha=datetime.datetime.now(), fk_id_gasolineria=Gasolinerias.objects.last())
            datos = {"status_code": status.HTTP_200_OK,
                     'message': 'ok'
                     }
            return JsonResponse(datos)


# Obtiene y edita una gasolineria
class EditGasolineria(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# Edita un registro de una gasolineria con el id enviado de la gasolineria
    def post(self, request):
        jd = json.loads(request.body)
        print(jd)
        gas = Gasolinerias.objects.get(id_gasolineria=jd['id'])
        print(gas)
        if request.method == 'POST':
            gas.nombre = jd['nombre']
            gas.ubicacion = jd['ubicacion']
            gas.save()
            datos = {"status_code": status.HTTP_200_OK,
                     'message': 'ok'
                     }
            return JsonResponse(datos)


# Obtiene y elimina una gasolineria especifica
class DeleteGasolineria(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# Elimina los registros en las tablas donde se tenga el id de la gasolineria
    def post(self, request):
        jd = json.loads(request.body)
        gas = Gasolinerias.objects.get(id_gasolineria=jd['id'])
        gas2 = GasolineriaUsuario.objects.get(fk_id_gasolineria=jd['id'])
        gas3 = Precios.objects.filter(fk_id_gasolineria=jd['id'])
        gas.delete()
        gas2.delete()
        gas3.delete()
        datos = {"status_code": status.HTTP_200_OK,
                 'message': 'ok'
                 }
        return JsonResponse(datos)


# CRUD USUARIOS----------------------------------------------------------------------------------------
class UsuariosViewSet(View):
    def get(self, request):
        gasolinerias = list(Gasolinerias.objects.filter(GasolineriaUsuario__fk_id_usuario=1).values())
        datos = {
            'status_code': status.HTTP_200_OK,
            'message': 'Peticion realizada correctamente',
            'resultado': gasolinerias
        }
        return JsonResponse(datos)

    def post(self):
        datos = {""}
        return JsonResponse(datos)

    def put(self):
        datos = {""}
        return JsonResponse(datos)

    def delete(self):
        datos = {""}
        return JsonResponse(datos)


# CRUD PRECIOS -------------------------------------------------------------------------------
class GetPrecios(View):
    def get(self, request):
        id = request.GET['id']  # id usuario
        gas = Gasolinerias.objects.filter(gasolineriausuario__fk_id_usuario=id).values('id_gasolineria')
        gas1 = list(Gasolinerias.objects.filter(gasolineriausuario__fk_id_usuario=id).values('nombre'))
        price = list(Precios.objects.filter(fk_id_gasolineria__in=gas).all().values('magna', 'premium', 'diesel', 'fk_id_gasolineria'))
        datos = {
            'status_code': status.HTTP_200_OK,
            'message': 'ok',
            'precios': price,
            "gasolinerias": gas1
        }
        return JsonResponse(datos)

    def post(self):
        datos = {""}
        return JsonResponse(datos)

    def put(self):
        datos = {""}
        return JsonResponse(datos)

    def delete(self):
        datos = {""}
        return JsonResponse(datos)


# Acceso Login ----------------------------------------------------------------------------------------------------------
class Acceder(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        usuario = list(Usuarios.objects.filter(email=email, password=password).values())
        print(usuario)
        if len(usuario) > 0:
            datos = {
                'status_code': status.HTTP_200_OK,
                'message': 'Acceso exitoso',
                'resultado': usuario
            }
        else:
            datos = {
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Acceso denegado',
                'resultado': 'none'
            }
        return JsonResponse(datos)

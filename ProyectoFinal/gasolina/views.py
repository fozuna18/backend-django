import datetime
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from gasolina.models import Gasolinerias, Usuarios, Precios, GasolineriaUsuario
from rest_framework import viewsets, status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


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
class GetUsuarios(View):
    def get(self, request):
        users = list(Usuarios.objects.all().values('id_usuario', 'tipoUsuario_desc', 'first_name', 'last_name', 'email'))
        print(users)
        if users is not None:
            datos = {
                'status_code': status.HTTP_200_OK,
                'message': 'Peticion realizada correctamente',
                'resultado': users
            }
            return JsonResponse(datos)
        else:
            datos = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'usuarios no encontrados',
                'resultado': "none"
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
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

# Edita el precio de la gasolinera seleccionada
    def post(self, request):
        jd = json.loads(request.body)
        print(jd)
        price = Precios.objects.get(fk_id_gasolineria=jd['id'])
        print(price)
        if request.method == 'POST':
            price.magna = jd['tMagna']
            price.premium = jd['tPremium']
            price.diesel = jd['tDiesel']
            price.fecha = datetime.datetime.now()
            price.save()
            datos = {"status_code": status.HTTP_200_OK,
                     'message': 'ok'
                     }
            return JsonResponse(datos)


class GetPrecioxGasolinera(View):
    def get(self, request):
        id = request.GET['id']  # id gasolineria

        price = list(Precios.objects.filter(fk_id_gasolineria=id).values('magna', 'premium', 'diesel', 'fk_id_gasolineria'))
        datos = {
            'status_code': status.HTTP_200_OK,
            'message': 'ok',
            'precios': price
        }
        return JsonResponse(datos)


# Acceso Login ----------------------------------------------------------------------------------------------------------
class Acceder(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd = json.loads(request.body)
        if request.method == 'POST':
            user = authenticate(email=jd['email'], password=jd['password'])
            print(request.body)
            if user is not None:
                login(request, user)
                datos = {
                    'status_code': status.HTTP_200_OK,
                    'message': 'true',
                    'session_id': request.session.session_key,
                    'resultado': [{
                        'id': user.id_usuario,
                        'email': user.email,
                        'nombre': user.first_name,
                        'apellidos': user.last_name,
                        'tipoUsuario': user.tipoUsuario_desc
                    }]
                }
                return JsonResponse(datos)
            else:
                datos = {
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Acceso denegado',
                    'resultado': 'none'
                }
                return JsonResponse(datos)

    def get(self, request):
        if request.session.get('_auth_user_id'):
            return JsonResponse({"isLoggedIn": True})
        else:
            return JsonResponse({"isLoggedIn": False})


class Logout(View):
    permission_classes = (IsAuthenticated,)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            status.HTTP_205_RESET_CONTENT
            return JsonResponse({"message": "Logout no exitoso"})
        except Exception as e:
            status.HTTP_400_BAD_REQUEST
            return JsonResponse({"message": "Logout no exitoso"})
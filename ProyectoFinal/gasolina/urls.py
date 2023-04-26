from django.urls import path
from . import views
from .views import Acceder, Gasolineria, EditGasolineria, DeleteGasolineria, GetPrecios, GetPrecioxGasolinera, GetUsuarios, Logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/login/', Acceder.as_view(), name='acceder'),
    path('auth/logout/', Logout.as_view(), name='logout'),
    path('gasolinerias/', Gasolineria.as_view(), name='gasolineria'),
    path('gasolinerias/edit', EditGasolineria.as_view(), name='gasolineria_edit'),
    path('gasolinerias/delete', DeleteGasolineria.as_view(), name='gasolineria_delete'),
    path('precios/', GetPrecios.as_view(), name='precios'),
    path('precios/gasolineria', GetPrecioxGasolinera.as_view(), name='precios_gasolineria'),
    path('usuarios/', GetUsuarios.as_view(), name='usuarios'),
]

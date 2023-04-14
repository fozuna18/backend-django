from django.urls import path
from . import views
from .views import Acceder, Gasolineria, EditGasolineria, DeleteGasolineria, GetPrecios

urlpatterns = [
    path('acceder', Acceder.as_view(), name='acceder'),
    path('gasolinerias/', Gasolineria.as_view(), name='gasolineria'),
    path('gasolinerias/edit', EditGasolineria.as_view(), name='gasolineria_edit'),
    path('gasolinerias/delete', DeleteGasolineria.as_view(), name='gasolineria_delete'),
    path('precios/', GetPrecios.as_view(), name='precios'),
]

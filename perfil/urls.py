from django.urls import path
from .views import ConfirmarPagoView, GraciasView, PlanesView, pagarPlan
app_name='perfil'

urlpatterns=[
    # path('',inicio, name='inicio'),
    path('planes/',PlanesView.as_view(), name='planes'),
    path('planes/pagar/',pagarPlan, name='pagar'),
    path('gracias/',GraciasView.as_view(), name='gracias'),
    path('confirmar-pago/',ConfirmarPagoView.as_view(), name='confirmar-pago'),
]
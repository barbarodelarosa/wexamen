from django.urls import path
from .views import ConfirmarPagoView, DetallePerfilView, EditarPerfilView, GraciasView, PlanesView,HomeView, affiliateApplication, pagarPlan, referedCode
app_name='perfil'

urlpatterns=[
    path('',HomeView.as_view(), name='home'),
    path('planes/',PlanesView.as_view(), name='planes'),
    path('editar-perfil/<pk>/',EditarPerfilView.as_view(), name='editar-perfil'),
    path('detalle-perfil/<pk>/',DetallePerfilView.as_view(), name='detalle-perfil'),

    path('planes/pagar/',pagarPlan, name='pagar'),
    path('gracias/',GraciasView.as_view(), name='gracias'),
    path('confirmar-pago/',ConfirmarPagoView.as_view(), name='confirmar-pago'),

    path('solicitar-afiliado/', affiliateApplication, name='solicitar-afiliado'),
    path('ref-code/<str:ref_code>/', referedCode, name='ref-code'), #Enviar en la solicitud el codigo de usuario y la url a la que sera redirigido

]
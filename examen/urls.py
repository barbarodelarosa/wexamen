from django.urls import path
from .views import CrearExamenView, CreateExamenView, ExamenListView, inicio, HomeUserView, realizarExamen
app_name='examen'

urlpatterns=[
    path('',inicio, name='inicio'),
    path('usuario/',HomeUserView.as_view(), name='home-user'),
    path('examen/',ExamenListView.as_view(), name='examen'),
    path('crear-examen/<exam_pk>/',realizarExamen, name='create-examen'),
]
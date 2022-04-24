from django.urls import path
from .views import CrearExamenView, CreateExamenView, ExamenListView, HomeView, inicio, HomeUserView, realizarExamen
app_name='examen'

urlpatterns=[
    # path('',inicio, name='inicio'),
    path('',HomeView.as_view(), name='inicio'),
    path('usuario/',HomeUserView.as_view(), name='home-user'),
    path('examenes/',ExamenListView.as_view(), name='examenes'),
    # path('examen/<exam_pk>/',realizarExamen, name='create-examen'),
    path('examen/<pk>/',CreateExamenView.as_view(), name='realizar-examen'),
]
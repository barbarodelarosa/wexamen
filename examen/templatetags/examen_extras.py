import random
from django import template
from examen.models import Respuesta

register = template.Library()
def respuestas(pregunta):
    respuestas = Respuesta.objects.filter(pregunta=pregunta).order_by('?')
    return respuestas

register.filter('respuestas', respuestas)
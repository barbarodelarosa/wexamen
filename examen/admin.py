from pyexpat import model
from django.contrib import admin


from .models import ExamenRespondido, Pregunta, Respuesta, Examen, PreguntasRespondidas
from .forms import ElegirInlineFormset


class ElegirRespuestaInline(admin.TabularInline):
    model = Respuesta
    min_num = 1
    max_num = Respuesta.MAXIMO_RESPUESTA
    can_delete = False
    formset = ElegirInlineFormset


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines=(ElegirRespuestaInline,)
    list_display=['texto',]
    search_fields=['texto','preguntas__texto',]


class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display=['pregunta','respuesta','correcta','puntaje_obtenido']

    class Meta:
        model=PreguntasRespondidas


admin.site.register(Examen)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)
admin.site.register(PreguntasRespondidas)
admin.site.register(ExamenRespondido)
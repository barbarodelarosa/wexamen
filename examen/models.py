from perfil.models import Profile
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre



class Examen(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #Cuando se crea el examen este selecciona 20 preguntas aleatorias y las agrega a preguntas
    preguntas = models.ManyToManyField('Pregunta', related_name='preguntas_examen', blank=True)
    # Cunado va a guardarse el examen este crea instancias de preguntas respondidas las cuales se guardan con el ID al exaqmen de las preguntas que fueron seleccionadas
    # preguntas_respondidas = models.ManyToManyField('PreguntasRespondidas', blank=True)
    precio = models.DecimalField(verbose_name="Precio del examen", default=0, decimal_places=2, max_digits=6)

    resultado = models.DecimalField(verbose_name="Resultado de examen", default=0, decimal_places=2, max_digits=6)
    intentos = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

  
class ExamenRespondido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #Cuando se crea el examen este selecciona 20 preguntas aleatorias y las agrega a preguntas
    # preguntas = models.ManyToManyField('Pregunta', related_name='preguntas_examen', blank=True)
    # Cunado va a guardarse el examen este crea instancias de preguntas respondidas las cuales se guardan con el ID al exaqmen de las preguntas que fueron seleccionadas
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    preguntas_respondidas = models.ManyToManyField('PreguntasRespondidas', blank=True)

    resultado = models.DecimalField(verbose_name="Resultado de examen", default=0, decimal_places=2, max_digits=6, blank=True, null=True)
    intentos = models.IntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

 



class Pregunta(models.Model):
    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1
    #Aqui van las categorias y etiquetas(relacion de mucho a mucho)
    texto = models.TextField(verbose_name="Texto de la pregunta")
    max_puntaje = models.DecimalField(verbose_name="Maximo puntaje", default=5, decimal_places=2, max_digits=6)
    #campo imagen


    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    MAXIMO_RESPUESTA = 4
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.TextField(verbose_name="Texto de la respuesta")
    correcta = models.BooleanField(default=False, verbose_name="Es esta la respuesta correcta?", null=False)
    #campo imagen


    def __str__(self):
        return self.texto



class PreguntasRespondidas(models.Model):
    usuario = models.ForeignKey(Profile, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='intentos')
    correcta = models.BooleanField(verbose_name="Es esta la respuesta correcta?", default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name="Puntaje obtenido", default=0, decimal_places=2, max_digits=6)






def pre_save_examen_receiver(sender, instance, *args, **kwargs):
    pass

pre_save.connect(pre_save_examen_receiver, sender=Examen)
# Create your models here.

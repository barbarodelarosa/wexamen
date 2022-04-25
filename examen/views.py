from django.utils.decorators import method_decorator
from examen.decorator import my_decorator

import random

from django.http import HttpResponse, HttpResponseRedirect
from examen.forms import CrearExamenForm 
from django.shortcuts import render
from django.views import generic
from .models import Examen, ExamenRespondido, PreguntasRespondidas, Profile, Pregunta, Respuesta
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'inicio.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['bienvenido']="HOLA INICIO"
        return context

def inicio(request):
    context={
        'bienvenido':'Hola inicio'
    }
    return render(request, 'inicio.html', context)

class HomeUserView(LoginRequiredMixin, generic.TemplateView):
    template_name='user/home_user.html'

    def get_context_data(self, **kwargs):
        super(HomeUserView, self).get_context_data(**kwargs)
        profile, created = Profile.objects.get_or_create(usuario=self.request.user)
        context={
            'prueba':'Probando',
            'profile':profile
        }
        return context


class ExamenListView(LoginRequiredMixin, generic.ListView):
    template_name='examen_list.html'
    model=Examen

    def get_context_data(self, **kwargs):
        context = super(ExamenListView, self).get_context_data(**kwargs)
        ExamenRespondido.objects.filter(usuario=self.request.user)
        #enviar examenes del usuario
        #enviar otros examenes
        context['examenes_realizados']=ExamenRespondido.objects.filter(usuario=self.request.user)
        return context

@method_decorator(my_decorator, name='dispatch')
class CreateExamenView(LoginRequiredMixin, generic.UpdateView):
    model = Examen
    form_class=CrearExamenForm
  
  
    template_name='user/create_examen.html'
    def get_context_data(self, **kwargs):
        context = super(CreateExamenView, self).get_context_data(**kwargs)
        examen = self.get_object()
        preguntas = examen.preguntas.all().order_by('?')
        for pregunta in preguntas:
            print("PREGUNTA",pregunta)
            for respuesta in pregunta.opciones.all():
                print("OPCONES",respuesta)

        context['examen'] = examen
        context['preguntas'] = preguntas
        return context

    def form_invalid(self, form):
        print(form)
        return super(CreateExamenView,self).form_invalid(form)
        
    def form_valid(self, form):
        # post = form.save(commit=False)
        puntaje_final=0
        examen_pk=self.get_object()
        examen = Examen.objects.get(pk=examen_pk.pk)
        user=self.request.user
        contar_preguntas=examen.preguntas.count()
        

        examen_respondido = ExamenRespondido.objects.create(
            usuario=user,
            examen=examen
        )
        i=1
        while i <= contar_preguntas:
            puntaje_obtenido=0
            # Funcion para todo el proceso de la respuest N
            respuesta=self.request.POST.get(f'respuesta_ok_{i}')
            # la respuesta viene con el id de la progunta y el id de las respuesta
            respuesta_split=respuesta.split("-")
            pregunta_pk = respuesta_split[0] 
            respuesta_pk = respuesta_split[1]

            pregunta_respondida = Pregunta.objects.get(pk=pregunta_pk)
            respuesta_seleccionada = Respuesta.objects.get(pk=respuesta_pk)
            if respuesta_seleccionada.correcta == True:
                puntaje_obtenido = pregunta_respondida.max_puntaje
            created = PreguntasRespondidas.objects.create(
                usuario=user.profile,
                examen=examen,
                pregunta=pregunta_respondida,
                respuesta=respuesta_seleccionada,
                correcta=respuesta_seleccionada.correcta,
                puntaje_obtenido=puntaje_obtenido,
            )
            created.save()
            examen_respondido.preguntas_respondidas.add(created)
            examen_respondido.resultado += puntaje_obtenido
            user.profile.presupuesto = user.profile.presupuesto - examen.precio
            if user.profile.presupuesto <= 0:
                user.profile.presupuesto = 0
            user.profile.save()
            examen_respondido.save()

            i+=1
        return HttpResponseRedirect('/examenes/')
        # post.save()
        # # or instead of two lines above, just do post = form.save()
        # return HttpResponseRedirect('/examen/2/')

    
   



@method_decorator(my_decorator, name='realizarExamen')
def realizarExamen(request, exam_pk):
    user=request.user
    if request.method=="POST":
        print("EL metodo es post")
        form = CrearExamenForm(request.POST)
        if form.is_valid:
            # pregunta = form.cleaned_data['respuesta_ok_1']
            examen_pk=request.POST.get('examen_pk')
            examen = Examen.objects.get(pk=examen_pk)
            contar_preguntas=examen.preguntas.count()
            

            puntaje_final=0
            examen_respondido = ExamenRespondido.objects.create(
                usuario=user,
                examen=examen
            )
            i=1
            while i <= contar_preguntas:
                puntaje_obtenido=0
                # Funcion para todo el proceso de la respuest N
                respuesta=request.POST.get(f'respuesta_ok_{i}')
                # la respuesta viene con el id de la progunta y el id de las respuesta
                respuesta_split=respuesta.split("-")
                pregunta_pk = respuesta_split[0] 
                respuesta_pk = respuesta_split[1]

                pregunta_respondida = Pregunta.objects.get(pk=pregunta_pk)
                respuesta_seleccionada = Respuesta.objects.get(pk=respuesta_pk)
                if respuesta_seleccionada.correcta == True:
                    puntaje_obtenido = pregunta_respondida.max_puntaje
                created = PreguntasRespondidas.objects.create(
                    usuario=user.profile,
                    examen=examen,
                    pregunta=pregunta_respondida,
                    respuesta=respuesta_seleccionada,
                    correcta=respuesta_seleccionada.correcta,
                    puntaje_obtenido=puntaje_obtenido,
                )
                created.save()
                examen_respondido.preguntas_respondidas.add(created)
                examen_respondido.resultado += puntaje_obtenido
                examen_respondido.save()



                i+=1
            return HttpResponseRedirect('/crear-examen/')
        else:
            form = CrearExamenForm(request.POST)

  
    examen = Examen.objects.get(id=exam_pk)
    preguntas = examen.preguntas.all().order_by('?')
    for pregunta in preguntas:
        print("PREGUNTA",pregunta)
        for respuesta in pregunta.opciones.all():
            print("OPCONES",respuesta)

    context = {
            'examen':examen,
            'preguntas':preguntas,
           
    }
  
    return render(request, 'user/create_examen.html', context)




class PlanesView(LoginRequiredMixin, generic.TemplateView):
    template_name='planes.html'

    def get_context_data(self, **kwargs):
        context = super(PlanesView, self).get_context_data(**kwargs)
       
        return context







class CrearExamenView(LoginRequiredMixin, generic.FormView):
    template_name='user/create_examen.html'
    form_class=CrearExamenForm
    success_url="examen:home-user"



    def get_form_kwargs(self):
        kwargs = super(CrearExamenView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        super(CrearExamenView, self).get_context_data(**kwargs)
        examen = Examen.objects.create(usuario=self.request.user)

        context = {
            'preguntas':examen.seleccionar_preguntas()
        }
 
        return context

    def form_invalid(self, form: CrearExamenForm):
        return super().form_invalid(form)


    def form_valid(self, form):
     
        files_objs = []

        files = self.request.FILES.getlist('product_images')
        for file in files:
            file_instant = ProductImagesContent(file=file, user=self.request.user,)
            file_instant.save()
            files_objs.append(file_instant)


        categories = form.cleaned_data['category']
        # tag = form.cleaned_data['tag'],
    
        # avialable_colours = form.cleaned_data.get('avialable_colours')
        # avialable_sizes = form.cleaned_data.get('avialable_sizes')
        # related_products = form.cleaned_data.get('related_products')

        created = Product.objects.create(
            user = self.request.user,
            brand = form.cleaned_data.get('brand'),
            merchant = form.cleaned_data.get('merchant'),
            title = form.cleaned_data.get('title'),
            slug = form.cleaned_data.get('slug'),
            image = form.cleaned_data.get('image'),
            price = form.cleaned_data.get('price'),
            old_price = form.cleaned_data.get('old_price'),
            description = form.cleaned_data.get('description'),
            details = form.cleaned_data.get('details'),
            created = form.cleaned_data.get('created'),
            updated = form.cleaned_data.get('updated'),
            active = True,
            stock = form.cleaned_data.get('stock'),
            new = True,
            selling = False,
            digital = False,
            content_url = form.cleaned_data.get('content_url'),
            content_file = form.cleaned_data.get('content_file'),
            for_auction = False,
            selling_date = form.cleaned_data.get('selling_date'),
        )

        created.product_images.set(files_objs)
        created.category.set(categories)
        # created.tag.set(tag)
        # created.avialable_colours.set(avialable_colours)
        # created.avialable_sizes.set(avialable_sizes)
        # created.related_products.set(related_products)
        created.save()
        messages.info(self.request,"Producto agregado exitosamente")
        return super().form_valid(form)

    



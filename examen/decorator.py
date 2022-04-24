
from django.http import HttpResponseRedirect
from examen.models import Profile, Examen


def my_decorator(func):
    # Comprobar que el usuario tengo el presupuesto necesrio para hacer el exmen
    def wrapper(request,*args, **kwargs):

        print ('Se ha llamado al decorador personalizado')
        # print ('Solicitar ruta% s'% request.path)
        profile = Profile.objects.get(usuario=request.user)
        examen = Examen.objects.get(pk=kwargs['pk'])
        if profile.presupuesto >= examen.precio:
            print("EL USUARIO TIEN PRESUPUESTO")
        else:
            print("EL USUARIO NOOO TIEN PRESUPUESTO")
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)
    return wrapper

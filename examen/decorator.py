
def my_decorator(func):
    # Comprobar que el usuario tengo el presupuesto necesrio para hacer el exmen
    def wrapper(request, *args, **kwargs):
        print ('Se ha llamado al decorador personalizado')
        print ('Solicitar ruta% s'% request.path)
        return func(request, *args, **kwargs)
    return wrapper

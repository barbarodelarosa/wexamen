from django.db import models
from perfil.utils import generate_ref_code
# from examen.models import PreguntasRespondidas

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model): #QuizUser
    GENDER_CHOICE = (
				('HOMBRE', 'HOMBRE'),
				('MUJER', 'MUJER'),
				('OTRO', 'OTRO'),

    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total=models.DecimalField(verbose_name="Puntaje total", default=0, decimal_places=2, max_digits=6)
    presupuesto=models.DecimalField(verbose_name="Presupuesto", default=0, decimal_places=2, max_digits=6)
   
    url = models.CharField(max_length=80, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    
    phone = models.CharField(max_length=11, blank=True, null=True)
    ci = models.CharField(max_length=11, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, unique=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="recommended")
    updated = models.DateTimeField(auto_now=True)
	# created = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, blank=True, null=True)
    affiliated=models.BooleanField(default=False, blank=True, null=True)#Solo se aprueba desde el administrador cuando cumpla los requisitos verificables
    affiliated_url=models.CharField(max_length=30, blank=True, null=True)#Segenera cuando sea aprovada la solicitud de afiliado
    recommended_plan=models.ManyToManyField('Plan', blank=True)
    
	# favorites = models.ManyToManyField(Post)

	# picture = models.ImageField(upload_to=user_directory_path_profile, blank=True, null=True, verbose_name='Picture')
	# banner = models.ImageField(upload_to=user_directory_path_banner, blank=True, null=True, verbose_name='Banner')

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
	# 	SIZE = 250, 250

	# 	if self.picture:
	# 		pic = Image.open(self.picture.path)
	# 		pic.thumbnail(SIZE, Image.LANCZOS)
	# 		pic.save(self.picture.path)

    def __str__(self):
	    return f"{self.user.username} - {self.code}"

    def get_recommended_profiles(self):
	    pass

    def save(self, *args, **kwargs):
	    if self.code=="":
		    code = generate_ref_code()
		    self.code = code
	    super().save(*args, **kwargs)
		

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class Plan(models.Model):
    TYPE_PLAN_CHICES={
        ('BASICO','BASICO'),
        ('MEDIO','MEDIO'),
        ('PRO','PRO'),
    }
    plan_type=models.CharField(max_length=25, choices=TYPE_PLAN_CHICES)
    title = models.CharField(max_length=25)
    caracteristica1 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica2 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica3 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica4 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica5 = models.CharField(max_length=50, blank=True, null=True)
    description=models.TextField()
    price=models.DecimalField(verbose_name="Precio", max_digits=6, default=0, decimal_places=2)


    def __str__(self):
        return self.title


class PlanPago(models.Model):
    TYPE_PLAN_CHICES={
        ('BASICO','BASICO'),
        ('MEDIO','MEDIO'),
        ('PRO','PRO'),
    }
    plan_type=models.CharField(max_length=25, choices=TYPE_PLAN_CHICES)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    purchused=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(verbose_name="Cantidad pagada", max_digits=6, default=0, decimal_places=2)
    # info de enzona
   
    transaction_uuid=models.CharField(max_length=35)
    user_uuid=models.CharField(max_length=35)
    

    def __str__(self):
        return self.profile.usuario.username
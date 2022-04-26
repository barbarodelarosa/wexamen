from django.urls import reverse
import os
from django.db import models
from affiliate.models import Shortener
from perfil.utils import generate_ref_code
from django.db.models.signals import post_save
# from examen.models import PreguntasRespondidas
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image

from django_resized import ResizedImageField




def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.usuario.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name

def user_directory_path_banner(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    banner_pic_name = 'user_{0}/banner.jpg'.format(instance.usuario.id)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

#Posiblemente a cambiar por  profile_pic_name
    return banner_pic_name 









class Profile(models.Model): #QuizUser
    GENDER_CHOICE = (
				('HOMBRE', 'HOMBRE'),
				('MUJER', 'MUJER'),
				('OTRO', 'OTRO'),

    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="Nombres", max_length=25, blank=True, null=True)
    last_name = models.CharField(verbose_name="Apellidos", max_length=25, blank=True, null=True)
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
    picture = ResizedImageField(size=[300, 300], quality=90, upload_to=user_directory_path_profile)
    # picture = models.ImageField(upload_to=user_directory_path_profile, blank=True, null=True, verbose_name='Picture')
    banner = models.ImageField(upload_to=user_directory_path_banner, blank=True, null=True, verbose_name='Banner')

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
	# 	SIZE = 250, 250

	# 	if self.picture:
	# 		pic = Image.open(self.picture.path)
	# 		pic.thumbnail(SIZE, Image.LANCZOS)
	# 		pic.save(self.picture.path)

    def __str__(self):
	    return f"{self.usuario.username} - {self.code}"

    def get_recommended_profiles(self):
	    pass
    
    def get_absolute_url(self):
        return reverse("perfil:detalle-perfil", kwargs={'pk': self.pk})
        
    def save(self, *args, **kwargs):
        # SIZE = 250, 250
        if self.code=="":
            code = generate_ref_code()
            self.code = code

        # if self.picture:
        #     pic = Image.open(self.picture.path)
        #     pic.thumbnail(SIZE, Image.LANCZOS)
        #     pic.save(self.picture.path)
        super().save(*args, **kwargs)
        

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(usuario=instance)

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
    credit = models.DecimalField(verbose_name="Creditos del plan", max_digits=6, default=0, decimal_places=2)


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
    credit = models.DecimalField(verbose_name="Credito adquirido", max_digits=6, default=0, decimal_places=2)
    
    # info de enzona
   
    transaction_uuid=models.CharField(max_length=35)
    user_uuid=models.CharField(max_length=35)
    

    def __str__(self):
        return self.profile.usuario.username




class AffiliateApplication(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	aprovated = models.BooleanField(default=False)


	def __str__(self):
		return self.profile.usuario.email
	

def post_save_affiliate_application_riceiver(sender, instance, created, **kwargs):
	shorttener = Shortener.objects.create(user=instance.profile.usuario, long_url=f'ref-code/{instance.profile.code}/?next_url=/')
	
	profile =  Profile.objects.filter(usuario=instance.profile.usuario).update(affiliated=instance.aprovated, affiliated_url=shorttener.short_url)
	

post_save.connect(post_save_affiliate_application_riceiver, sender=AffiliateApplication)
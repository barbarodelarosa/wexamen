from django.urls import path, re_path

from . import views

app_name='affiliate'
urlpatterns = [
    path('links/', views.affiliateLinks, name='links'),
    path('shortener/', views.shortener, name='shortener'),
	# re_path(r"^shortener/(?P<long_url>[a-zA-Z0-9_-]+)/$", views.shortener, name="shortener",),

  
]
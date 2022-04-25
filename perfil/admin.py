from .models import Plan, PlanPago, Profile
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Plan)
admin.site.register(PlanPago)

from django.contrib import admin
# Register your models here.
from .models import Delegacion, Padron

admin.site.register(Delegacion)
admin.site.register(Padron)

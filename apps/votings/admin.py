from django.contrib import admin
# Register your models here.
from .models import Vote, IVoted

admin.site.register(Vote)
admin.site.register(IVoted)
from django.contrib import admin
# Register your models here.
from .models import Voting, Answer

admin.site.register(Voting)
admin.site.register(Answer)

from django.urls import path
from . import views

app_name = 'votings'

urlpatterns = [
    path('', views.index, name='index'), 
    path('my_profile', views.my_profile, name='my_profile'), 
    path('vote/<int:voting_id>', views.vote, name='vote'),
]

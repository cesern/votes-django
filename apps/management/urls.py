from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('user_list', views.user_list, name='user_list'),
    path('create_voting', views.create_voting, name="create_voting"),
    path('voting_list', views.voting_list, name="voting_list"),
    path('deactivate/<int:user_id>', views.deactivate, name="deactivate"),
    path('activate/<int:user_id>', views.activate, name="activate"),
    path('voting_results/<int:voting_id>', views.voting_results, name='voting_results'),
    path('upload_padron', views.upload_padron, name='upload_padron'),
    path('download_padron', views.download_padron, name='download_padron')
]

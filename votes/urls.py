from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth.views import password_reset_done, password_reset_complete
from .views import index, error_404

urlpatterns = [
    path('', index),
    path('superadmin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('votings/', include('apps.votings.urls')),
    path('management/', include('apps.management.urls')),
    path('password_reset/done', password_reset_done, {
        'template_name':'mails/reset_password/password_reset_done.html'
        }, name='password_reset_done' ),
    path('reset/password_reset_complete', password_reset_complete, {
        'template_name':'mails/reset_password/password_reset_complete.html'
        }, name='password_reset_complete'),
    re_path('[^ ]/', error_404),
]

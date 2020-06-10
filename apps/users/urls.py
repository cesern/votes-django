from django.urls import path, re_path
from . import views
from django.contrib.auth.views import password_reset, password_reset_confirm

app_name = 'users'

urlpatterns = [
    path('new', views.create_new_emplooye, name='new'),
    path('login', views.LoginEmplooyeeView.as_view(), name='login'),
    path('logout', views.logout , name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),

    path('reset/password_reset', password_reset, {
        'template_name':'mails/reset_password/password_reset_form.html',
        'email_template_name': 'mails/reset_password/password_reset_email.html'
        }, name='password_reset'),

    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, { 
            'template_name':'mails/reset_password/password_reset_confirm.html'
            }, name='password_reset_confirm' ),    
]

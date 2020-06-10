from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from .models import Delegacion, Padron
from django.contrib.auth.models import User
from .forms import DelegacionForm, CreateEmplooyeeForm, LoginEmplooyeeForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

def get_delegacion_names():
    delegaciones = list(Delegacion.objects.all().values())
    delegaciones_names = []
    
    for d in delegaciones:
        if d['nombre'] != "TODAS":
            delegaciones_names.append( d['nombre'] )

    delegaciones_names.sort()

    return delegaciones_names

def validate_user(user):
    try:
        if ('username' in user) and ('email' in user) and ('delegacion' in user): 
            padron = Padron.objects.get(numero_de_empleado=user['username']) 
            user = User.objects.get(email=user['email']) 
            user = User.objects.get(username=user['username'])
            return 1 # Usuario ya registrado
        else:
            return 2
    except Padron.DoesNotExist:
        return 2 # el padron
    except User.DoesNotExist:
        if padron.delegacion.nombre != user['delegacion']:
            return 3 # Delegación incorrecta
        elif padron.status == False:
            return 4 # el status es no activo
        else:
            return 5 # es valido
    except:
        return 2

def send_email(user, request):
    # get dominio
    current_site = get_current_site(request)
    # asunto y mensaje
    subject = 'Activa tu cuenta'
    message = render_to_string('mails/activar_cuenta.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token':account_activation_token.make_token(user),
    })
    # crea y envia el mensaje
    email = EmailMessage(
        subject, message, to=[request.POST['email']]
    )
    email.send()

def create_new_emplooye(request):
    if request.user.is_authenticated:
        return redirect('votings:index')

    msg = None

    if request.method == 'POST':
        tipo_error = validate_user(request.POST)   
        if tipo_error == 1:
            msg = 'Usuario ya registrado'
        elif tipo_error == 2:
            msg = 'El número de empleado no se encuentra en el padrón'
        elif tipo_error == 3:
            msg = 'El número de empleado no coincide con la delegación'
        elif tipo_error == 4:
            msg = 'Su estado en el padrón es inactivo'
        else: 
            form = CreateEmplooyeeForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                send_email(user, request)
                # manda una aviso de que active su cuenta    
                return render(request, 'users/new.html', {
                    'form': form,
                    'msg': None,
                    'activate': True, 
                    'd_names': get_delegacion_names()
                })
            # envia los error al context y los renderiza
            return render(request, 'users/new.html', {
                'form': form,
                'msg': None,
                'activate': False, 
                'd_names': get_delegacion_names(),
                'user': {
                    'username': request.POST['username'],
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'email': request.POST['email'],
                    'delegacion': request.POST['delegacion'] 
                }
            })
    
        # hubo un error
        return render(request, 'users/new.html', {
            'form': CreateEmplooyeeForm(),
            'msg': msg,
            'activate': False, 
            'd_names': get_delegacion_names(),
            'user': {
                'username': request.POST['username'],
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'delegacion': request.POST['delegacion'] 
            }
        })

    else:
        # si es get o hubo un error
        return render(request, 'users/new.html', {
            'form': CreateEmplooyeeForm(),
            'msg': msg,
            'activate': False, 
            'd_names': get_delegacion_names()
        })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # if user is not None and account_activation_token.check_token(user, token):
    if user is not None:
        user.is_active = True
        user.save()
        return render(request, 'users/activate.html', {
            'message':'Gracias por la verificación de su correo electrónico. Ahora puede iniciar sesión con cuenta.'
        })
    else:
        return render(request, 'users/activate.html', {
            'message':'¡El enlace de activación no es válido!'
        })

class LoginEmplooyeeView(CreateView):
    form = LoginEmplooyeeForm()
    template = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('votings:index')
        
        if 'show' not in request.session:
            request.session['show'] = False
            return render(request, self.template, {'form': self.form, 'show':True})
        else:
            return render(request, self.template, {'form': self.form, 'show':False})

    def post(self, request, *args, **kwargs):
        username_post = request.POST['username'] if 'username' in request.POST else 'noexiste' 
        password_post = request.POST['password'] if 'password' in request.POST else 'noexiste'

        user = authenticate(username=username_post, password=password_post)

        if user is not None:
            login_django(request, user)
            if request.user.is_staff == False:
                return redirect('votings:index')
            else:
                return redirect('management:voting_list')
        else:
            messages.error(request, 'Numero de empleado o contraseña incorrecta')   
        return render(request, self.template, {
            'form': self.form,
            'user': {
                'username': request.POST['username'],
                'password': request.POST['password'],
            }
        })

@login_required(login_url='users:login')
def logout(request):
    logout_django(request)
    return redirect('users:login')
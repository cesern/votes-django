from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Voting, Answer
from apps.users.models import Padron, Delegacion
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
# csv
import csv
from django.http import HttpResponse, StreamingHttpResponse

def get_users():
    return list(User.objects.raw("""
        SELECT 1 id, au.id as user_id, ud.nombre as delegacion, up.numero_de_empleado, up.nombre_completo, au.is_active
        FROM users_padron up 
        JOIN users_delegacion ud ON ud.id = up.delegacion_id
        JOIN auth_user au
        WHERE au.username = up.numero_de_empleado"""))
    
@login_required(login_url='users:login')
def user_list(request):
    
    if request.user.is_staff == True:
        return render(request, 'management/user_list.html', {'users':get_users()})
    else:
        return redirect('votings:index')

def get_delegacion_names():
    delegaciones = list(Delegacion.objects.all().values())
    delegaciones_names = []
    
    for d in delegaciones:
        if d['nombre'] != "TODAS":
            delegaciones_names.append( d['nombre'] )

    delegaciones_names.sort()
    # para ponerla al inicio
    delegaciones_names.insert(0, "TODAS")

    return delegaciones_names

def get_date(fecha):
    date = fecha[0].split("-") # 2017-03-07 13:00, 2018-03-07 14:00 
    hour_and_minute = fecha[1].split(":")
    return datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), 
        hour=int(hour_and_minute[0]), minute=int(hour_and_minute[1]))

def get_dates(fecha_de_inicio, fecha_de_cierre):
    return get_date(fecha_de_inicio), get_date(fecha_de_cierre)

def save_voting(post):
    tema, pregunta = post['tema'], post['pregunta']
    fecha_de_inicio, fecha_de_cierre = get_dates([post['fecha_de_inicio'], post['hora_de_inicio']], 
        [ post['fecha_de_cierre'], post['hora_de_cierre']])

    if fecha_de_inicio < datetime.now():
        return {'tipo': 0, 'd_names':get_delegacion_names()}
    elif fecha_de_cierre < fecha_de_inicio:
        return {'tipo': 1, 'd_names':get_delegacion_names()}
    # creo el votacion
    voting = Voting()
    voting.tema = tema
    voting.pregunta = pregunta
    voting.delegacion = Delegacion.objects.get(nombre=post['delegacion'])
    voting.fecha_de_inicio = fecha_de_inicio
    voting.fecha_de_cierre = fecha_de_cierre
    voting.save()
    # creo las respuestas y las guardo
    # len(post)-8 = numero de respuestas
    for i in range(len(post)-8): 
        answer = Answer()
        answer.respuesta = post['op{}'.format(i+1)]
        answer.votacion = voting
        answer.save()
    return None

@login_required(login_url='users:login')
def create_voting(request):
    
    if request.method == 'GET':
        
        if request.user.is_staff == True:
            return render(request, 'management/create_voting.html', {'d_names':get_delegacion_names()})
        else:
            return redirect('votings:index')

    else:
        error = save_voting(request.POST)
        if error is None:
            return redirect('management:voting_list')
        else:
            print(error)
            return render(request, 'management/create_voting.html', error)

def send_email(request, template, subject, user, case=0):
    # get dominio
    current_site = get_current_site(request)
    context = ({'user':user, 'razon': request.POST['razon']} if case == 0 else {'user':user})
    message = render_to_string(template, context)
    # crea y envia el mensaje
    email = EmailMessage(
        subject, message, to=[user.email]
    )
    email.send()

@login_required(login_url='users:login')
def deactivate(request, user_id):
    if request.method == 'POST':
        try:
            user_desactivate = User.objects.get(id=user_id)
            user_desactivate.is_active = False
            user_desactivate.save()
            send_email(request, 'mails/desactivar_usuario.html', 
                'Su cuenta a sido desactivada', user_desactivate)
            print("se cambio")
            return redirect('management:user_list')
        except User.DoesNotExist:
            print("no existe")
            return redirect('management:user_list') 
    else:
        
        if request.user.is_staff == True:
            return redirect('management:user_list')
        else:
            return redirect('votings:index')

@login_required(login_url='users:login')
def activate(request, user_id):
    if request.method == 'POST':
        try:
            user_activate = User.objects.get(id=user_id)
            user_activate.is_active = True
            user_activate.save()
            send_email(request, 'mails/activar_usuario.html', 
                'Su cuenta a sido activada', user_activate, case=1)
            return redirect('management:user_list')
        except User.DoesNotExist:
            return redirect('management:user_list') 
    else:
        
        if request.user.is_staff == True:
            return redirect('management:user_list')
        else:
            return redirect('votings:index')

def get_date_str(date):
    seven_hours = timedelta(hours=7)
    fecha = date - seven_hours
    return fecha.strftime("20%y/%m/%d %H:%M")

def get_today():
    #saca la zona horaria de hermosillo
    timezone = pytz.timezone("America/Hermosillo")
    #le pone la zona horaria y la trnaforma para poder comparar
    return timezone.localize(datetime.now())

def get_votings():
    voting_list = list(Voting.objects.all().values())
    votings = []
    # los paso a string, para convertir la fecha
    for v in voting_list:
        voting = {
            'id': v['id'],
            'tema': v['tema'],
            'fecha_de_inicio_str': get_date_str(v['fecha_de_inicio']),
            'fecha_de_cierre_str': get_date_str(v['fecha_de_cierre']),
            'fecha_de_inicio': v['fecha_de_inicio'],
            'fecha_de_cierre': v['fecha_de_cierre'],
        }
        votings.append(voting)

    return votings

@login_required(login_url='users:login')
def voting_list(request):
    
    if request.user.is_staff == True:
        context = {
            'votings': get_votings(),
            'fecha': get_today()
        }
        return render(request, 'management/voting_list.html', context)
    else:
        return redirect('votings:index')

def get_users_who_voted(voting_id):
    users_who_voted = list(Delegacion.objects.raw("""
        SELECT 1 id, d.nombre delegacion, p.numero_de_empleado, p.nombre_completo
        FROM votings_ivoted iv
        JOIN auth_user u ON u.id = iv.usuario_id
        JOIN users_padron p ON p.numero_de_empleado = u.username
        JOIN users_delegacion d ON p.delegacion_id = d.id
        WHERE iv.votacion_id = %s
        ORDER BY delegacion ASC""", [voting_id] ))

    users_who_voted_list = []
    # obtengo las personas que votaron
    for user_who_voted in users_who_voted:
        user_v = {
            'delegacion': user_who_voted.delegacion,
            'numero_de_empleado': user_who_voted.numero_de_empleado,
            'nombre_completo': user_who_voted.nombre_completo,
        }
        users_who_voted_list.append(user_v)

    return users_who_voted_list

def get_voting_results(voting_id):
    
    try:
        voting_results =  list(Voting.objects.raw("""
        SELECT 1 id, vg.tema, vg.pregunta, a.respuesta, COUNT(*) votos
        FROM votings_vote v
        JOIN management_voting vg ON vg.id = v.votacion_id
        JOIN management_answer a ON a.id = v.respuesta_id
        WHERE v.votacion_id = %s
        GROUP BY a.respuesta ORDER BY votos DESC""", [voting_id]))

        # obtengo los datos de la votacion
        votacion = {
            'tema': voting_results[0].tema,
            'pregunta': voting_results[0].pregunta
        }
    except:
        # si no hay votaciones, se obtiene la votacion
        voting = Voting.objects.get(id=voting_id)
        votacion = {
            'tema': voting.tema,
            'pregunta': voting.pregunta
        }
        voting_results = []


    voting_results_list = []
    # obtengo las respuestas con sus votos
    for voting_result in voting_results:
        voting = {
            'respuesta': voting_result.respuesta,
            'votos': voting_result.votos
        }
        voting_results_list.append(voting)

    # agrego alguna respuesta si es que falto
    answers_of_voting = list(Answer.objects.filter(votacion_id=voting_id).values())
    answers_of_voting = [ v['respuesta'] for v in answers_of_voting ]

    for answer_of_voting in answers_of_voting:
        if answer_of_voting not in ( voting['respuesta'] for voting in voting_results_list):
            voting_results_list.append({
                'respuesta': answer_of_voting,
                'votos': 0
            })

    return votacion, voting_results_list

@login_required(login_url='users:login')
def voting_results(request, voting_id):
    
    if request.method == 'POST':
        #saca la zona horaria de hermosillo
        timezone = pytz.timezone("America/Hermosillo")
        #le pone la zona horaria y la trnaforma para poder comparar
        fecha = timezone.localize(datetime.now())
        users_who_voted = get_users_who_voted(voting_id) 
        votacion, voting_results = get_voting_results(voting_id)
        return JsonResponse({ 
            'votacion': votacion,
            'users': users_who_voted, 
            'results': voting_results,
            'fecha' : fecha 
        })
    else:
        return redirect('management:voting_list')

def clean_padron(dirty_padron):
    padron_clean = []
    padron_space = dirty_padron.split(",")
    for p in padron_space:
        padron_clean.append(p)
    return padron_clean

@login_required(login_url='users:login')
def upload_padron(request):
    
    if request.method == 'GET':
        
        if request.user.is_staff == True:
            return render(request, 'management/upload_padron.html', {})
        else:
            return redirect('votings:index')

    try:
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo no es CSV')
            return redirect('management:upload_padron')

        file_data = csv_file.read().decode("utf-8")        
 
        lines = file_data.split("\n")
        lines.pop() # elimino el ultimo ya que es basura
        padron_list = []
        
        for i in range(len(lines)):
            padron_user = lines[i].split(",") 
            
            print(i, padron_user[:])

            padron = Padron(
                numero_de_empleado= int(padron_user[1]),
                nombre_completo= padron_user[2],
                status= True if padron_user[3].strip() == 'ACTIVO' else False,
                delegacion= Delegacion.objects.get(nombre=padron_user[0]),
            )

            padron_list.append( padron )

        Padron.objects.bulk_create(padron_list)            
        
    except Exception as e:
        messages.error(request, "Incapas de subir el archivo. "+repr(e))
        return redirect('management:upload_padron')

    messages.success(request, 'Se subio el padron')
    return redirect('management:upload_padron')
# para la descarga del padron
class Echo:
    
    def write(self, value):
        return value     

@login_required(login_url='users:login')
def download_padron(request):
    if request.method == 'GET':
        return render(request, 'management/download_padron.html', {})
    else:
        # obtengo el padron actual
        padron_list = list(Padron.objects.all())
        # creo la lista
        rows = ([p.delegacion.nombre, p.numero_de_empleado, p.nombre_completo, "ACTIVO" if p.status else "NO ACTIVO" ] for p in padron_list)
        writer = csv.writer(Echo())
        # grabo el padron
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="Padron.csv"'
        return response
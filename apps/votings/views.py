from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib import messages
from apps.management.models import Voting, Answer
from apps.users.models import Delegacion
from .models import Vote, IVoted
import datetime
import pytz

# Create your views here.
def get_encuestas(usuario):
    #return list(Voting.objects.all().order_by('-fecha_de_inicio'))
    delegacion_usuario = Delegacion.objects.get(nombre=usuario.delegacion)
    delegacion_all = Delegacion.objects.get(nombre="TODAS")
    delegaciones = [delegacion_usuario.id, delegacion_all.id]

    return list(Voting.objects.raw("""
        SELECT 1 idd, mv.id, mv.tema, mv.pregunta, mv.fecha_de_inicio, mv.fecha_de_cierre
        FROM management_voting mv
        WHERE mv.delegacion_id IN %s 
        ORDER BY mv.fecha_de_inicio DESC""", [delegaciones]))

def get_respuestas(encuestas):
    #return list(Answer.objects.all())

    encuestas_ids = [ e.id for e in encuestas ]

    return list(Answer.objects.raw("""
        SELECT 1 idd, ma.id, ma.votacion_id, ma.respuesta
        FROM management_answer ma
        WHERE ma.votacion_id IN %s """, [encuestas_ids]))

def get_resultados(encuestas):
    voting_ids = [ e.id for e in encuestas ]

    voting_results = list(Voting.objects.raw("""
        SELECT 1 id, v.votacion_id, a.respuesta, COUNT(*) votos
        FROM votings_vote v
        JOIN management_voting vg ON vg.id = v.votacion_id
        JOIN management_answer a ON a.id = v.respuesta_id
        WHERE v.votacion_id IN %s
        GROUP BY a.respuesta, v.votacion_id ORDER BY votos DESC""", [voting_ids]))

    answers_with_zero_votes = []
    for v_id in voting_ids:
        # agrego alguna respuesta si es que falto
        answers_of_voting = list(Answer.objects.filter(votacion_id=v_id).values())
        # se agregan las respuestas de la votacion con votos
        voting_result = []
        for v in voting_results:
            if v.votacion_id == v_id:
                voting_result.append(v.respuesta)
    
        # se agregan las respuestas con cero votos
        for answer_of_voting in answers_of_voting:
            if answer_of_voting['respuesta'] not in voting_result:
                answers_with_zero_votes.append({
                    'id':1,
                    'votacion_id': v_id,
                    'respuesta': answer_of_voting['respuesta'],
                    'votos': 0
                })    

    return voting_results + answers_with_zero_votes

def get_iVoted(request):
    return list(IVoted.objects.filter(usuario=request.user))   

def get_iVotedPregunta(request):
    return list(IVoted.objects.all())   

def get_user(request):
    return list(User.objects.raw("""
        SELECT 1 id, d.nombre delegacion, p.numero_de_empleado, p.nombre_completo, u.email
        FROM auth_user u
        JOIN users_padron p ON p.numero_de_empleado = u.username
        JOIN users_delegacion d ON p.delegacion_id = d.id
        WHERE u.username = %s""", [request.user.username]))[0]

@login_required(login_url='users:login')
def index(request):
    
    if request.method == 'GET':
        
        if request.user.is_staff == False:
            usuario = get_user(request)
            encuestas = get_encuestas(usuario)
            respuestas = get_respuestas(encuestas)
            resultados = []
            ivoted = get_iVoted(request)
            #nomas tomar los id's
            votos = [i.votacion.id for i in ivoted]
            #saca la zona horaria de hermosillo
            timezone = pytz.timezone("America/Hermosillo")
            #le pone la zona horaria y la trnaforma para poder comparar
            ahora = timezone.localize(datetime.datetime.now())
            #nomas agarrar el de la fecha d einicio mayor"
            encuesta = []

            if len(encuestas) > 1:
                encuesta.append(encuestas[0])
                encuesta.append(encuestas[1])
                resultados = get_resultados(encuesta)
            elif len(encuestas) == 1:
                encuesta.append(encuestas[0])
                resultados = get_resultados(encuesta)

            if 'show2' not in request.session:
                request.session['show2'] = False
                return render(request, 'votings/index.html', {
                    'encuestas': encuesta,
                    'respuestas': respuestas,
                    'resultados': resultados,
                    'votos': votos,
                    'fecha':ahora,
                    'show2':True
                })
            else:
                return render(request, 'votings/index.html', {
                    'encuestas': encuesta,
                    'respuestas': respuestas,
                    'resultados': resultados,
                    'votos': votos,
                    'fecha':ahora,
                    'show2':False
                })

        else:
            return redirect('management:user_list')

@login_required(login_url='users:login')
def vote(request, voting_id):
    
    if request.method == 'POST':
        #para checar si no ha pasado la fecha y est fuera de tiempo
        votacion = Voting.objects.get(id=voting_id)
        #saca la zona horaria de hermosillo
        timezone = pytz.timezone("America/Hermosillo")
        #le pone la zona horaria y la trnaforma para poder comparar
        ahora = timezone.localize(datetime.datetime.now())
        #calcula si esta fuera de tiempo
        fueraDeTiempo=votacion.fecha_de_cierre<ahora
        #hace una consulta y si encuentra que el usuario respondio esa pregunta lo guarda en yaVoto y si no sta vacia la variable
        yaVoto=list(IVoted.objects.filter(usuario=request.user,votacion_id=voting_id))
        #si no ha votado guarda y no ha pasado la fecha de cierre el voto
        if (not yaVoto) and (not fueraDeTiempo) and ('choice' in request.POST): 
            # ivoted_p = IVoted(usuario_id=request.user.id, votacion_id=votacion_id)
            # obtengo la votacion y la respuesta
            try:
                votacion = Voting.objects.get(id=voting_id)
                respuesta = Answer.objects.get(id=request.POST['choice'])
                #crea y guardo el voto
                vote = Vote()
                vote.votacion = votacion
                vote.respuesta = respuesta
                vote.save()
                # creo y guardo que el usuario a votado en esa votacion
                ivoted = IVoted()
                ivoted.usuario = request.user
                ivoted.votacion = votacion
                ivoted.save()
            except:
                print("Error votacion o respuesta null")
        #si ya voto le recrimina por trampa    
        else: 
            print("Ya habia votado o es fuera de tiempo")

    if request.user.is_staff == False:
        return redirect('votings:index')
    else:
        return redirect('management:user_list')

@login_required(login_url='users:login')
def my_profile(request):
    
    if request.method == 'GET':
        
        if request.user.is_staff == False:
            return render(request, 'votings/my_profile.html', {'user':get_user(request)})
        else:
            return redirect('management:user_list')

    else:
        # cambio el password
        password_old = request.POST['password_old'] if 'password_old' in request.POST else 'noexiste123'
        password_new1 = request.POST['password_new1'] if 'password_new1' in request.POST else 'noexiste123'
        password_new2 = request.POST['password_new2'] if 'password_new2' in request.POST else 'noexiste124'

        if password_new1 == password_new2:

            if authenticate(username=request.user.username, password=password_old):
                request.user.set_password(password_new1)
                request.user.save()                
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Contraseña actualizada')
            else:
                messages.error(request, 'La contraseña actual no coincide') 

        else:
            messages.error(request, 'Las contraseñas no coinciden') 

        return render(request, 'votings/my_profile.html', {'user':get_user(request)})
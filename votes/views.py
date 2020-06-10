from django.shortcuts import render, redirect

def index(request):
    return redirect('users:login')

def error_404(request, s1=0):
    return redirect('users:login')
    # return render(request, 'error404.html', {})

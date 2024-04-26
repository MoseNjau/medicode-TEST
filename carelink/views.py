from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from .forms import CreateUserForm,LoginForm
from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
def homepage(request):
    return render(request,"carelink/index.html")


def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        

    context ={
        'registerform':form,
    }    
    return render(request,"carelink/register.html", context)




def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponseRedirect('login')
  
    context = {
      'loginform': form,
            }
    return render(request, 'carelink/login.html', context)


def logout(request):
    auth.logout(request)

    return redirect(reverse('login'))

@login_required(login_url='login')

def dashboard(request):
    return render(request,"carelink/dashboard.html")


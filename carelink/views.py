from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from .forms import CreateUserForm,LoginForm
from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Room, Message
from django.http import HttpResponse, JsonResponse
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

def show_chat(request):
    return render(request,"carelink/chatpage.html")

# Create your views here.
def home(request):
    return render(request, 'index.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    print(room_details)
    return render(request, 'carelink/chatpage.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def colourful(request):
    return render(request, 'carelink/colourful.html')


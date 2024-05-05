# Create your views here.
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from .forms import CreateUserForm,LoginForm
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import json 
from .models import Message
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

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request ,username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                return redirect('login')
  
    context = {
      'loginform': form,
            }
    return render(request, 'carelink/login.html', context)


def logout(request):
    auth.logout(request)

    return redirect(reverse('login'))

def home(request):
    return render(request, 'index.html')

#dashboard feature
@login_required(login_url='login')
def dashboard(request):
    users = User.objects.exclude(pk=request.user.pk)
    context = {
        'users':users 
            }
    return render(request,"carelink/dashboard.html",context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']  # Assuming content is sent in the request POST data
        sender = request.user
        receiver_id = int(data['receiver_id'])  # Assuming receiver_id is sent in the request POST data
        print(data,content)      
        receiver = User.objects.get(pk=receiver_id)
        
        # Create a new message instance
        message = Message.objects.create(sender=sender, receiver=receiver, content=content)
        # Return a success response
        return JsonResponse({'status': 'success', 'message_id': message.id})
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

@login_required
@csrf_exempt
def check_messages(request):
    if request.method == 'POST':
        receiver_id = json.loads(request.body)['receiver']
        print(receiver_id)
        # Get messages for the current user
        user_messages = Message.objects.filter((Q(sender=request.user) & Q(receiver_id=receiver_id)) | (Q(sender_id=receiver_id) & Q(receiver=request.user))).order_by('timestamp') 
        print(user_messages)
        # Serialize messages data
        messages_data = [{'content': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),'sender':message.sender.pk == request.user.pk } for message in user_messages]
        
        # Return messages data as JSON response
        return JsonResponse(messages_data, safe=False)
    else:
        # Return an error response if the request method is not GET
        return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed'})


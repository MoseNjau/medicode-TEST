# Create your views here.
from types import new_class
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from .forms import CreateUserForm,LoginForm
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import csv,os 
from fpdf import FPDF
from django.conf import settings
import json 
from .models import Message
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message,User_profile
from django.contrib.auth.decorators import login_required

#for messages 
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
#import objectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

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


#messages 
@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']  # Assuming content is sent in the request POST data
        sender = request.user
        receiver_id = int(data['receiver_id'])  # Assuming receiver_id is sent in the request POST data     
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
        try:
            receiver_id = json.loads(request.body)['receiver']
        except (KeyError, TypeError, json.JSONDecodeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        
        # Get messages for the current user
        user_messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver_id=receiver_id)) | 
            (Q(sender_id=receiver_id) & Q(receiver=request.user))
        ).order_by('timestamp')
        print(Message.objects) 
        # Serialize messages data
        messages_data = [
            {
                'content': message.content, 
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'sender': message.sender.pk == request.user.pk
            } 
            for message in user_messages
        ]
        
        # Return messages data as JSON response
        return JsonResponse(messages_data, safe=False)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)
@login_required
@csrf_exempt
def patients(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'doctors.csv')
    specialty = set()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            specialty.add(row['specialty'])
        if len(specialty) == 0:
            specialty.add('Not hospitals in the DATASET')

    # Build the file path
    file_path = os.path.join(settings.BASE_DIR, 'data', 'patients.csv')
    # Open and read the CSV file
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    # Pass the data to the template or return it as a JSON response
    file_path = os.path.join(settings.BASE_DIR, 'data', 'Health_facilities(Health_facilities_0).csv')
    hospitals = set()
    agency = set()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            hospitals.add(row['Facility Name'])
            agency.add(row['Agency'])
        if len(hospitals) == 0:
            hospitals.add('Not hospitals in the DATASET')

    context = {'patients': data,'hospitals':hospitals,'agency':agency,"speciality":specialty}
    return render(request,"carelink/patients.html",context)

@login_required
@csrf_exempt
def get_doctor_in_hospital(request):
    hospital_name = ''
    if request.method == 'POST':
        hospital_name= json.loads(request.body)['hospital_name']
    # Pass the data to the template or return it as a JSON response
    file_path = os.path.join(settings.BASE_DIR, 'data', 'doctors.csv')
    
    doctors = set()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)[0:100]
        for row in csv_reader:
            if row['hospital_name'] == hospital_name:
                doctors.add(row)
        if len(doctors) == 0:
            doctors.add('Not hospitals in the DATASET')

    context = {'doctors': doctors}
    return JsonResponse(context)
@login_required
@csrf_exempt
def search_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        hospital=data['hospital']
        specialty = data['specialty']

        file_path = os.path.join(settings.BASE_DIR, 'data', 'doctors.csv')
        # Open and read the CSV file
        results = []
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            if hospital != '' and specialty != '':
                for row in csv_reader:
                    if(row['hospital_name'] == hospital and row['specialty']==specialty):
                        results.append(row['doctor_name'])
                if len(results) == 0:
                    results.append('Not found')
            elif hospital == '' and specialty!='':
                for row in csv_reader:
                    if(row['specialty']==specialty):
                        results.append(row['doctor_name'])
                if len(results) == 0:
                    results.append('Not found')
            elif specialty == '' and hospital!='':
                for row in csv_reader:
                    if(row['hospital_name'] == hospital):
                        results.append(row['doctor_name'])
                if len(results) == 0:
                    results.append('Not found')
            else:
                for row in csv_reader:
                    results.append(row['doctor_name'])
                if len(results) == 0:
                    results.append('Not found')
        return JsonResponse({'results':results})

@login_required
@csrf_exempt
def retrieve_history(request):
    if request.method == 'POST':
        patient_number = json.loads(request.body)['patientNumber']

    file_path = os.path.join(settings.BASE_DIR,'data','patient-history.csv')
    history = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row['patient_number']) == patient_number:
                history.append(row)
    file_path = os.path.join(settings.BASE_DIR, 'data', 'patients.csv')
    # Open and read the CSV file
    personalInfo = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if(int(row['patient_number']) == patient_number):
                personalInfo.append(row)

    return JsonResponse({'history':history,'info':personalInfo})

@login_required
@csrf_exempt
def search(request):
    if request.method == 'POST':
        search_phrase = json.loads(request.body)['searchPhrase']
    
        file_path = os.path.join(settings.BASE_DIR, 'data', 'patients.csv')
        # Open and read the CSV file
        results = []
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if(search_phrase in row['patient_number'].lower() or search_phrase.lower() in row['name'].lower()):
                    results.append(row)
            if len(results) == 0:
                results.append('Not found')

        return JsonResponse({'results':results})

@login_required
@csrf_exempt
def search_notifications(request):
    if request.method == 'POST':
        search_phrase = json.loads(request.body)['searchPhrase']
    
        file_path = os.path.join(settings.BASE_DIR, 'data', 'notifications.csv')
        # Open and read the CSV file
        results = []
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if((search_phrase in row['patient_number'].lower() or search_phrase.lower() in row['name'].lower())and row['pk']==request.user.pk):
                    results.append(row)
            if len(results) == 0:
                results.append('Not found')

        return JsonResponse({'results':results})

@login_required
@csrf_exempt
def search_service_provider(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data, data['hospital'], data['specialty'])
        search_phrase = data['searchPhrase']
        hospital = data['hospital']
        specialty = data['specialty']
        file_path = os.path.join(settings.BASE_DIR, 'data', 'doctors.csv')

        # Open and read the CSV file
        results = []
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            if hospital != '' and specialty != '':
                for row in csv_reader:
                    if row and (search_phrase in str(row.get('doctor_number', '')) or search_phrase.lower() in str(row.get('doctor_name', '')).lower()) and row['hospital_name'] == hospital and row['specialty'] == specialty:
                        results.append(row)
                if not results:
                    results.append('Not found')

            elif hospital == '' and specialty != '':
                for row in csv_reader:
                    if row and (search_phrase in str(row.get('doctor_number', '')) or search_phrase.lower() in str(row.get('doctor_name', '')).lower()) and row['specialty'] == specialty:
                        results.append(row)
                if not results:
                    results.append('Not found')

            elif specialty == '' and hospital != '':
                for row in csv_reader:
                    if row and (search_phrase in str(row.get('doctor_number', '')) or search_phrase.lower() in str(row.get('doctor_name', '')).lower()) and row['hospital_name'] == hospital:
                        results.append(row)
                if not results:
                    results.append('Not found')

            else:
                for row in csv_reader:
                    if row and (search_phrase in str(row.get('doctor_number', '')) or search_phrase.lower() in str(row.get('doctor_name', '')).lower()):
                        results.append(row)
                if not results:
                    results.append('Not found')

        return JsonResponse({'results': results})

@login_required
@csrf_exempt
def send_sms_message(request):
    if request.method == 'POST':
        #get the details: 
        details = json.loads(request.body)
        """
        {
        name,
        patient_number,
        refferalDoctor,
        waiting number
        }
        """
        PHONE_NUMBER = os.getenv('PHONE_NUMBER')
        TWILIO_ACCOUNT_SID = os.getenv('ACC_SID')
        TWILIO_AUTH_TOKEN = os.getenv('AUTH_TOKEN')
        TWILIO_MESSAGE_SERVICE_SID = os.getenv('MESSAGING_SERVICE')

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print(client, TWILIO_AUTH_TOKEN)

 # Extract the values from the details object
        name = details.get('name')
        patient_number = details.get('patient_number')
        referral_doctor = details.get('refferalDoctor')
        waiting_number = details.get('waiting_number')
        hospital = details.get('hospital')

        # Prepare the referral message
        referral_message = f"{name}, upon evaluating your condition, we reffer you to {referral_doctor} of {hospital} for further care. The hospital has specialists who can better manage your condition. Please take your medical records with you, your waiting number is {waiting_number}."
        message = client.messages.create(
        messaging_service_sid=TWILIO_MESSAGE_SERVICE_SID,
        body=referral_message,
        to='+254702716555'
)
        print(message.sid)
        return JsonResponse({'message':'message successfully sent to patient'})

@login_required
@csrf_exempt
def service_providers(request):
    curr_user_pk = int(request.user.pk)
    print(curr_user_pk)

    file_path = os.path.join(settings.BASE_DIR, 'data', 'notifications.csv')

    # Open and read the CSV file
    notifications = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if(curr_user_pk == int(row['pk'])):
                if row['urgency'] == "high":
                    row.update({'urgency_color':"red"})
                elif row['urgency'] == "medium":
                    row.update({'urgency_color':"yellow"})
                else:
                    row.update({'urgency_color':"green"})

                notifications.append(row)

    if len(notifications) == 0:
        notifications.append('No notifications for now')

    file_path = os.path.join(settings.BASE_DIR, 'data', 'doctors.csv')
    specialty = set()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            specialty.add(row['specialty'])

    if len(specialty) == 0:
        specialty.add('Not hospitals in the DATASET')

    file_path = os.path.join(settings.BASE_DIR, 'data', 'Health_facilities(Health_facilities_0).csv')
    hospitals = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for i, row in enumerate(csv_reader):
            if i < 100:  # Limit to the first 50 rows
                hospitals.append({'name': row['Facility Name'], 'lat': row['Latitude'], 'long': row['Longitude'],'level':row['Agency']})
            else:
                break

    if len(hospitals) == 0:
        hospitals.append('Not hospitals in the DATASET')

    return render(request, "carelink/service-providers.html", {"notifications": notifications, "hospitals": hospitals, "specialties": specialty})

@login_required
def profile(request):
    file_path=os.path.join(settings.BASE_DIR,'media')
    user = request.user

    try:
        Profile = User_profile.objects.filter(user=user)
        print(Profile.__dict__)
    except ObjectDoesNotExist:
        Profile = None 

    return render(request, 'carelink/profile.html', {'user': user, 'Profile': Profile})

def save_profile_changes(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect to the user's profile page
        else:
            messages.error(request, 'There was an error updating your profile. Please try again.')
            return redirect('profile')  # Redirect back to the profile page with error messages
    else:
        # This view should only handle POST requests
        return redirect('profile')  # Redirect 

#generate reports based on 
@login_required
def generate_report(request):
    file_path = os.path.join(settings.BASE_DIR,'data','patient-history.csv')
    pdf = FPDF()
    pdf.add_page()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            ##add this to the urls
            ##check doc number from dataset is equal to the current user pk
            if int(row['doctor_number']) == request.user.pk:
                pdf.text
    pdf.output('test.pdf','D')


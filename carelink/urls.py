from os import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register , name='register'),
    path('login/', views.login_view , name='login'),
    path('profile/', views.profile, name='profile'),
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('logout',views.logout,name = "logout" ),
    #urls for sending messages
    path('send_message/', views.send_message, name='send_message'),
    path('check_messages/', views.check_messages, name='check_messages'),
    path('patients/',views.patients,name='patients'),
    path('service_providers/',views.service_providers,name="service_providers"),
    path('retrieve_history/',views.retrieve_history,name="retrieve_history"),
    path('search/',views.search,name="search"),
    path('send_sms/',views.send_sms_message,name="send_sms_message"),
    path('search_notifications/',views.search_notifications,name="search_notifications"),
    path('search_service_provider/',views.search_service_provider,name="search_provider"),
    path('get_doctor_in_hospital/',views.get_doctor_in_hospital,name="get_doctor_in_hospital"),
    path('search_doctor/',views.search_doctor,name="search_doctor")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register , name='register'),
    path('login/', views.login_view , name='login'),
    path('profile/', views.profile, name='profile'),
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    
    path('dashboard/', views.dashboard , name='dashboard'),
    path('logout/',views.logout,name = "logout" ),
    #urls for sending messages (to implement later)
    # path('chat/<str:room>/', views.room, name='room'),
#     path('checkview/', views.checkview, name='checkview'),
#     path('send', views.send, name='send'),
#     path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
# 
]


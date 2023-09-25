# students/urls.py
from django.urls import path
from .views import  freeSessions, login, studentsignup,createSession,deansignup,bookSession,pendingSessions

urlpatterns = [
    path('login/', login, name='student-login'),
    path('studentsignup/', studentsignup, name='student-login'),
    path('deansignup/', deansignup, name='student-login'),
    path('list-free-sessions/',freeSessions , name='list-free-sessions'),
    path('create-session/',createSession , name='create-session'),
    path('book-session/',bookSession , name='book-session'),
    path('pending-sessions/',pendingSessions , name='pending-session'),
]

# students/views.py
from rest_framework import generics,status
from .models import  Session
from .serializers import  SessionSerializer,UserSerializer,SessionViewSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.models import Group, Permission, Group
from datetime import datetime


# used to get list of available sessions by student
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def freeSessions(request):
    user = Token.objects.get(key=request.auth.key).user

    if(User.objects.filter(username=user, groups__name='Student').exists()):
        sessions = Session.objects.filter(booked=False)
        serializer = SessionViewSerializer(sessions, many=True)
        return Response(serializer.data)
    else:
        return Response("forbidden", status=status.HTTP_403_FORBIDDEN)


# used to view pending sessions by dean
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def pendingSessions(request):
    user = Token.objects.get(key=request.auth.key).user
    if(User.objects.filter(username=user, groups__name='Dean').exists()):
        sessions = Session.objects.filter(booked=True,start_time__gte=datetime.today(),dean=user)
        serializer = SessionViewSerializer(sessions, many=True)
        return Response(serializer.data)
    else:
        return Response("forbidden", status=status.HTTP_403_FORBIDDEN)

# used to create session by deans
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createSession(request):
    user = Token.objects.get(key=request.auth.key).user
    if(User.objects.filter(username=user, groups__name='Dean').exists()):
        request.data['dean'] = User.objects.get(username=user).id

        date = datetime.strptime(request.data['start_time'], '%Y-%m-%dT%H:%M:%S')
        if( (date.strftime("%A") in ["Thursday","Friday"]) and (int(date.strftime("%H")) >= 10) ):
            serializer = SessionSerializer(data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response("Created session succesfully", status=status.HTTP_201_CREATED)
        else:
            return Response("please select only thurday or friday after 10 AM", status=status.HTTP_409_CONFLICT)
    else:
        return Response("forbidden", status=status.HTTP_403_FORBIDDEN)


# used to book session for students
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookSession(request):
    user = Token.objects.get(key=request.auth.key).user
    if(User.objects.filter(username=user, groups__name='Student').exists()):
        session = Session.objects.get(id=request.data["session_id"])
        setattr(session,"student",User.objects.get(username=user))
        setattr(session,"booked",True)
        session.save()
        return Response("Success",status=status.HTTP_200_OK)
    else:
        return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)


# used for student sign up
@api_view(['POST'])
def studentsignup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['university_id'])
        user.set_password(request.data['password'])
        
        group = Group.objects.get(name="Student")
        user.groups.add(group)
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

# used for dean sign up
@api_view(['POST'])
def deansignup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['university_id'])
        user.set_password(request.data['password'])
        group = Group.objects.get(name="Dean")
        user.groups.add(group)
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

# used for login for all members
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['university_id'])
    if not user.check_password(request.data['password']):
        return Response("Invalid user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

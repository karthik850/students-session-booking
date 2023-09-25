# students/serializers.py
from rest_framework import serializers
from .models import Session
from django.contrib.auth.models import User


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class SessionViewSerializer(serializers.ModelSerializer):
    dean = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    session_id = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ["session_id","date","time","dean","student"]
    def get_dean(self, obj):
        return obj.dean.username
    def get_student(self, obj):
        if(obj.student) :
            return obj.student.username
        else: 
            return None
    def get_session_id(self, obj):
        return obj.id
    def get_date(self, obj):
        return obj.start_time.strftime("%x")
    def get_time(self, obj):
        return obj.start_time.strftime("%X")
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}


class UserSerializer(serializers.ModelSerializer):
    university_id = serializers.CharField(source='username')
    class Meta(object):
        model = User 
        fields = ['id', 'university_id', 'password']

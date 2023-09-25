from django.db import models
import uuid
from django.contrib.auth.models import User
import json

class Session(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="student")
    dean = models.ForeignKey(User, on_delete=models.CASCADE,related_name="dean")
    start_time = models.DateTimeField()
    booked = models.BooleanField(default=False)

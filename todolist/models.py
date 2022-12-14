from django.db import models 
from django.contrib.auth.models import User
from datetime import datetime

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.TextField()
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
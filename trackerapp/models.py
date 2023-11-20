from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.

medicine_choices = [
    ('Ibuprofen','Ibuprofen'),
    ('Paracetamol','Paracetamol'),
    ('Zyrtec','Zyrtec'),
    ('Cetirizine','Cetirizine'),
    ('Promethazine','Promethazine'),
    ('Ivy Leaf Extract','Ivy Leaf Extract'),
]

class EatModel(models.Model):
    # user is one to many 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    medicine = models.CharField(max_length=50, choices=medicine_choices)
    last_fed = models.DateTimeField(default=datetime.now)
    interval = models.IntegerField(default=4)
    remarks = models.TextField(max_length=140)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.medicine
    
    class Meta:
        ordering = ['complete'] #ordering in descending just do -complete
        
class MedicalInfo(models.Model):
    medicine = models.CharField(max_length=50, choices=medicine_choices)
    rec_interval = models.IntegerField(null=False)
    description = models.TextField(max_length=500)
    used_for = models.TextField(max_length=500, default="")
    sideeffects = models.TextField(max_length=500)
    
    def __str__(self):
        return self.medicine
    
    
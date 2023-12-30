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

class MedicalInfo(models.Model):
    medicine = models.CharField(max_length=50, choices=medicine_choices)
    rec_interval = models.IntegerField(null=False)
    description = models.TextField(max_length=500)
    used_for = models.TextField(max_length=500, default="")
    sideeffects = models.TextField(max_length=500)
    brandname = models.TextField(max_length=500, default="", null=True)
    
    def __str__(self):
        return self.medicine
    
class EatModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    medicine = models.ForeignKey(MedicalInfo, on_delete=models.SET_NULL, null=True)
    interval = models.IntegerField(default=4)
    last_fed = models.DateTimeField(default=datetime.now)
    second_dose = models.DateTimeField(default=None, null=True)
    third_dose = models.DateTimeField(default=None, null=True)
    fourth_dose = models.DateTimeField(default=None, null=True)
    fifth_dose = models.DateTimeField(default=None, null=True)
    remarks = models.TextField(max_length=140, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return str(self.id)

    @property
    def get_second_dose(self):
        a = self.last_fed + timedelta(hours=self.interval)
        return a  
     
    @property
    def get_third_dose(self):
        b = self.last_fed + timedelta(hours=self.interval) * 2
        return b  
     
    @property
    def get_fourth_dose(self):
        c = self.last_fed + timedelta(hours=self.interval) * 3
        return c      
    
    @property
    def get_fifth_dose(self):
        d = self.last_fed + timedelta(hours=self.interval) * 4
        return d
    
    def save(self, *args, **kwargs):
        self.second_dose = self.get_second_dose
        self.third_dose = self.get_third_dose
        self.fourth_dose = self.get_fourth_dose
        self.fifth_dose = self.get_fifth_dose
        super(EatModel, self).save(*args, **kwargs)
          
    class Meta:
        ordering = ['complete'] #ordering in descending just do -complete

class Patient(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, default=None)
    parent = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.name)  
    
class CourseInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    medicine = models.ForeignKey(MedicalInfo, on_delete=models.SET_NULL, null=True)
    interval = models.IntegerField(default=4)
    course_duration = models.IntegerField(default=3)
    course_start = models.DateTimeField(default=datetime.now)
    complete = models.BooleanField(default=False)
    course_created = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
        
    def __str__(self):
        return str(self.id)
    
class DoseInfo(models.Model):
    courseinfo = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, default='')
    dose_timing = models.DateTimeField(default=datetime.now)
    dose_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['dose_timing']
        
    def __str__(self):
        return str(self.id)


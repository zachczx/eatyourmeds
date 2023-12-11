from django.contrib import admin
from .models import EatModel, MedicalInfo 
from .models import CourseInfo, DoseInfo

# Register your models here.

admin.site.register(EatModel)
admin.site.register(MedicalInfo)
admin.site.register(CourseInfo)
admin.site.register(DoseInfo)
from django import forms
from .models import CourseInfo, DoseInfo

class BetaCourseForm(forms.ModelForm):
    class Meta:
        fields = ['medicine', 'interval', 'course_duration', 'course_start']
        model = CourseInfo

class BetaDoseForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = DoseInfo

class BetaDoseHtmxForm(forms.ModelForm):
    class Meta:
        fields = ['dose_timing']
        model = DoseInfo

class BetaDoseAutoForm(forms.ModelForm):
    class Meta:
        fields = []
        model = DoseInfo
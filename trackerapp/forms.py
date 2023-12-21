from django import forms
from .models import CourseInfo, DoseInfo
#crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, MultiField, Submit, Div, Button
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.urls import reverse_lazy, reverse

class BetaCourseForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = CourseInfo
        labels = {
            'interval': 'Number of hours in between each dose:',
            'course_duration': 'Number of days to take the medicine:',
            'course_start': 'Date/time you first ate the medicine:',
            "patient": "Who's eating the medicine?",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Hi {{form_user}}! Give me some details of the medicine to start:',
            ),
            Div(
                Div('medicine', css_class='col-sm-6'),
                Div('patient', css_class='col-sm-6'),
                css_class='row pt-3 pb-4',
            ),
            Div(
                Div(AppendedText('interval', 'hours'), css_class='col-sm-6'),
                Div(AppendedText('course_duration', 'days'), css_class='col-sm-6'),
                css_class='row pb-4',
            ),
            Div(
                'course_start',
                css_class='row pb-4',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='text-white fw-bold'),
                Button('cancel', 'Cancel', css_class='btn btn-outline-secondary'),
            ),
        )

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
        
class BetaUserCreateForm(UserCreationForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'username',
                css_class='row pb-4',
            ),
            Div(
                'email',
                css_class='row pb-4',
            ),
            Div(
                Div('password1', css_class='col-sm-6'),
                Div('password2', css_class='col-sm-6'),
                css_class='row pb-4',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='text-white fw-bold'),
                Button('cancel', 'Cancel', css_class='btn btn-outline-secondary'),
            ),
        )
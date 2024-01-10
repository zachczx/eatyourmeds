from django import forms
from .models import Sequence, Session, Worker
#crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Reset, Div, Row, Column
from crispy_forms.bootstrap import FormActions
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.urls import reverse_lazy, reverse

class WorkerForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'session', 'dept']
        model = Worker
        labels = {
            'name': 'Name:',
            'session': 'Which session:',
            'dept': 'Dept:',
        }
        
    def __init__(self, user=None, *args, **kwargs):
        self.patient = Worker.objects.filter(parent=user)
        super(WorkerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Hi {{form_user}}! Let\'s start with adding someone:',
            ),
            Div(
                Div('session', css_class='col-sm-4'),
                Div('name', css_class='col-sm-4'),
                Div('dept', css_class='col-sm-4'),
                css_class='row pt-3 pb-4',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='text-white fw-bold'),
                Reset('cancel', 'Cancel', css_class='btn btn-outline-secondary'),
            ),
        )

class HtmxAddWorker(forms.ModelForm):
    class Meta:
        fields = ['name', 'dept']
        model = Worker
        labels = {
            'name': 'Name:',
            'dept': 'Dept:',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('name', placeholder='Name', css_class='form-group col-4 mx-0'),
                ),
                Column(
                    Field('dept', placeholder='Dept', css_class='form-group col-4 mx-0'),
                ),
                Column(Submit('submit', 'Submit', css_class='btn-primary fw-bold col-4')),
                css_class='d-flex align-items-top'
            ),

        )
        self.helper.form_show_labels = False
'''
Div(
    Div('name', css_class='col-sm-3'),
    Div('dept', css_class='col-sm-3'),
    FormActions(
        Submit('submit', 'Submit', css_class='text-white fw-bold'),
    ),
    css_class='row',
),
'''
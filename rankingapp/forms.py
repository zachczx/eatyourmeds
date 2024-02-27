from django import forms
from .models import Sequence, Session, Worker
#crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Reset, Div, Row, Column
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse, reverse_lazy 

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
        fields = ['name', 'dept', 'prev']
        model = Worker
        labels = {
            'name': 'Name:',
            'dept': 'Dept:',
            'prev': 'Prev Grade',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('name', placeholder='Name', css_class='form-group col-3 mx-0'),
                ),
                Column(
                    Field('dept', placeholder='Dept', css_class='form-group col-2 mx-0'),
                ),
                Column(
                    Field('prev', placeholder='Prev grade', css_class='form-group col-2 mx-0'),
                ),
                Column(
                    Submit('submit', 'Add', css_class='btn-primary fw-bold col-5 mx-0'),
                ),
                css_class='d-flex align-items-top',
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

class GetSessionForm(forms.ModelForm):
    class Meta:
        fields = ['user_defined']
        model = Session
        labels = {
            'user_defined': 'Session ID:',
        }
        widgets = {
            'user_defined': forms.TextInput(attrs={
                'hx-get': reverse_lazy('htmx_existing_session'),
                'hx-target': '#htmx_existing_session',
                'hx-trigger': 'keyup[target.value.length > 0] delay:0s', #this was formerly 0.3s
                'placeholder': 'Continue where you left out last time',
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons('user_defined', StrictButton("Return", css_class="btn-primary", type="submit", id="button-existing"), input_size="input-group-sm"),
        )
        self.helper.form_show_labels = False

class NewSession(forms.ModelForm):
    class Meta:
        fields = ['user_defined']
        model = Session
        labels = {
            'user_defined': 'Session ID:',
        }
        widgets = {
            'user_defined': forms.TextInput(attrs={
                'hx-get': reverse_lazy('htmx_validate_session'),
                'hx-target': '#htmx_validate_session',
                'hx-trigger': 'keyup[target.value.length > 0] delay:0s', #this was formerly 0.3s
                'placeholder': 'Start a session using a unique ID',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FieldWithButtons('user_defined', StrictButton("Start", css_class="btn-primary", type="submit", id="button-new"), )
        )
        self.helper.form_show_labels = False
        
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('user_defined', placeholder='New ID', css_class='form-group col-8 mx-0'),
                ),
                Column(Submit('submit', 'Create!', css_class='btn-primary fw-bold col-4 mx-0')),
                css_class='d-flex align-items-top g-0'
            ),
        )
        
        self.helper.form_show_labels = False
    '''

class HtmxSaveSequence(forms.ModelForm):
    class Meta:
        fields = ['sequence']
        model = Session
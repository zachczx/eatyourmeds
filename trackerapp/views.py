from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
#from django.http import HttpResponse

from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login # to login right after creating account
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.admin.widgets import AdminDateWidget
from django.urls import reverse_lazy
from .models import EatModel, MedicalInfo

from django.utils.timezone import datetime, timedelta

from django.views.generic.base import TemplateView #for newlist class
from django.db.models import FilteredRelation

# Create your views here.

class EatLogin(LoginView):
    template_name = 'trackerapp/registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('eatlist')

class EatLogout(LogoutView):
    next_page = 'eatlogin'    

class EatRegister(FormView):
    template_name = 'trackerapp/registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('eatlist')
    
    def form_valid(self, form):
        user = form.save() # this is user cos we are working with usercreationform 
        if user != None:
            login(self.request, user)
        return super(EatRegister, self).form_valid(form)
    
    # validate and then redirect using login()
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:      
            #import redirect
            return redirect('eatlist')
        return super(EatRegister, self).get(*args, **kwargs)
    
class EatDetails(LoginRequiredMixin, DetailView):
    login_url = 'eatlogin'
    model = EatModel
    context_object_name = 'outstanding_list'  #this allows me to call it from the details page, outstanding_list.id

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['tasks'] = EatModel.objects.filter(user=self.request.user)
#        return context

class EatCreate(LoginRequiredMixin, CreateView):
    model = EatModel
    fields = ['medicine', 'remarks', 'last_fed', 'interval', 'complete']
    success_url = reverse_lazy('eatlist')
    
    #for date picking
    #def get_form(self, form_class=None):
    #    form = super(EatCreate, self).get_form(form_class)
    #    form.fields['last_fed'].widget = AdminDateWidget(attrs={'type': 'date'})
    #    return form
    
    # after form is submitted, checks if user submitting matches the user in the form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EatCreate, self).form_valid(form)
    
class EatUpdate(LoginRequiredMixin, UpdateView):
    model = EatModel
    fields = ['medicine', 'remarks', 'last_fed', 'interval', 'complete']
    success_url = reverse_lazy('eatlist')

class EatDelete(LoginRequiredMixin, DeleteView):
    model = EatModel
    fields = ['medicine', 'remarks', 'interval', 'complete']
    context_object_name = 'outstanding_list'
    success_url = reverse_lazy('eatlist')    

########### my own func views ###################

def MakeNextDoses(userpk):
    alldetails = EatModel.objects.filter(pk=userpk).values()
    hrs = alldetails[0]['interval'] #putting this here to avoid doing another filter
    doses_per_day = int(24 / hrs)

    first_dose = EatModel.objects.filter(id=userpk).values_list('last_fed', flat=True)
    second_dose = first_dose[0] + timedelta(hours=hrs)
    third_dose = second_dose + timedelta(hours=hrs)
    fourth_dose = third_dose + timedelta(hours=hrs)
    dose = {
        'doses_per_day': doses_per_day,
        'doses_timings': [first_dose[0], second_dose, third_dose, fourth_dose],
        'user_id': alldetails[0]['user_id'], #I used this to check user_id later
    }
    return dose 

def GetMedicalInfo(userpk):
    alldetails = EatModel.objects.filter(pk=userpk).values()
    get_medical_info = MedicalInfo.objects.filter(id=alldetails[0]['medicine_id']).values()
    return get_medical_info

def nextDose(request, pk=None):
    if request.user.is_authenticated is True:
        ### display if authenticated ###
        next_four_doses = MakeNextDoses(pk)
        ### checks if requestor is owner of record ###
        if request.user.id == next_four_doses['user_id']:
            medical_info = GetMedicalInfo(pk) 
            context = {
                'next_four_doses': next_four_doses,
                'medical_info': medical_info,
            }
            return render(request, 'trackerapp/dose.html', context)
         ### redirects if not ###
        else:
            return redirect('eatlist') 
        ### redirects to register if not logged in ###
    else:
        return redirect('eatregister')
    
class newlist(LoginRequiredMixin, TemplateView):
    
    template_name = 'trackerapp/eatmodel_newlist.html'
    login_url = 'eatlogin'
    
    #filter to only contain the user's data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = EatModel.objects.filter(user=self.request.user)
        #context['medicine'] = MedicalInfo.objects.all()
        return context
    
##################################
'''
#original code for nextDose before I split it up

def nextDose(request, pk=None):

    if request.user.is_authenticated is True:
       
        alldetails = EatModel.objects.filter(pk=pk).values()
        hrs = alldetails[0]['interval'] #putting this here to avoid doing another filter
        number_of_times = int(24 / hrs)
        if request.user.id == alldetails[0]['user_id']: #check if user is the creator of the record
            first_dose = EatModel.objects.filter(id=pk).values_list('last_fed', flat=True)
            first_dose = first_dose[0]
            second_dose = first_dose + timedelta(hours=hrs)
            third_dose = second_dose + timedelta(hours=hrs)
            fourth_dose = third_dose + timedelta(hours=hrs)
            
            #second_dose = datetime.strptime(list_result, "%Y, %m, %d %H:%M:%S")
            dose = [first_dose, second_dose, third_dose, fourth_dose]
            
            #get the info from MedicalInfo Model
            #get_type_medicine = EatModel.objects.filter(pk=pk).values_list('medicine', flat=True)
            #get_type_medicine = get_type_medicine[0]
            #medical_info = MedicalInfo.objects.filter(medicine=get_type_medicine).values()


            medical_info = MedicalInfo.objects.filter(id=alldetails[0]['medicine_id']).values()

            context = {
                'dose': dose,
                'alldetails': alldetails,
                'medical_info': medical_info,
                'number_of_times': number_of_times,
            }
        else:
            return redirect('eatlist') #redirects user who tried to access someone else's records
        
        return render(request, 'trackerapp/dose.html', context) #for some reason need to access via {{ details.0.medicine }}
        
    else:
        return redirect('eatregister')

from django.views.generic.list import ListView
class EatList(LoginRequiredMixin, ListView):
    model = EatModel
    context_object_name = 'outstanding_list'
    fields = ['medicine', 'remarks', 'last_fed', 'interval', 'complete']
    login_url = "eatlogin"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["outstanding_list"] = context["outstanding_list"].filter(user=self.request.user)
        context["count"] = context["outstanding_list"].filter(complete=False).count()
        return context    

'''
    
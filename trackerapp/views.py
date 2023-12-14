from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
#from django.http import HttpResponse

from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login # to login right after creating account
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.admin.widgets import AdminDateWidget
from django.urls import reverse_lazy, reverse
from .models import EatModel, MedicalInfo

#beta version stuff
from .models import CourseInfo, DoseInfo
from .forms import BetaCourseForm, BetaDoseForm, BetaDoseHtmxForm, BetaDoseAutoForm
from django.views.generic.list import ListView
from .utils import Calendar
from django.utils.safestring import mark_safe

#from datetime import datetime as core_datetime #for the sorting by time
#from django.db.models import Q #for query multiply columns

from django.utils.timezone import datetime, timedelta, localtime #localtime to do subtraction

from django.views.generic.base import TemplateView #for newlist class
from django.db.models import FilteredRelation

# Create your views here.

class EatLogin(LoginView):
    template_name = 'trackerapp/registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('newlist')

class EatLogout(LogoutView):
    next_page = 'eatlogin'    

class EatRegister(FormView):
    template_name = 'trackerapp/registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('newlist')
    
    def form_valid(self, form):
        user = form.save() # this is user cos we are working with usercreationform 
        if user != None:
            login(self.request, user)
        return super(EatRegister, self).form_valid(form)
    
    # validate and then redirect using login()
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:      
            #import redirect
            return redirect('newlist')
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
    success_url = reverse_lazy('newlist')
    
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
    #success_url = reverse_lazy('doseview')

    def get_success_url(self):
        return reverse('doseview', kwargs={"pk": self.kwargs.get('pk')})

class EatDelete(LoginRequiredMixin, DeleteView):
    model = EatModel
    fields = ['medicine', 'remarks', 'interval', 'complete']
    context_object_name = 'outstanding_list'
    success_url = reverse_lazy('newlist')    

@require_http_methods(['DELETE'])
def htmx_delete(request, id):
    EatModel.objects.filter(id=id).delete()
    list = EatModel.objects.filter(user=request.user).all()
    return render(request, "trackerapp/partials/eatmodel_newlist_content.html", {'list': list})

class DoseView(LoginRequiredMixin, DetailView):

    model = EatModel
    template_name = 'trackerapp/eatmodel_dose.html'
    login_url = 'eatlogin'
    context_object_name = 'nextfewdoses'
    
    def get_context_data(self, *args, **kwargs):
        context = super(DoseView, self).get_context_data(*args, **kwargs)
        context['doses_per_day'] = int(24 / self.object.interval)
        #key = [self.object.second_dose, self.object.third_dose, self.object.fourth_dose, self.object.fifth_dose]
        #newkey = []
        #for v in key:
        #    time_remaining = v + timedelta(hours=72)
        #    newkey.append(time_remaining)
        #context['dose_differential'] = newkey
        now = localtime()
        
        #get number of hours
        last_fed_in_hrs = float((self.object.last_fed - now).total_seconds())/3600
        second_dose_in_hrs = float((self.object.second_dose - now).total_seconds())/3600
        third_dose_in_hrs = float((self.object.third_dose - now).total_seconds())/3600
        fourth_dose_in_hrs = float((self.object.fourth_dose - now).total_seconds())/3600
        
        if last_fed_in_hrs < 0:
            context['last_fed_alert_status'] = "secondary"
        elif 0 < last_fed_in_hrs < self.object.interval: 
            context['last_fed_alert_status'] = "danger"
        else:
            context['last_fed_alert_status'] = "success"
            
        if second_dose_in_hrs < 0:
            context['second_dose_alert_status'] = "secondary"
        elif 0 < second_dose_in_hrs < self.object.interval: 
            context['second_dose_alert_status'] = "danger"
        else:
            context['second_dose_alert_status'] = "success"
            
        if third_dose_in_hrs < 0:
            context['third_dose_alert_status'] = "secondary"
        elif 0 < third_dose_in_hrs < self.object.interval: 
            context['third_dose_alert_status'] = "danger"
        else:
            context['third_dose_alert_status'] = "success"
        
        if fourth_dose_in_hrs < 0:
            context['fourth_dose_alert_status'] = "secondary"
        elif 0 < fourth_dose_in_hrs < self.object.interval: 
            context['fourth_dose_alert_status'] = "danger"
        else:
            context['fourth_dose_alert_status'] = "success"
            
        '''
        # these were for printing the time remaining statically
        if self.object.last_fed > now:
            key = str(self.object.last_fed - now)
            splitkey = key.split(":")
            context['remaining_last_fed'] = splitkey[0] + " hrs " + splitkey[1] + " mins "
        else:
            context['remaining_last_fed'] = "over"
            
        if self.object.second_dose > now:
            key = str(self.object.second_dose - now)
            splitkey = key.split(":")
            context['remaining_second_dose'] = splitkey[0] + " hrs " + splitkey[1] + " mins "
        else:
            context['remaining_second_dose'] = "over"
            
        if self.object.third_dose > now:
            key = str(self.object.third_dose - now)
            splitkey = key.split(":")
            context['remaining_third_dose'] = splitkey[0] + " hrs " + splitkey[1] + " mins "
        else:
            context['remaining_third_dose'] = "over"
        
        if self.object.fourth_dose > now:
            key = str(self.object.fourth_dose - now)
            splitkey = key.split(":")
            context['remaining_fourth_dose'] = splitkey[0] + " hrs " + splitkey[1] + " mins "
        else:
            context['remaining_fourth_dose'] = "over"
        '''
        return context
    
class newlist(LoginRequiredMixin, TemplateView):
    
    template_name = 'trackerapp/eatmodel_newlist.html'
    login_url = 'eatlogin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = localtime()
        context['list'] = EatModel.objects.filter(user=self.request.user)
                
        '''
        q = {}
        for item in context['list']:
            if item.second_dose > t and item.third_dose > t and item.fourth_dose > t and item.fifth_dose > t:
                q[item.id] = ['True', 'True', 'True', 'True']
            elif item.second_dose < t and item.third_dose > t and item.fourth_dose > t and item.fifth_dose > t:
                q[item.id] = ['False', 'True', 'True', 'True']
            elif item.second_dose < t and item.third_dose < t and item.fourth_dose < t and item.fifth_dose > t:
                q[item.id] = ['False', 'False', 'True', 'True']    
            elif item.second_dose < t and item.third_dose < t and item.fourth_dose < t and item.fifth_dose > t:
                q[item.id] = ['False', 'False', 'False', 'True']    
        context['dose_status'] = q
        '''
        return context
#################################

'''
def newcourse(request):
    
    if request.method == 'POST':

        eatmodel_form = EatModelForm(request.POST)
        dosesinfo_form = DosesInfoForm(request.POST)

        if eatmodel_form.is_valid() and dosesinfo_form.is_valid():

            eatmodel_form.save()
            dosesinfo_form.save()
            return HttpResponseRedirect('newlist')        

        else:
            context = {
                'eatmodel_form': eatmodel_form,
                'dosesinfo_form': dosesinfo_form,
            }

    else:
        context = {
            'eatmodel_form': EatModelForm(),
            'dosesinfo_form': DosesInfoForm(),
        }

    return render(request, 'trackerapp/create_timings.html', context)
'''

class BetaCreateCourse(LoginRequiredMixin, CreateView):
    template_name = 'trackerapp/betacreatecourse.html'
    form_class = BetaCourseForm
    success_url = reverse_lazy('betaviewdose')
    
    #to auto populate the form user created
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BetaCreateCourse, self).form_valid(form)
    
class BetaCreateDose(CreateView):
    template_name = 'trackerapp/betacreatedose.html'
    form_class = BetaDoseForm
    success_url = reverse_lazy('betaviewdose')
'''    
class BetaViewCourse(LoginRequiredMixin, DetailView):

    model = CourseInfo
    template_name = 'trackerapp/betaviewcourse.html'
    login_url = 'eatlogin'
    context_object_name = 'courseinfo'
    
    def get_context_data(self, *args, **kwargs):
        context = super(BetaViewCourse, self).get_context_data(*args, **kwargs)
        context['info'] = CourseInfo.objects.filter(pk=self.kwargs.get('pk')).select_related()
        now = localtime()
        q = CourseInfo.objects.filter(pk=self.kwargs.get('pk')).values()
        return context
'''
class BetaViewCourse(LoginRequiredMixin, ListView):

    model = CourseInfo
    template_name = 'trackerapp/betaviewcourse.html'
    login_url = 'eatlogin'
    context_object_name = 'courseinfo'

    def get_queryset(self):
        return CourseInfo.objects.filter(pk=self.kwargs.get('pk'))
 
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['doseinfo'] = DoseInfo.objects.filter(courseinfo_id=self.kwargs.get('pk')).order_by('dose_timing').values()      
        context['htmx_create_dose'] = BetaDoseHtmxForm()

        dose_dates = DoseInfo.objects.filter(courseinfo_id=self.kwargs.get('pk')).order_by('dose_timing').values_list('dose_timing', flat=True)
        #start_timing_calendar = DoseInfo.objects.filter(courseinfo_id=self.kwargs.get('pk')).order_by('dose_timing').values('dose_timing').first()
        if not dose_dates:
            pass
        else:
            start_timing_calendar_month = dose_dates[0].month
            start_timing_calendar_year = dose_dates[0].year
            cal = Calendar(start_timing_calendar_year, start_timing_calendar_month)
            html_cal = cal.formatmonth(withyear=True)
            context['calendar'] = mark_safe(html_cal)
        return context
    
def htmx_create_dose(request, id):
    
    form = BetaDoseHtmxForm(request.POST or None)
    
    #if request.method == 'GET':    
    #    return render(request, 'trackerapp/htmx_create_dose.html', {'form': form})
    
    if request.method == 'POST':
        form.courseinfo = id  
        if form.is_valid():
            #fill in the course info automatically
            filled = form.save(commit=False)
            filled.courseinfo_id = id
            filled.save()
            courseinfo = CourseInfo.objects.filter(pk=id)
            doseinfo = DoseInfo.objects.filter(courseinfo_id=id).order_by('dose_timing').values()
            htmx_create_dose = BetaDoseHtmxForm()
                
            context = {
                'courseinfo': courseinfo,
                'doseinfo': doseinfo,
                'form': form,
                'htmx_create_dose': htmx_create_dose,
            }
            return render(request, 'trackerapp/htmx_view_dose.html', context)

@require_http_methods(['POST'])
def htmx_create_dose_auto(request, id):
    
    form = BetaDoseAutoForm(request.POST or None)
    
    #if request.method == 'GET':    
    #    return render(request, 'trackerapp/htmx_create_dose.html', {'form': form})
    
    # generate the dose timings
    qs = CourseInfo.objects.filter(pk=id).values('course_start','course_duration', 'interval')
    start_date = qs[0]['course_start']
    course_duration = qs[0]['course_duration']
    interval = qs[0]['interval']
    
    number_of_doses = int((course_duration * 24)/interval)
    local_time = localtime()

    new_doses = [
        DoseInfo(courseinfo_id=id, dose_timing=start_date, dose_created=local_time),
    ]
    
    i = 1
    
    while i < number_of_doses:
        start_date = start_date + timedelta(hours=interval)
        new_doses.append(DoseInfo(courseinfo_id=id, dose_timing=start_date, dose_created=local_time))
        i += 1
    
    if request.method == 'POST':

        if form.is_valid():
            objs = DoseInfo.objects.bulk_create(new_doses)
            url = reverse('betaviewcourse', kwargs={'pk':id})
            return HttpResponseRedirect(url)

@require_http_methods(['DELETE'])
def htmx_delete_dose(request, id, doseid):
    DoseInfo.objects.filter(id=doseid).delete()
    courseinfo = CourseInfo.objects.filter(pk=id)
    doseinfo = DoseInfo.objects.filter(courseinfo_id=id).order_by('dose_timing').values()
    context = {
        'courseinfo': courseinfo,
        'doseinfo': doseinfo,
    }
    return render(request, 'trackerapp/htmx_view_dose.html', context)            

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
                'findid': pk,
            }
            return render(request, 'trackerapp/dose.html', context)
         ### redirects if not ###
        else:
            return redirect('newlist') 
        ### redirects to register if not logged in ###
    else:
        return redirect('eatregister')
'''
    
from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
#from django.http import HttpResponse

from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout #new django 5.0 logout

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
from utils.mixins import CacheMixin

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
        return reverse_lazy('betamain')

def logout_view(request):
    logout(request)
    return redirect('betamain')
    # Redirect to a success page.

class EatRegister(FormView):
    template_name = 'trackerapp/registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('betamain')
    
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

class newlist(LoginRequiredMixin, TemplateView):
    
    template_name = 'trackerapp/eatmodel_newlist.html'
    login_url = 'eatlogin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = localtime()
        context['list'] = EatModel.objects.filter(user=self.request.user)
        return context


class BetaMain(LoginRequiredMixin, ListView):
    cache_timeout = 90
    template_name = 'trackerapp/betamain.html'
    model = CourseInfo
    context_object_name = 'courseinfo'
    
    def get_queryset(self):
        return CourseInfo.objects.filter(user=self.request.user).prefetch_related()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ########## start class based notif ########## 
        #datetoday = localtime()
        #context['datetoday'] = datetoday
        qs_id = CourseInfo.objects.filter(user=self.request.user).values('id')
        #context['notif'] = DoseInfo.objects.filter(courseinfo_id__in=qs_id).filter(
        #    dose_timing__year=datetoday.year,
        #    dose_timing__month=datetoday.month,
        #    dose_timing__day=datetoday.day
        #    ).select_related() #for notif
        #context['notif_count'] = len(context['notif'])
        ########## end class based notif ##########
        upcomingoneday = localtime() + timedelta(hours=8) #for main page content display 
        context['doseinfo'] = DoseInfo.objects.filter(courseinfo_id__in=qs_id).filter(dose_timing__gte=localtime()).filter(dose_timing__lte=upcomingoneday).select_related() #for main page content display        
        return context

class BetaCreateCourse(LoginRequiredMixin, CreateView):
    template_name = 'trackerapp/betacreatecourse.html'
    form_class = BetaCourseForm
    success_url = reverse_lazy('betaviewdose')
    
    #to auto populate the form user created
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BetaCreateCourse, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('betaviewcourse', kwargs={'pk': self.object.id})
    
class BetaCreateDose(CreateView):
    template_name = 'trackerapp/betacreatedose.html'
    form_class = BetaDoseForm

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
        context['doseinfo'] = DoseInfo.objects.filter(courseinfo_id=self.kwargs.get('pk')).values()      
        context['htmx_create_dose'] = BetaDoseHtmxForm()

        dose_dates = DoseInfo.objects.filter(courseinfo_id=self.kwargs.get('pk')).values_list('dose_timing', flat=True)
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

class BetaDeleteCourse(LoginRequiredMixin, DeleteView):
    model = CourseInfo
    template_name = 'trackerapp/betadelete_p.html'
    fields = "__all__"
    context_object_name = 'courseinfo'
    success_url = reverse_lazy('betamain')
    
class BetaUpdateCourse(LoginRequiredMixin, UpdateView):
    model = CourseInfo
    template_name = 'trackerapp/betaupdatecourse.html'
    fields = "__all__"
    context_object_name = 'courseinfo'
    fields = "__all__"

    def get_success_url(self):
        return reverse('betaviewcourse', kwargs={"pk": self.kwargs.get('pk')})
    
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
def htmx_delete_course(request, id):
    CourseInfo.objects.filter(id=id).delete()
    courseinfo = CourseInfo.objects.filter(user=request.user).prefetch_related()
    qs_id = CourseInfo.objects.filter(user=request.user).values('id')
    upcomingoneday = localtime() + timedelta(hours=8) 
    doseinfo = DoseInfo.objects.filter(courseinfo_id__in=qs_id).filter(dose_timing__gte=localtime()).filter(dose_timing__lte=upcomingoneday).select_related()                              
    context = {
        'courseinfo': courseinfo,
        'doseinfo': doseinfo,

    }
    return render(request, "trackerapp/partials/betamain_content.html", context)

@require_http_methods(['DELETE'])
def htmx_delete_dose(request, id, doseid):
    DoseInfo.objects.filter(id=doseid).delete()
    courseinfo = CourseInfo.objects.filter(pk=id)
    doseinfo = DoseInfo.objects.filter(courseinfo_id=id).order_by('dose_timing').values()
    
    qs_id = CourseInfo.objects.filter(user=request.user).values('id')

    upcomingoneday = localtime() + timedelta(hours=8)         
    
    context = {
        'courseinfo': courseinfo,
        'doseinfo': doseinfo,
    }
    return render(request, 'trackerapp/htmx_view_dose.html', context)            
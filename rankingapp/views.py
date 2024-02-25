from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Worker, Session
from django.views.decorators.http import require_http_methods
from .forms import HtmxAddWorker, GetSessionForm, NewSession, HtmxSaveSequence
from time import localtime
from django.urls import reverse
import math

# Create your views here.

def home(request):
    form = GetSessionForm()
    form_session = NewSession()
    return render(request, 'rankingapp/rankinghome.html', {'form':form, 'form_session': form_session})

def rankingredirect(request):
    sanitize = str(request.GET['user_defined'])
    return redirect('rankinglist', id=sanitize)

def htmx_validate_session(request):
    if Session.objects.filter(user_defined=request.GET['user_defined']).exists():
        return HttpResponse("<span class='text-dark ms-1'><i class='bi bi-x-circle-fill text-primary'></i>&nbsp;&nbsp;Choose something else, this is already taken.</span>")
    else:
        return HttpResponse("<span class='text-dark ms-1'><i class='bi bi-check-circle-fill' style='color:#64c10b'></i>&nbsp;&nbsp;This is ok, it's not taken.</span>")

def htmx_existing_session(request):
    if Session.objects.filter(user_defined=request.GET['user_defined']).exists():
        return HttpResponse("Use the ID you created previously.")
    else:
        return HttpResponse("<span class='text-dark ms-1' id='blocker2'><i class='bi bi-x-circle-fill text-primary'></i>&nbsp;&nbsp;There's no such session, are you sure this is correct?</span>")


@require_http_methods(['POST'])
def new_session(request):
    new_session = NewSession(request.POST or None)
    
    #if request.method == 'GET':    
    #    return render(request, 'trackerapp/htmx_create_dose.html', {'form': form})
    
    if request.method == 'POST':
        if new_session.is_valid():
            sanitized = new_session.cleaned_data['user_defined']
            new_session.save()
            return redirect('rankinglist', id=sanitized)    
        else:
            return redirect('rankinghome')       


class RankingList(ListView):
    model = Worker
    template_name = 'rankingapp/rankinglist.html'
    context_object_name = 'worker'
    '''
    def get_queryset(self):
        get_qs = Worker.objects.filter(pk=self.kwargs.get('session_id'))
        return get_qs
    '''
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        context['id'] = self.kwargs.get('id')
        worker_qs = Worker.objects.filter(session_id=self.kwargs.get('id'))
        worker_total = worker_qs.count()

        #grab the session quotas from db to populate noUIslider
        nouislider_quotas = Session.objects.filter(user_defined=self.kwargs.get('id')).values('user_quotaB','user_quotaC','user_quotaD').first()
        print(f"The DB user_quotas %% are {nouislider_quotas}")

        #calculate the quota percentages
        if Session.objects.filter(user_defined=self.kwargs.get('id')).exists():
            print("Are we using the DB values? Yes")
            user_quota = Session.objects.filter(user_defined=self.kwargs.get('id')).values()
            quotaB = math.ceil(user_quota[0]['user_quotaB']/100 * worker_total) #this is where quotaB starts
            quotaC = math.ceil(user_quota[0]['user_quotaC']/100 * worker_total) #this is where quotaC starts
            quotaD = math.ceil(user_quota[0]['user_quotaD']/100 * worker_total) #this is where quotaD starts
        else:
            print("Are we using the DB values? No, it's fallback.")
            quotaB = math.ceil(0.05 * worker_total)
            quotaC = math.floor(0.4 * worker_total) + quotaB
            quotaD = math.floor(0.5 * worker_total) + quotaC

        context['nouislider_quotas'] = nouislider_quotas
        context['worker_total'] = worker_total
        context['cumulative_quotas'] = {
            'quotaB': quotaB, 
            'quotaC': quotaC,
            'quotaD': quotaD,
        }
        print(f"The cumulative_quotas are: {context['cumulative_quotas']}")
        print(f"Total no. of entries: {context['worker_total']}")
        context['worker'] = worker_qs
        context['htmx_add_worker'] = HtmxAddWorker()
        return context


@require_http_methods(["POST"])
def htmx_add_worker(request, sessionid):

    form = HtmxAddWorker(request.POST or None)
    
    #if request.method == 'GET':    
    #    return render(request, 'trackerapp/htmx_create_dose.html', {'form': form})
    
    if request.method == 'POST':
        form.session_id = sessionid  
        if form.is_valid():
            filled = form.save(commit=False)
            filled.session_id = sessionid
            filled.save()
            worker = Worker.objects.filter(session=sessionid)
            form = HtmxAddWorker()
            
            worker_total = worker.count()
            
            user_quota = Session.objects.filter(user_defined=sessionid).values()
            quotaB = math.ceil(user_quota[0]['user_quotaB']/100 * worker_total)
            quotaC = math.ceil(user_quota[0]['user_quotaC']/100 * worker_total)
            quotaD = math.ceil(user_quota[0]['user_quotaD']/100 * worker_total)

            cumulative_quotas = {
                'quotaB': quotaB, 
                'quotaC': quotaC,
                'quotaD': quotaD,
            }
                
            context = {
                'worker': worker,
                'form': form,
                'worker_total': worker_total,
                'cumulative_quotas': cumulative_quotas,
            }
            
    return render(request, 'rankingapp/partials/htmx_view_worker.html', context)

@require_http_methods(["POST"])
def htmx_save_sequence (request, sessionid):

    rank_order = request.POST.getlist('sort_order')
    print(rank_order)
    for idx, form_rank_id in enumerate(rank_order, start=1):
        entry = Worker.objects.get(rank_id=form_rank_id)
        entry.order = idx
        entry.save()
        
    worker = Worker.objects.filter(session_id=sessionid)
    
    worker_total = worker.count()
    
    user_quota = Session.objects.filter(user_defined=sessionid).values('user_quotaB', 'user_quotaC', 'user_quotaD')
    quotaB = math.ceil(user_quota[0]['user_quotaB']/100 * worker_total)
    quotaC = math.ceil(user_quota[0]['user_quotaC']/100 * worker_total)
    quotaD = math.ceil(user_quota[0]['user_quotaD']/100 * worker_total)

    cumulative_quotas = {
        'quotaB': quotaB, 
        'quotaC': quotaC,
        'quotaD': quotaD,
    }

    context = {
        'worker': worker,
        'cumulative_quotas': cumulative_quotas,
    }

    return render(request, 'rankingapp/partials/htmx_view_worker.html', context)

@require_http_methods(["POST"])
def htmx_save_quota (request, sessionid):

    session = Session.objects.get(pk=sessionid)

    session.user_quotaB = request.POST['quotaB-input']
    session.user_quotaC = request.POST['quotaC-input']
    session.user_quotaD = request.POST['quotaD-input']
    print(f"The new % inserted into DB are: {session.user_quotaB}, {session.user_quotaC}, {session.user_quotaD}")
    session.save()
        
    worker = Worker.objects.filter(session_id=sessionid)
    
    worker_total = worker.count()
    new_session = Session.objects.filter(pk=sessionid).values()
    
    quotaB = math.ceil(new_session[0]['user_quotaB']/100 * worker_total)
    quotaC = math.ceil(new_session[0]['user_quotaC']/100 * worker_total)
    quotaD = math.ceil(new_session[0]['user_quotaD']/100 * worker_total)
    
    cumulative_quotas = {
        'quotaB': quotaB, 
        'quotaC': quotaC,
        'quotaD': quotaD,
    }
        
    context = {
        'worker': worker,
        'worker_total': worker_total,
        'cumulative_quotas': cumulative_quotas,
    }

    return render(request, 'rankingapp/partials/htmx_view_worker.html', context)

@require_http_methods(['DELETE'])
def htmx_delete_worker(request, sessionid, workerid):
    Worker.objects.filter(id=workerid).delete()
    worker = Worker.objects.filter(session_id=sessionid)
    worker_total = worker.count()
    
    user_quota = Session.objects.filter(user_defined=sessionid).values()
    quotaB = math.ceil(user_quota[0]['user_quotaB']/100 * worker_total)
    quotaC = math.ceil(user_quota[0]['user_quotaC']/100 * worker_total) + quotaB
    quotaD = math.ceil(user_quota[0]['user_quotaD']/100 * worker_total) + quotaC

    cumulative_quotas = {
        'quotaB': quotaB, 
        'quotaC': quotaC,
        'quotaD': quotaD,
    }
    
    context = {
        'worker': worker,
        'worker_total': worker_total,
        'cumulative_quotas': cumulative_quotas,
    }
    return render(request, 'rankingapp/partials/htmx_view_worker.html', context)
#    return HttpResponse('ok')

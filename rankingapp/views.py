from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Worker, Session
from django.views.decorators.http import require_http_methods
from .forms import HtmxAddWorker, GetSessionForm, NewSession
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

        quotaB = math.ceil(0.05 * worker_total)
        quotaC = math.floor(0.4 * worker_total) + quotaB
        quotaD = math.floor(0.5 * worker_total) + quotaC
        context['worker_total'] = worker_total
        context['cumulative_quotas'] = {
            'quotaB': quotaB, 
            'quotaC': quotaC,
            'quotaD': quotaD,
        }
        print(context['cumulative_quotas'])
        context['worker'] = worker_qs
        context['htmx_add_worker'] = HtmxAddWorker()
        return context


@require_http_methods(["POST"])
def htmx_add_worker(request, id):

    form = HtmxAddWorker(request.POST or None)
    
    #if request.method == 'GET':    
    #    return render(request, 'trackerapp/htmx_create_dose.html', {'form': form})
    
    if request.method == 'POST':
        form.session_id = id  
        if form.is_valid():
            filled = form.save(commit=False)
            filled.session_id = id
            filled.save()
            worker = Worker.objects.filter(session=id)
            form = HtmxAddWorker()
            
            worker_total = worker.count()
            quotaB = math.ceil(0.05 * worker_total)
            quotaC = math.floor(0.4 * worker_total) + quotaB
            quotaD = math.floor(0.5 * worker_total) + quotaC
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


@require_http_methods(['DELETE'])
def htmx_delete_worker(request, sessionid, workerid):
    Worker.objects.filter(id=workerid).delete()
    worker = Worker.objects.filter(session_id=sessionid)
    worker_total = worker.count()
    quotaB = math.ceil(0.05 * worker_total)
    quotaC = math.floor(0.4 * worker_total) + quotaB
    quotaD = math.floor(0.5 * worker_total) + quotaC
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

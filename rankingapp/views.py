from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Worker
from django.views.decorators.http import require_http_methods
from .forms import HtmxAddWorker, GetSessionForm, NewSession
from time import localtime

# Create your views here.

def home(request):
    form = GetSessionForm()
    form_session = NewSession()
    return render(request, 'rankingapp/rankinghome.html', {'form':form, 'form_session': form_session})

def rankingredirect(request):
    sanitize = str(request.GET['user_defined'])
    return redirect('rankinglist', id=sanitize)

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
        context['worker'] = Worker.objects.filter(session_id=self.kwargs.get('id'))
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
                
            context = {
                'worker': worker,
                'form': form,
            }
            
    return render(request, 'rankingapp/partials/htmx_view_worker.html', context)
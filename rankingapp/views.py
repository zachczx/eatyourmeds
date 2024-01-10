from django.shortcuts import render
from django.views.generic import ListView
from .models import Worker
from django.views.decorators.http import require_http_methods
from .forms import HtmxAddWorker

# Create your views here.

def home(request):
    return render(request, 'rankingapp/home.html')

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
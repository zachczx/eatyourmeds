from django.shortcuts import render
from django.views.generic import ListView
from .models import Worker

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
        
        return context

# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext

def index(request, template_name):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    else:
       form = UserCreationForm()
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

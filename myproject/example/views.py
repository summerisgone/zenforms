# Create your views here.
from django.forms.models import modelform_factory
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext
from django.contrib.auth.models import User
from .models import Profile, Card

def index(request, template_name):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    else:
       form = UserCreationForm()
    return render_to_response(template_name, {'form': form},
        context_instance=RequestContext(request))

def profile(request, template_name):
    CardFormset = inlineformset_factory(Profile, Card, extra=2, can_delete=False)
    ProfileForm = modelform_factory(Profile, exclude='user')

    if request.user.is_anonymous():
        current_profile = None
    else:
        current_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        formset = CardFormset(request.POST, instance=current_profile)
        form = ProfileForm(request.POST, instance=current_profile)
        if formset.is_valid():
            pass
    else:
        formset = CardFormset(instance=current_profile)
        form = ProfileForm(instance=current_profile)

    return render_to_response(template_name, {
        'formset': formset,
        'form': form,
    }, context_instance=RequestContext(request))

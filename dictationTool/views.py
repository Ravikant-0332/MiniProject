from django.shortcuts import render, redirect, HttpResponse
from .forms import FlatPageForm

# Create your views here.

def home(request):
    return render(request, 'dictationTool/index.html')

def dictationTool(request):
    form = FlatPageForm()
    context = {
        'form':form,
    }
    return render(request, 'dictationTool/dictationPad.html', context=context)
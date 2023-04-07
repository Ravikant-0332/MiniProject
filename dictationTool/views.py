from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

def home(request):
    return render(request, 'dictationTool/index.html')

def dictationTool(request):
    return HttpResponse("Welcome")
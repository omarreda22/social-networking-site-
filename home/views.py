from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    template_name = 'main/home.html'
    context = {

    }
    return render(request, template_name, context)

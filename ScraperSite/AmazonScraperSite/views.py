from django.shortcuts import render
from django.http import HttpResponse

def landing_page(request):
    #return HttpResponse('landing_page')
    return render(request, 'landing_page.html')

def help(request):
    #return HttpResponse('help')
    return render(request, 'help.html')

def download_page(request):
    #return HttpResponse('download_page')
    return render(request, 'download_page.html')

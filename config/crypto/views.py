from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse('Страница представления crypto')

def crypto(request):
    return HttpResponse('i m talk about crypto')

def snapshots(request, snap_id):
    return HttpResponse(f"<h1>Снимки</h1><p>id: {snap_id}</p>")
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from . import models
from django.db.models import Q


def greeting(request):
    return render(request, 'main_page/greeting.html')


def about(request):
    return render(request, 'main_page/about.html')


def tickets(request):
    return render(request, 'main_page/tickets.html')


def plan(request):
    return render(request, 'main_page/plan.html')


def search(request):
    searchquery = request.GET.get('q', '')

    if searchquery:
        all_info = models.Exhibit.objects.filter(
            Q(exhibit_name__icontains=searchquery) |
            Q(exhibit_desc__icontains=searchquery)
        )
        exposition_info = models.Exposition.objects.filter(
            Q(exposition_name__icontains=searchquery) |
            Q(exposition_desc__icontains=searchquery)
        )
    else:
        all_info = models.Exhibit.objects.all()
        exposition_info = models.Exposition.objects.all()

    context = {
        'all_info': all_info,
        'exposition_info': exposition_info,
    }
    return render(request, 'main_page/search.html', context)

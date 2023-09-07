from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from . import models
from django.db.models import Q
from django.views.generic import DetailView
from .models import Exhibit
from .models import Exposition
from .models import Hall
from .models import Tickets
from django.urls import resolve
import datetime
from datetime import timedelta
from django.contrib import messages


def greeting(request):
    return render(request, 'main_page/greeting.html')


def about(request):
    return render(request, 'main_page/about.html')


def tickets(request):
    data = request.GET.get('data', '')
    count = request.GET.get('count', '')
    time = request.GET.get('time', '')
    number = request.GET.get('number', '')

    datasucces = False
    countsucces = False
    numbersucces = number != '' and len(number) == 11 and str(number).isnumeric()
    if(data != ''):
        data = datetime.datetime.strptime(data, '%Y-%m-%d')
        if(data.weekday() != 0 and datetime.datetime.now() < data):
            if(time != ''):
                data = data + timedelta(hours=int(time))
                datasucces = True


    if(datasucces and count != '' and time != ''):
        infoondate = models.Tickets.objects.filter(Q(ticket_date=data))
        print(infoondate)
        if(len(infoondate) + int(count) < 15):
            countsucces = True
            print(data, count, time)

    message = ""
    if(not datasucces):
        message = "Дата или время не введены или введены неверно."
        messages.info(request, message)
    if(not countsucces):
        message = "Количество билетов не введено."
        messages.info(request, message)
    if(not numbersucces):
        message = "Номер не введён."
        messages.info(request, message)

    canbuy = datasucces and countsucces and numbersucces
    if(canbuy):
        for i in range(int(count)):
            Tickets.objects.create(ticket_date=data, phone_number=number)
    context = {
        'data_info': data,
        'count_info': count,
        'time_info': time,
        'number_info':number,
        'canbuy': canbuy,
    }
    if(canbuy):
        print("sadasd")
        return render(request, 'main_page/successfulbuy.html')
    else:
        return render(request, 'main_page/tickets.html', context)

def successfulbuy(request):
    return render(request, 'main_page/successfulbuy.html')


def plan(request):
    url_name = resolve(request.path).url_name
    if url_name == 'plan1':
        floor_info = models.Hall.objects.filter(floor_number=1)
        hall_floor = 1
    elif url_name == 'plan2':
        floor_info = models.Hall.objects.filter(floor_number=2)
        hall_floor = 2
    else:
        floor_info = models.Hall.objects.filter(floor_number=3)
        hall_floor = 3


    context = {
        'url_name': url_name,
        'halls': floor_info,
        'hall_floor': hall_floor,
    }
    return render(request, 'main_page/plan.html', context)


def search(request):
    if(request.method == 'POST'):
        tags = request.POST.getlist('tags[]')
        print(tags)
        print("12")
    
    tags = request.GET.getlist('tags[]')
    searchquery = request.GET.get('q', '')
    ExposChecked = False
    ExponChecked = True
    exp = request.GET.getlist('exp[]')
    print("exps: ",exp)
    ExposChecked = 'Expos' in exp
    ExponChecked = 'Expon' in exp
    if(not ExponChecked and not ExposChecked and tags == [] and len(searchquery) == 0):
        ExponChecked = True
        ExposChecked = False
    if(not (ExposChecked or ExponChecked)):
        ExponChecked = True
        ExposChecked = False

    models.Exhibit.objects.filter
    if searchquery:
        all_info = models.Exhibit.objects.filter(
            Q(exhibit_name__icontains=searchquery) |
            Q(exhibit_desc__icontains=searchquery)
        )
        exposition_info = models.Exposition.objects.filter(
            (Q(exposition_name__icontains=searchquery) |
            Q(exposition_desc__icontains=searchquery))
        )
    else:
        all_info = models.Exhibit.objects.all()
        exposition_info = models.Exposition.objects.all()

    if(tags != []):
        tags2 = models.ExhibitTags.objects.filter(
            Q(id_tag__in=tags)
        )
        all_info = all_info.filter(
            Q(exhibit_id__in=tags2.values("id_exhibit_tag"))
        )

        filtered = []
        for i in all_info:
            if(len(tags2.values("id_exhibit_tag").filter(id_exhibit_tag=i.exhibit_id)) >=
               len(tags)):
                filtered.append(i.exhibit_id)
                print("added", i)
        all_info = all_info.filter(Q(exhibit_id__in=filtered))

        tags3 = models.ExpositionExhibits.objects.filter(
            Q(id_exhibit_exposition__in=all_info.values("exhibit_id"))
        )
        exposition_info = exposition_info.filter(
            Q(exposition_id__in=tags3.values("id_exposition"))
        )
    
    print(tags)
    tags_info = models.Tags.objects.all()
    tags = tags_info.filter(Q(tag_id__in=tags))
    context = {
        'all_info': all_info,
        'exposition_info': exposition_info,
        'tags_info': tags_info,
        'search_quary': searchquery,
        'checked_tags': tags,
        'expos_checked': ExposChecked,
        'expon_checked': ExponChecked
    }
    return render(request, 'main_page/search.html', context)

class ExpDetailView(DetailView):
    model = Exhibit
    template_name = 'main_page\details_view.html'
    context_object_name = 'exhibit'

class ExponDetailView(DetailView):
    model = Exposition
    template_name = 'main_page\details_view_exposition.html'
    context_object_name = 'exposition'

class HallDetailView(DetailView):
     model = Hall
     template_name = 'main_page\details_view_hall.html'
     context_object_name = 'hall'


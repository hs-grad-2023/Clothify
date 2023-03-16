from django.shortcuts import redirect, render
from django.http import HttpResponse
from .api import get_loc_data, get_time, get_weather_data, get_icon
from .getDB import get_clothes_list
from .models import clothes
import sqlite3
import requests
import datetime
import math, json, sqlite3
from django.contrib import messages

# Create your views here.

# def 404(request):
#     return render(request,"404.html")

def index(request):
    location = get_loc_data()
    date = get_time()
    weather = get_weather_data()
    icon = get_icon()
    results= {
        'location' : location,
        'date' : date,
        'minTmp' : weather['minTmp'],
        'maxTmp' : weather['maxTmp'] ,
        'alertRain' : weather['alertRain'] ,
        'curTmp' : weather['curTmp'] ,
        'humidity' : weather['humidity'] ,
        'sky' : weather['sky'] ,
        'icon' : icon,
        }
    return render(request,"index.html",results)

def blog(request):
    return render(request,"blog.html")

def feature(request):
    return render(request,"feature.html")


def view_closet(request):
    # db = get_clothes_list()
    c = clothes.objects.all()   #clothes의 모든 객체를 c에 담기
    o = {
        'c' : c
    }
    
    return render(request,"view_closet.html", o)

def about(request):
    return render(request,"about.html")

def login(request):
    return render(request,"login.html")


def upload_closet(request):
    if request.method == 'POST':
        if request.FILES.get('imgfile'):
            new_clothes=clothes.objects.create(
                type1=request.POST.get('type1'),
                type2=request.POST.get('type2'),
                tag=request.POST.get('tags'),
                name=request.POST.get('name'),
                imgfile=request.FILES.get('imgfile'),
                details=request.POST.get('details'),
            )
        else:
            new_clothes=clothes.objects.create(
                type1=request.POST.get('type1'),
                type2=request.POST.get('type2'),
                tag=request.POST.get('tags'),
                name=request.POST.get('name'),
                imgfile=request.FILES.get('imgfile'),
                details=request.POST.get('details'),
            )
        return redirect('index') #상품목록으로 돌아가야함
    return render(request, 'upload_closet.html')


#게시글이 생성되면 index로 생성되지 않으면 글쓰기 게시판으로 돌아간다는데
# https://wikidocs.net/91438

# def remove_clothes(request, pk):
#     clothes = clothes.objects.get(pk=pk) #models.py 의 clothes
#     if request.method == 'POST':
#         post.delete()
#         return redirect('/index/') #상품목록으로 돌아가야함
#     return render(request, 'main/remove_post.html', {'clothes': clothes})

def detail_closet(request):
    return render(request,"detail_closet.html")
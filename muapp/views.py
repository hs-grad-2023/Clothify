from django.shortcuts import render
from django.http import HttpResponse
from .api import get_loc_data, get_time, get_weather_data, get_icon
import sqlite3
import requests
import datetime
import math, json, sqlite3

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

def product(request):
    return render(request,"product.html")

def about(request):
    return render(request,"about.html")

def login(request):
    return render(request,"login.html")


def login(request):
    return render(request,"login.html")



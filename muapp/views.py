from django.shortcuts import render
from django.http import HttpResponse
import sqlite3

# Create your views here.

def index(request):
    return render(request,"index.html")

# def 404(request):
#     return render(request,"404.html")

def blog(request):
    return render(request,"blog.html")

def feature(request):
    return render(request,"feature.html")

def product(request):
    return render(request,"product.html")

def about(request):
    return render(request,"about.html")

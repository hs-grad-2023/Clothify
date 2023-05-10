import shutil
from sqlite3 import IntegrityError
import sqlite3
import sys
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .api import get_loc_data, get_time, get_weather_data, get_icon
from .models import clothes, photos, Musinsa, Comment, viton_upload_cloth,viton_upload_model, viton_upload_result
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm, ModifyForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.db.models import Q
from functools import reduce
from operator import or_
from allauth.socialaccount.models import SocialAccount
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
import json
from ast import literal_eval
from django.core.paginator import Paginator
import io
import base64
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from itertools import chain
from django.views.decorators.http import require_POST
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector
import os
import numpy as np
import datetime, time, pygame
from muapp.viton import clothmask
import re, random
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

# def 404(request):
#     return render(request,"404.html")

typeCategory = {
        '상의':  ["== 상의 ==","니트/스웨터","셔츠/블라우스","후드 티셔츠", "피케/카라 티셔츠","맨투맨/스웨트셔츠", "반소매 티셔츠","긴소매 티셔츠","민소매 티셔츠","기타 상의"],
        '하의': ["== 하의 ==","데님 팬츠","숏 팬츠","코튼 팬츠", "레깅스","슈트 팬츠/슬랙스","점프 슈트/오버올","트레이닝/조거 팬츠","기타 바지"],
        '치마': ["== 치마 ==","미니 스커트", "미디 스커트","롱 스커트"],
        '원피스': ["== 원피스 ==","미니 원피스", "미디 원피스","맥시 원피스"],
        '아우터': ["== 아우터 ==","후드 집업","환절기 코트", "블루종/MA-1","겨울 코트", "레더/라이더스 재킷","무스탕/퍼","롱패딩/롱헤비 아우터","슈트/블레이저 재킷","숏패딩/숏헤비 아우터","카디건","아노락 재킷","패딩 베스트","플리스/뽀글이","트레이닝 재킷","기타 아우터"],
        '가방': ["== 가방 ==","백팩","메신저/크로스 백","파우치 백","숄더백","에코백","토트백","클로치 백","웨이스트백/힙색"],
        '악세서리': ["== 악세서리 ==","모자","레그웨어","머플러","장갑","시계","팔찌","귀걸이","반지","발찌","목걸이","헤어 액세서리"],
        '신발': ["== 신발 ==","구두","샌들","로퍼","힐/펌프스","플랫 슈즈","부츠","캔버스/단화","스포츠 스니커즈"],
}

allTypeCategory = [ "== 상의 ==", "== 하의 ==","== 치마 ==","== 원피스 ==","== 아우터 ==","== 가방 ==","== 악세서리 ==","== 신발 =="]

@receiver(user_signed_up)
def add_social_user_name(sender, request, user, **kwargs):
    social_accounts = SocialAccount.objects.get(user=user)
    user.first_name = get_random_string(length=16)
    if social_accounts.provider == 'kakao':
        user.name = social_accounts.extra_data['properties']['nickname']
    else:
        user.name = social_accounts.extra_data['name']
    user.save()
    messages.success(request, '축하합니다!!\nClothify의 회원가입이 완료되었습니다!')

def index(request):

    clothesobject = clothes.objects.all()   #clothes의 모든 객체를 c에 담기

    try:
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
            'clothesobject':clothesobject,
            }
        return render(request,"index.html",results)
    except:
        return render(request,"index.html",{ 'clothesobject':clothesobject, })

@login_required(login_url='login')
def view_closet(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    clothesobject = clothes.objects.all()   #clothes의 모든 객체를 c에 담기
    photoobject = photos.objects.all()

    
    if request.method == 'POST':
        del_clothes = request.POST.getlist('del_clothes')   #여러 개의 값 받아오기
        tmp = del_clothes[0].split(",")                     # 받아온 groupID 값 자르기

        if del_clothes:
            for group_id in tmp:
                remove = clothesobject.filter(groupID__exact=group_id)
                remove.delete()
        result = {
                    'clothesobject':clothesobject,
                    'user':user,
                    'photoobject':photoobject,
                }
        return render(request, "view_closet.html", result)
        
            
        #result = {
        #        'clothesobject' : clothesobject,
        #        'photoobject' : photoobject,
        #        'user':user,
        #}
        #return render(request, "view_closet.html", result)
    
    elif request.method == 'GET':
        # ===== filtering ======
        fl = request.GET.get('fl')  # 검색어
        if fl: #검색어가 있고
            filterList = fl.split(',')
            q_list=[]                   # 필터링 하기 위한 배열
            for item in filterList:
                if "==" in item:
                    type1Item = item.replace("==","").strip()       # '=='가 포함된 문자열을 ""으로 치환
                    type1_filter = clothesobject.filter(type1__icontains=type1Item)&clothesobject.filter(uploadUser__exact=user.id)    # type1 에서 type1Item 과 대소문자를 가리지 않고 부분 일치하는 조건
                    q_list.append(type1_filter)                     # 조건에 맞은 type1_filter를 q_list에 넣기
                else:
                    type2_filter = clothesobject.filter(type2__icontains=item)&clothesobject.filter(uploadUser__exact=user.id)
                    q_list.append(type2_filter)
                
                
            #clothesobject = clothesobject.filter(reduce(or_, q_list)).distinct()   # 타입 검색 -> queryset끼리 중복 제외하고 합병( 조건부 표현식에 대해 필터링 할 수 없다고 뜸)
                
            clothesobject = reduce(or_, q_list).distinct()                          # 타입 검색 -> queryset끼리 중복 제외하고 합쳐짐
            
            result = {
                    'clothesobject':clothesobject,
                    'user':user,
                    'filterList':filterList,
                    'photoobject':photoobject,
                }
            return render(request, 'view_closet.html', result)
        elif not fl: #검색어가 없으면
            groupIdList = clothesobject.filter(uploadUser__exact=user.id).values_list("groupID") #<QuerySet [('vi3qalsycy',)]>
            photoobject = photoobject.filter(groupID__in = groupIdList).values()
            result = {
                    'clothesobject' : clothesobject,
                    'photoobject' : photoobject,
                    'groupIdList' : groupIdList,
                    'user':user,
                }
            return render(request, 'view_closet.html', result)


    
@login_required(login_url='login')
def uploadCloset(request, username):
    user = get_object_or_404(User, first_name=username) #user = User.objects.get(first_name=username) 예외 처리를 따로 하고 싶을 때 사용
    if user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        getGroupID = request.POST.get('groupID')
        if request.FILES.getlist('imgfile'):
            for imgfile in request.FILES.getlist('imgfile'):
                try:
                    new_clothes =  clothes.objects.filter(Q(groupID__exact = str(getGroupID))).get() # first는 None을 리턴
                # except None:
                except clothes.DoesNotExist or None:
                    try:
                        new_clothes = clothes.objects.create(
                            uploadUser_id=request.user.id,
                            uploadUserName=request.user.username,
                            type1=request.POST.get('type1'),
                            type2=request.POST.get('type2'),
                            tag=request.POST.get('tags'),
                            name=request.POST.get('clothesName'),
                            details=request.POST.get('details'),
                            ucodi=request.POST.get('ucodi'),
                            groupID=getGroupID,
                        )
                        if new_clothes.ucodi == None:
                            new_clothes.ucodi = False
                    except:
                        new_clothes =  clothes.objects.filter(Q(groupID__exact = str(getGroupID))).get() # first는 None을 리턴
                new_clothes.save()
                    
                new_photo = photos.objects.create(
                                groupID_id=new_clothes.groupID,
                                imgfile = imgfile,
                )
                new_photo.save()
        return redirect('view_closet', username=user.first_name)
    else: 
        return render(request, 'upload_closet.html', {"user":user})

@login_required(login_url='login')
def detail_closet(request, username, groupID):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    clothesobject = clothes.objects.filter(Q(groupID__exact=groupID) & Q(uploadUser__exact=user.id)).get()  

    photosobject = photos.objects.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('groupID')],
                    order_by=[F('groupID_id')])).order_by('groupID_id')         #order_by 수정

    photosobject = photosobject.filter(groupID__exact=groupID)

    result = {
        'clothesobject' : clothesobject,
        "user" : user,
        "groupID" : groupID,
        'photosobject':photosobject,
    }
    return render(request,"detail_closet.html",result)

@login_required(login_url='login')
def updateCloset(request, username, groupID):
    user = get_object_or_404(User, first_name=username) #user = User.objects.get(first_name=username) 예외 처리를 따로 하고 싶을 때 사용
    if user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        getgroupID = request.POST.get('groupID')
        try:
            new_clothes = clothes.objects.get(groupID__exact = groupID)
            new_clothes.type1 = request.POST.get('type1')
            new_clothes.type2 = request.POST.get('type2')
            new_clothes.tag = request.POST.get('tags')
            new_clothes.name = request.POST.get('clothesName')
            new_clothes.details = request.POST.get('details')
            if request.POST.get('ucodi') == 'True':
                new_clothes.ucodi = True
            else:
                new_clothes.ucodi = False
            new_clothes.save()
        except clothes.DoesNotExist:
            print('객체 오류')
            
        

        if request.FILES.getlist('imgfile'):
            for imgfile in request.FILES.getlist('imgfile'):
                new_photo = photos.objects.create(
                                groupID_id=new_clothes.groupID,
                                imgfile = imgfile,
                )
                new_photo.save()

        return redirect('view_closet', username=user.first_name)
    else:
        clothesobject = clothes.objects.filter(Q(groupID__exact=groupID) & Q(uploadUser__exact=user.id)).get()   
        photosobject = photos.objects.annotate(
                    row_number=Window(
                        expression=RowNumber(),
                        partition_by=[F('groupID')],
                        order_by='groupID_id'
                    )
        )
        photosobject = photosobject.filter(groupID__exact=groupID)
        
        result = {
            "user":user,
            "clothesobject" : clothesobject,
            "groupID" : groupID,
            "photosobject" : photosobject,
        }
        return render(request, 'update_closet.html',result)


@login_required(login_url='login')
def remove_closet(request, username, groupID):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    
    try:
        remove_clothes= clothes.objects.get(groupID=groupID)      # clothes에서 pk와 같은 primary_key 값을 remove_clothes에 담기
        remove_clothes.delete()     # 삭제 후 메시지를 보여줍니다.
        # messages.success(request, '데이터를 삭제했습니다.')
    except clothes.DoesNotExist:
        messages.error(request, '삭제할 데이터가 없습니다.')
    
    return redirect('view_closet', username=user.first_name)

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = get_random_string(length=16)
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            messages.success(request, '축하합니다!!\nClothify의 회원가입이 완료되었습니다!')
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def logins(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method =='POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            #검증 완료시 로그인
            login(request, form.get_user())
            user = form.get_user().first_name
            if 'next' in request.POST:
                next_string = request.POST.get('next')
                result = next_string.split('/')[1]
                if result == 'modify' or result == 'userlike':
                    return redirect(f'/{result}/')
                elif result == 'usercodi':
                    return redirect(request.POST.get('next'))
                else:
                    print(f'/{result}/{user}')
                    return redirect(f'/{result}/{user}')
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login2.html', {'form': form}) 

@login_required(login_url='login')
def user_modify(request):
    if request.method == 'POST':
        form = ModifyForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ModifyForm(instance=request.user)
    return render(request,"user_modify.html", {'form': form,})

@login_required(login_url='login')
def mypage(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    return render(request,"mypage.html",{"user":user})


@login_required(login_url='login')
def codibook(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    if user.style is None:
        return redirect(f'/mypage/userstyle/{user.first_name}')
    userstyle = literal_eval(user.style) # json으로 사용해도됨. 방법:리스트를 JSON 형식으로 직렬화하여 문자열로 저장 userstyle = json.loads(selected_styles)
    musinsa = Musinsa.objects.filter(item_text__in=userstyle)
    paginator = Paginator(musinsa, 9)
    page = request.GET.get('page')
    musinsa = paginator.get_page(page)
    return render(request,"codibook.html",{"user":user, "musinsa":musinsa})

def blog(request):
    return render(request,"blog.html")

def feature(request):
    return render(request,"feature.html")

@login_required(login_url='login')
def user_style(request, username):
    style = ['아메리칸 캐주얼', '캐주얼', '시크', '댄디', '포멀', '걸리시', '골프', '레트로', '로맨틱', '스포츠', '스트릿', '고프코어']
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return redirect('/')
    if request.method == 'POST':
        selected_styles = request.POST.getlist("style")
        if not selected_styles:
            messages.error(request, '적어도 하나 이상의 스타일을 선택해주세요')
            return redirect('user_style', username=username)
        user.style = str(selected_styles) # json으로 사용해도됨. 방법:리스트를 JSON 형식으로 직렬화하여 문자열로 저장 user.style = json.dumps(selected_styles)
        user.save()
        return redirect('/')
    return render(request, "user_style.html", {"user": user, "style": style})

# @login_required(login_url='login')
# def product(request, username):
#     user = User.objects.get(username=username)
#     return render(request,"product.html",{"user":user})


def about(request):
    return render(request, "about.html")


def usercodi(request):
    clothesobject = clothes.objects.filter(ucodi=True)
    paginator = Paginator(clothesobject, 9)
    page = request.GET.get('page')
    clothesobject = paginator.get_page(page)
    comments = Comment.objects.all()
    return render(request,"usercodi.html",{'cloth':clothesobject, 'comments': comments})

def detail_usercodi(request, id):
    clothesobject = clothes.objects.filter(groupID__exact=id).get()  

    comments = Comment.objects.filter(post=clothesobject).order_by('-created_date')

    photosobject = photos.objects.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('groupID')],
                    order_by='groupID_id'
                )
    )

    photosobject = photosobject.filter(groupID__exact=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = clothesobject
            comment.save()
            return redirect('detail_usercodi', id=id)
    else:
        form = CommentForm()

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    result = {
        'clothesobject' : clothesobject,
        'photosobject' : photosobject,
        'comments' : comments,
        'form' : form,
    }
    
    return render(request,"detail_usercodi.html", result)

@login_required(login_url='login')
def like(request):
    # 어떤 게시물에, 어떤 사람이 like를 했는 지
   if request.headers.get('X-Requested-With'): #ajax 방식일 때 아래 코드 실행
        groupid = request.GET.get('groupID') #좋아요를 누른 게시물id 가지고 오기
        post = clothes.objects.get(groupID=groupid) 
        user = request.user #request.user : 현재 로그인한 유저
        if post.like.filter(id=user.id).exists(): #이미 좋아요를 누른 유저일 때
            post.like.remove(user) #like field에 현재 유저 추가
        else: #좋아요를 누르지 않은 유저일 때
            post.like.add(user) #like field에 현재 유저 삭제
        # post.like.count() : 게시물이 받은 좋아요 수  
        context = {'like_count' : post.like.count(),}
        return HttpResponse(json.dumps(context), content_type='application/json')
       
@login_required(login_url='login')
def like2(request):
    # 어떤 게시물에, 어떤 사람이 like를 했는 지
   if request.headers.get('X-Requested-With'): #ajax 방식일 때 아래 코드 실행
        cid = request.GET.get('id') #좋아요를 누른 게시물id 가지고 오기
        post = Musinsa.objects.get(id=cid) 
        user = request.user #request.user : 현재 로그인한 유저
        if post.like.filter(id=user.id).exists(): #이미 좋아요를 누른 유저일 때
            post.like.remove(user) #like field에 현재 유저 삭제
        else: #좋아요를 누르지 않은 유저일 때
            post.like.add(user) #like field에 현재 유저 추가
        # post.like.count() : 게시물이 받은 좋아요 수  
        context = {'like_count' : post.like.count(),}
        return HttpResponse(json.dumps(context), content_type='application/json')
   
@login_required(login_url='login')
def virfit(request):
    
    user = request.user
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    cpath = os.path.join(base_dir, "muapp", "VirtualFitting", "Resources")
    dpath = os.path.join(base_dir, "_media", "imgfiles")

    pygame.mixer.init()
    shutter_sound = pygame.mixer.Sound(os.path.join(cpath, "shutter.mp3"))
    shutter_sound.set_volume(0.5)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
    detector = PoseDetector()

    shirtsFolderPath = os.path.join(cpath, "Shirts")
    pantsFolderPath = os.path.join(cpath, "Pants")


    listShirts = os.listdir(shirtsFolderPath)
    listPants = os.listdir(pantsFolderPath)

    fixedRatio = 320 / 190 #셔츠의 넓이 262 / lm11에서 12의 사이 넓이
    shirtsRatioHeight = 500 / 440 #이미지 사이즈 비율 581/440 높이면 작아짐

    fixedRatio2 = 270 / 140 #셔츠의 넓이 262 / lm11에서 12의 사이 넓이
    pantsRatioHeight = 1000 / 440 #이미지 사이즈 비율 581/440

    imageNumber = 0
    imageNumber2 = 0

    cameraButton = cv2.imdecode(np.fromfile(os.path.join(cpath, "camera.png"), np.uint8), cv2.IMREAD_UNCHANGED)
    shirtsButton = cv2.imdecode(np.fromfile(os.path.join(cpath, "shirts.png"), np.uint8), cv2.IMREAD_UNCHANGED)
    pantsButton = cv2.imdecode(np.fromfile(os.path.join(cpath, "pants.png"), np.uint8), cv2.IMREAD_UNCHANGED)
    
    imgButtonRight = cv2.imdecode(np.fromfile(os.path.join(cpath, "button.png"), np.uint8), cv2.IMREAD_UNCHANGED)
    imgButtonLeft = cv2.flip(imgButtonRight, 1)
    counterButton = 0
    counterRight = 0
    counterLeft = 0
    counterRight2 = 0
    counterLeft2 = 0
    counterLeft3 = 0
    counterRight3 = 0
    selectionSpeed = 20
    distance_threshold = 673
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findPose(img, draw=False)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
        if bboxInfo:
            # center = bboxInfo["center"]
            # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

            lm11 = lmList[11][1:3]
            lm12 = lmList[12][1:3]

            lm23 = lmList[23][1:3]
            lm24 = lmList[24][1:3]

            distance = lmList[24][2]
            
            # else:
            #     cv2.putText(img, f"Distance: {distance}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            imgShirt = cv2.imdecode(np.fromfile(os.path.join(cpath, os.path.join(shirtsFolderPath, listShirts[imageNumber])), np.uint8), cv2.IMREAD_UNCHANGED)

            imgPant = cv2.imdecode(np.fromfile(os.path.join(cpath, os.path.join(pantsFolderPath, listPants[imageNumber2])), np.uint8), cv2.IMREAD_UNCHANGED)



            widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
            widthOfShirt = max(widthOfShirt, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtsRatioHeight)))

            widthOfPant = int((lm23[0] - lm24[0]) * fixedRatio2)
            widthOfPant = max(widthOfPant, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
            imgPant = cv2.resize(imgPant, (widthOfPant, int(widthOfPant * pantsRatioHeight)))

            currentScale = (lm11[0] - lm12[0]) / 145 #옷 위치 190
            offset = int(50 * currentScale), int(48 * currentScale) #좌우 44, 48 *30/48

            currentScale2 = (lm23[0] - lm24[0]) / 150 #옷 위치 190
            offset2 = int(75 * currentScale2), int(80 * currentScale2) #좌우 44, 48 *30/48 x, y



            try:
                #  img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
                img_height, img_width, _ = img.shape#웹캠 영상의 높이와 너비를 가져옵니다.
                sh_height, sh_width, _ = imgShirt.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

                x_position = max(0, lm12[0] - offset[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
                y_position = max(0, lm12[1] - offset[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

                pa_height, pa_width, _ = imgPant.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

                x_position2 = max(0, lm24[0] - offset2[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
                y_position2 = max(0, lm24[1] - offset2[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

                # 셔츠 이미지가 웹캠 영역을 벗어난 경우, 잘라내기
                if x_position2 + pa_width <= img_width and y_position2 + pa_height <= img_height:
                    img = cvzone.overlayPNG(img, imgPant, (x_position2, y_position2))

                if x_position2 + pa_width > img_width or y_position2 + pa_height > img_height:
                    cropped_width2 = min(pa_width, img_width - x_position2)#잘라낼 셔츠 이미지의 너비를 계산합니다. 웹캠 영상의 너비에서 이미지의 x 위치를 뺀 값과 셔츠 이미지의 원래 너비 중 작은 값을 사용합니다.
                    cropped_height2 = min(pa_height, img_height - y_position2)#잘라낼 셔츠 이미지의 높이를 계산합니다. 웹캠 영상의 높이에서 이미지의 y 위치를 뺀 값과 셔츠 이미지의 원래 높이 중 작은 값을 사용합니다.
                    imgPant_cropped = imgPant[:cropped_height2, :cropped_width2]#셔츠 이미지에서 웹캠 영역 안에 있는 부분만 잘라냅니다.
                    img = cvzone.overlayPNG(img, imgPant_cropped, (x_position2, y_position2))#잘라낸 셔츠 이미지를 웹캠 영상에 붙입니다.
                
                if x_position + sh_width <= img_width and y_position + sh_height <= img_height:
                    img = cvzone.overlayPNG(img, imgShirt, (x_position, y_position))

                if x_position + sh_width > img_width or y_position + sh_height > img_height:
                    cropped_width = min(sh_width, img_width - x_position)
                    cropped_height = min(sh_height, img_height - y_position)#
                    imgShirt_cropped = imgShirt[:cropped_height, :cropped_width]
                    img = cvzone.overlayPNG(img, imgShirt_cropped, (x_position, y_position))
                        
                
            except:
                pass
            
            if lmList[15][1] > 1050 and lmList[15][1] < 1200 and lmList[15][2] < 200 and lmList[15][2] > 100:
                counterLeft3 += 1
                cv2.ellipse(img, (1138, 160), (66, 66), 0, 0, 
                            counterLeft3 * selectionSpeed, (0, 255, 0), 20)
                if counterLeft3 * selectionSpeed > 360:
                    counterLeft3 = 0
                    start_time = time.time()
                    countdown = 3

                    while countdown >= 0:
                        _, img = cap.read()
                        img = cv2.flip(img, 1)
                        img = cv2.resize(img, (1280, 720))
                        img = detector.findPose(img, draw=False)
                        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
                        if bboxInfo:
                            # center = bboxInfo["center"]
                            # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

                            lm11 = lmList[11][1:3]
                            lm12 = lmList[12][1:3]

                            lm23 = lmList[23][1:3]
                            lm24 = lmList[24][1:3]

                            distance = lmList[24][2]          
        
                            # else:
                            #     cv2.putText(img, f"Distance: {distance}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            imgShirt = cv2.imdecode(np.fromfile(os.path.join(cpath, os.path.join(shirtsFolderPath, listShirts[imageNumber])), np.uint8), cv2.IMREAD_UNCHANGED)

                            imgPant = cv2.imdecode(np.fromfile(os.path.join(cpath, os.path.join(pantsFolderPath, listPants[imageNumber2])), np.uint8), cv2.IMREAD_UNCHANGED)

                            widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
                            widthOfShirt = max(widthOfShirt, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
                            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtsRatioHeight)))

                            widthOfPant = int((lm23[0] - lm24[0]) * fixedRatio2)
                            widthOfPant = max(widthOfPant, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
                            imgPant = cv2.resize(imgPant, (widthOfPant, int(widthOfPant * pantsRatioHeight)))

                            currentScale = (lm11[0] - lm12[0]) / 145 #옷 위치 190 내리면 올라감
                            offset = int(50 * currentScale), int(48 * currentScale) #좌우 44, 48 *30/48 왼쪽꺼 내리면 오른쪽으로

                            currentScale2 = (lm23[0] - lm24[0]) / 150 #옷 위치 190
                            offset2 = int(75 * currentScale2), int(80 * currentScale2) #좌우 44, 48 *30/48 x, y



                        # 이 부분에 이미지 처리 코드를 삽입하세요.
                        try:
                            #  img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
                            img_height, img_width, _ = img.shape#웹캠 영상의 높이와 너비를 가져옵니다.
                            sh_height, sh_width, _ = imgShirt.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

                            x_position = max(0, lm12[0] - offset[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
                            y_position = max(0, lm12[1] - offset[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

                            pa_height, pa_width, _ = imgPant.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

                            x_position2 = max(0, lm24[0] - offset2[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
                            y_position2 = max(0, lm24[1] - offset2[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

                            # 셔츠 이미지가 웹캠 영역을 벗어난 경우, 잘라내기
                            if x_position2 + pa_width <= img_width and y_position2 + pa_height <= img_height:
                                img = cvzone.overlayPNG(img, imgPant, (x_position2, y_position2))

                            if x_position2 + pa_width > img_width or y_position2 + pa_height > img_height:
                                cropped_width2 = min(pa_width, img_width - x_position2)#잘라낼 셔츠 이미지의 너비를 계산합니다. 웹캠 영상의 너비에서 이미지의 x 위치를 뺀 값과 셔츠 이미지의 원래 너비 중 작은 값을 사용합니다.
                                cropped_height2 = min(pa_height, img_height - y_position2)#잘라낼 셔츠 이미지의 높이를 계산합니다. 웹캠 영상의 높이에서 이미지의 y 위치를 뺀 값과 셔츠 이미지의 원래 높이 중 작은 값을 사용합니다.
                                imgPant_cropped = imgPant[:cropped_height2, :cropped_width2]#셔츠 이미지에서 웹캠 영역 안에 있는 부분만 잘라냅니다.
                                img = cvzone.overlayPNG(img, imgPant_cropped, (x_position2, y_position2))#잘라낸 셔츠 이미지를 웹캠 영상에 붙입니다.
                            
                            if x_position + sh_width <= img_width and y_position + sh_height <= img_height:
                                img = cvzone.overlayPNG(img, imgShirt, (x_position, y_position))

                            if x_position + sh_width > img_width or y_position + sh_height > img_height:
                                cropped_width = min(sh_width, img_width - x_position)
                                cropped_height = min(sh_height, img_height - y_position)#
                                imgShirt_cropped = imgShirt[:cropped_height, :cropped_width]
                                img = cvzone.overlayPNG(img, imgShirt_cropped, (x_position, y_position))      
                            
                        except:
                            pass

                        elapsed_time = time.time() - start_time
                        if elapsed_time >= 1:
                            countdown -= 1
                            start_time = time.time()

                        if countdown != -1:
                            img_pil = Image.fromarray(img)
                            draw = ImageDraw.Draw(img_pil)
                            font = ImageFont.truetype(os.path.join(cpath, "GmarketSansTTF\GmarketSansTTFBold.ttf"), 80)
                            text = f"{countdown}"
                            position = (580, 10)
                            border_color = (0, 0, 0)  # 검은색 테두리
                            fill_color = (0, 255, 0, 0)  # 초록색 내부 색상
                            border_width = 1  # 테두리 두께

                            # 텍스트 주위에 테두리를 그립니다.
                            for x_offset in range(-border_width, border_width + 1):
                                for y_offset in range(-border_width, border_width + 1):
                                    draw.text((position[0] + x_offset, position[1] + y_offset), text, font=font, fill=border_color)

                            # 텍스트를 그립니다.
                            draw.text(position, text, font=font, fill=fill_color)
                            img = np.array(img_pil)

                        cv2.imshow("Virtual Fitting", img)
                        cv2.waitKey(1)

                    shutter_sound.play()
                    white_img = np.full(img.shape, 255, dtype=np.uint8)
                    cv2.imshow("Virtual Fitting", white_img)
                    cv2.waitKey(200)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

                    new_img_name = os.path.join(dpath, f"VirtualFitting\capture_{timestamp}.png")
                    extension = os.path.splitext(new_img_name)[1]
                    result, encoded_img = cv2.imencode(extension, img)

                    if result:
                        with open(new_img_name, mode='w+b') as f:
                            encoded_img.tofile(f)
                            new_clothes = clothes.objects.create(
                            uploadUser_id=user.id,
                            uploadUserName=user.username,
                            type1='코디',
                            type2='가상피팅',
                            name=f'{user.username}-{timestamp}',
                            ucodi=False,
                            tag='#가상피팅',
                            groupID=get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789'),
                        )
                            new_clothes.save()
                            
                            new_photo = photos.objects.create(
                                    groupID_id=new_clothes.groupID,
                                    imgfile = f'imgfiles\VirtualFitting\capture_{timestamp}.png',
                            )
                            new_photo.save()


                    print("Capture saved")

            else:
                counterLeft3 = 0


            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype(os.path.join(cpath, "GmarketSansTTF\GmarketSansTTFBold.ttf"), 30)  # 한글 폰트 파일을 사용합니다. 시스템에 따라 경로를 변경해야 할 수도 있습니다.
            text = "좌우 버튼을 눌러서 가상피팅을 해보세요!(나가기-Q)"
            position = (580, 10)
            border_color = (0, 0, 0)  # 검은색 테두리
            fill_color = (0, 255, 0, 0)  # 초록색 내부 색상
            border_width = 1  # 테두리 두께

            # 텍스트 주위에 테두리를 그립니다.
            for x_offset in range(-border_width, border_width + 1):
                for y_offset in range(-border_width, border_width + 1):
                    draw.text((position[0] + x_offset, position[1] + y_offset), text, font=font, fill=border_color)

            # 텍스트를 그립니다.
            draw.text(position, text, font=font, fill=fill_color)
            img = np.array(img_pil)

            # if distance > distance_threshold:
            #     img_pil = Image.fromarray(img)
            #     draw = ImageDraw.Draw(img_pil)
            #     font = ImageFont.truetype(f"{cpath}GmarketSansTTF\GmarketSansTTFBold.ttf", 30)  # 한글 폰트 파일을 사용합니다. 시스템에 따라 경로를 변경해야 할 수도 있습니다.
            #     draw.text((10, 10), "너무 가깝습니다.", font=font, fill=(0, 0, 255, 0))
            #     img = np.array(img_pil)

            img = cvzone.overlayPNG(img, cameraButton, (1074, 93))

            if counterButton == 0:
                img = cvzone.overlayPNG(img, shirtsButton, (72, 93))
            elif counterButton == 1:
                img = cvzone.overlayPNG(img, pantsButton, (72, 93))

            img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
            img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

            # img = cvzone.overlayPNG(img, imgButtonRight, (1074, 493))
            # img = cvzone.overlayPNG(img, imgButtonLeft, (72, 493))

            
            if lmList[16][1] < 200 and lmList[16][1] > 100 and lmList[16][2] < 200 and lmList[16][2] > 100:
                counterRight3 += 1
                cv2.ellipse(img, (134, 160), (76, 76), 0, 0, 
                            counterRight3 * selectionSpeed, (0, 255, 0), 20)
                if counterRight3 * selectionSpeed > 360:
                    counterRight3 = 0
                    if counterButton == 0:
                        counterButton = 1
                    else:
                        counterButton = 0

            if counterButton == 0:
                if lmList[16][1] < 200 and lmList[16][1] > 100 and lmList[16][2] < 400 and lmList[16][2] > 300:
                    counterRight += 1
                    cv2.ellipse(img, (139, 360), (66, 66), 0, 0, 
                                counterRight * selectionSpeed, (0, 255, 0), 20)
                    if counterRight * selectionSpeed > 360:
                        counterRight = 0
                        if imageNumber < len(listShirts)-1:
                            imageNumber += 1
                        else:
                            imageNumber = 0

                elif lmList[15][1] > 1050 and lmList[15][1] < 1200 and lmList[15][2] < 400 and lmList[15][2] > 300:
                    counterLeft += 1
                    cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, 
                                counterLeft * selectionSpeed, (0, 255, 0), 20)
                    if counterLeft * selectionSpeed > 360:
                        counterLeft = 0
                        if imageNumber > 0:
                            imageNumber -= 1
                        else:
                            imageNumber = len(listShirts)-1
                else:
                    counterRight = 0
                    counterLeft = 0
            
            elif counterButton == 1:
                if lmList[16][1] < 200 and lmList[16][1] > 100 and lmList[16][2] < 400 and lmList[16][2] > 300:
                    counterRight2 += 1
                    cv2.ellipse(img, (139, 360), (66, 66), 0, 0, 
                                counterRight2 * selectionSpeed, (0, 255, 0), 20)
                    if counterRight2 * selectionSpeed > 360:
                        counterRight2 = 0
                        if imageNumber2 < len(listPants)-1:
                            imageNumber2 += 1
                        else:
                            imageNumber2 = 0

                elif lmList[15][1] > 1050 and lmList[15][1] < 1200 and lmList[15][2] < 400 and lmList[15][2] > 300:
                    counterLeft2 += 1
                    cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, 
                                counterLeft2 * selectionSpeed, (0, 255, 0), 20)
                    if counterLeft2 * selectionSpeed > 360:
                        counterLeft2 = 0
                        if imageNumber2 > 0:
                            imageNumber2 -= 1
                        else:
                            imageNumber2 = len(listPants)-1
                else:
                    counterRight2 = 0
                    counterLeft2 = 0

            

        cv2.imshow("Virtual Fitting", img)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return redirect('virtual_fit_video', user.first_name)

@login_required(login_url='login')
def virtual_fit_photo(request,username):
    user = request.user
    model_dataset = viton_upload_model.objects.all()
    model_paginator = Paginator(model_dataset, 20)
    model_page = request.GET.get('mpage')
    model_paging = model_paginator.get_page(model_page)
    
    cloth_dataset = viton_upload_cloth.objects.all()
    cloth_paginator = Paginator(cloth_dataset, 20)
    cloth_page = request.GET.get('cpage')
    cloth_paging = cloth_paginator.get_page(cloth_page)

    del_model = request.POST.getlist('del_model')     # 여러 개의 값 받아오기
    del_cloth = request.POST.getlist('del_cloth')     
    
    
    if del_model:
        tmp = del_model[0].split(",")                     # 받아온 name 값 자르기
        for model_name in tmp:
            remove_model = model_dataset.filter(name__exact=model_name)
            remove_model.delete()
        
    if del_cloth:
        tmp2 = del_cloth[0].split(",")
        for cloth_name in tmp2:
            remove_cloth = cloth_dataset.filter(name__exact=cloth_name)
            remove_cloth.delete()    

    result = {    
                'model_paging' : model_paging,
                'cloth_paging' : cloth_paging,
            }
    return render(request, "virtual_fit_photo.html", result)
    
    

@login_required(login_url='login')
def virtual_fit_photo_result(request,username):
    user = request.user
    if request.method == 'POST':
        model_result = request.POST.getlist('model_result')
        cloth_result = request.POST.getlist('cloth_result')


        selected_model = model_result[0].split(",")
        selected_cloth = cloth_result[0].split(",")
        
        
        
        print(selected_model)
        
        result_vition = viton_upload_result.objects.all().annotate(
                row_number=Window(
                    expression=RowNumber(),
                    order_by=[F('name')])).order_by('name')         #order_by 수정
                    
  
        q_list=[]
        testWrite = ''

        for model in selected_model:
            for cloth in selected_cloth:
                result_name = model[:5] + '_' + cloth[:5] + '_00.jpg'
                filter = result_vition.filter(name__exact=result_name)
                q_list.append(filter)

        result_vition = reduce(or_, q_list).distinct()       # 타입 검색 -> queryset끼리 중복 제외하고 합쳐짐
        
        result = {'result_vition':result_vition,
                  "user":user,
                  }

        return render(request, "virtual_fit_photo_result.html",result)
    else:
        return redirect('virtual_fit_photo', username=user.first_name)


@login_required(login_url='login')
def virtual_fit_video(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return redirect(f'/virtual_fit_video/{request.user.first_name}')
    return render(request,"virtual_fit_video.html",{"user":user})

@login_required(login_url='login')
def virtual_fit_upload(request,username):
    user = request.user
    if user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        if request.FILES.getlist('imgfile'):
            getType = request.POST.get('itemtype')
            if getType == '옷':
                for imgfile in request.FILES.getlist('imgfile'):
                    # 조정된 이미지 저장
                    item = viton_upload_cloth.objects.create(
                        clothesname = request.POST.get('itemName'),
                        image=imgfile,
                        uploadUser=request.user.username,
                    )
                    item.save()
                    
                    name_val = viton_upload_cloth.objects.values('name').first()
                    item_name = name_val['name']
                    print("item : ",item_name)
                    
                    wcpath = 'C:/hs-grad-2023/django/muapp/viton/data/custom/cloth/{}'.format(item_name)
                    rcpath = 'C:/hs-grad-2023/django/_media/datasets/cloth/{}'.format(item_name)
                    shutil.copyfile(rcpath, wcpath) #rc -> wc로 복사

                    clothmask.cloth_mask(wcpath)
                    
                    # 파일 이름 리스트를 저장할 txt 파일 경로 및 이름 지정
                    file_list_file = 'C:/hs-grad-2023/django/muapp/viton/data/custom/custom_pairs.txt'
                            
                    model_all = viton_upload_model.objects.all()

                    with open(file_list_file, 'w') as f:
                        for model in model_all:
                            result_name = model.name + ' ' + item_name
                            f.write(result_name + '\n')

                    # 업로드한 사진 + 모델들 합성해서 결과 만들기
                    os.chdir('C:/hs-grad-2023/django/muapp/viton')
                    os.system(
                        "python C:/hs-grad-2023/django/muapp/viton/custom.py --name output --save_dir C:/hs-grad-2023/django/muapp/viton/data/custom/results")
                    
                    # 결과 DB 업로드
                    result_dir = "C:/hs-grad-2023/django/muapp/viton/data/custom/results/output"
                    for root, dirs, files in os.walk(result_dir):
                        for result in files:
                            # 이미지 파일 경로 생성
                            result_path = os.path.join(root, result)

                            with open(result_path, 'rb') as f:
                                file = SimpleUploadedFile(f.name, f.read())

                            # 모델 인스턴스 생성 및 저장
                            values = re.split('[_|.]',result)
                            
                            model_val = viton_upload_model.objects.filter(name__contains=values[0])
                            cloth_val = viton_upload_cloth.objects.filter(name__contains=values[1])

                            model_obj = model_val.first()
                            cloth_obj = cloth_val.first()

                            model_id = model_obj.ID
                            cloth_id = cloth_obj.ID


                            result = viton_upload_result(name=result, image=file, model_id=model_id, cloth_id=cloth_id, uploadUser=request.user.username)
                            result.save()
                    
                    # 업로드 완료한 결과 폴더 삭제
                    shutil.rmtree(result_dir)
                    

            elif getType == '모델':
                for imgfile in request.FILES.getlist('imgfile'):
                    try:
                        item = viton_upload_model.objects.create(
                            name=request.POST.get('itemName'),
                            image = imgfile,
                            uploadUser=request.user.username,
                        )
                        item.save()
                    except:
                        print('업로드 실패')

        return redirect('virtual_fit_photo', username=user.first_name)
        #return render(request,"virtual_fit_upload.html", {"user":user})
    else: 
        return render(request,"virtual_fit_upload.html", {"user":user})

@login_required(login_url='login')
def userlike(request):
    user = request.user
    clothesobject = user.likes.all()
    paginator = Paginator(clothesobject, 9)
    page = request.GET.get('page')
    clothesobject = paginator.get_page(page)
    comments = Comment.objects.all()
    
    musinsa = user.likes2.all()
    paginator = Paginator(musinsa, 9)
    page = request.GET.get('page')
    musinsa = paginator.get_page(page)
    return render(request,"userlike.html",{'cloth':clothesobject, 'comments': comments, 'musinsa': musinsa,})


from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .api import get_loc_data, get_time, get_weather_data, get_icon
from .models import clothes, photos
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm, ModifyForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.db.models import Q
from functools import reduce
from operator import or_
from allauth.socialaccount.models import SocialAccount
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
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
    user.name = social_accounts.extra_data['name']
    user.save()

def index(request):
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
            }
        return render(request,"index.html",results)
    except:
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
            'errcode' : 1
            }
        return render(request,"index.html",results)



@login_required(login_url='login')
def view_closet(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    clothesobject = clothes.objects.all()   #clothes의 모든 객체를 c에 담기
    photoobject = photos.objects.all()

    # ===== filtering ======
    fl = request.GET.get('fl')  # 검색어
    if fl: #검색어가 있고
        filterList = fl.split(',')
        q_list=[Q(uploadUser__exact=user.id)] #userID가 같은 값으로 1차 필터링
        for item in filterList:
            if "==" in item:
                type1Item = item.replace("==","").strip()
                q_list.append(Q(type1__icontains=type1Item))
            else:
                q_list.append(Q(type2__icontains=item))

        clothesobject = clothesobject.filter(reduce(or_, q_list)).distinct() # 타입 검색
        
        result = {
                'clothesobject' : clothesobject,
                'user':user,
                'filterList':filterList,
                'photoobject':photoobject,
            }
        return render(request, 'view_closet.html', result)
    else: #검색어가 없으면
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
                    new_clothes = clothes.objects.get(groupID = getGroupID)
                except clothes.DoesNotExist:
                    new_clothes = clothes.objects.create(
                                        uploadUser_id=request.user.id,
                                        uploadUserName=request.user.username,
                                        type1=request.POST.get('type1'),
                                        type2=request.POST.get('type2'),
                                        tag=request.POST.get('tags'),
                                        name=request.POST.get('clothesName'),
                                        details=request.POST.get('details'),
                                        groupID = getGroupID,
                        )
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
    clothesobject = clothes.objects.filter(Q(groupID__exact=groupID) & Q(uploadUser__exact=user.id))   #clothes의 모든 객체를 c에 담기

    photosobject = photos.objects.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('groupID')],
                    order_by='groupID_id'
                )
    )

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
    groupID_val = get_random_string(length=5)
    user = get_object_or_404(User, first_name=username) #user = User.objects.get(first_name=username) 예외 처리를 따로 하고 싶을 때 사용
    if user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        if request.FILES.getlist('imgfile'):
            for imgfile in request.FILES.getlist('imgfile'):
                # try:
                #     new_clothes = clothes.objects.get(groupID = getGroupID)
                # except clothes.DoesNotExist:
                #     new_clothes = clothes.objects.create(
                #                         uploadUser_id=request.user.id,
                #                         uploadUserName=request.user.username,
                #                         type1=request.POST.get('type1'),
                #                         type2=request.POST.get('type2'),
                #                         tag=request.POST.get('tags'),
                #                         name=request.POST.get('clothesName'),
                #                         details=request.POST.get('details'),
                #                         groupID = getGroupID,
                #         )
                #     new_clothes.save()

                # new_photo = photos.objects.create(
                #                 groupID_id=new_clothes.groupID,
                #                 imgfile = imgfile,
                # )
                # new_photo.save()
                return redirect('view_closet', username=user.first_name)
    else:
        clothesobject = clothes.objects.filter(Q(groupID__exact=groupID) & Q(uploadUser__exact=user.id))   #clothes의 모든 객체를 c에 담기
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
def remove_clothes(request, username, pk):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    
    clothesobject = clothes.objects.all()           # clothes의 모든 객체를 clothesobject에 담기
    remove_clothes= clothes.objects.get(pk=pk)      # clothes에서 pk와 같은 primary_key 값을 remove_clothes에 담기

    result={
        "user":user,
        "remove_clothes":remove_clothes,
        "clothesobject":clothesobject,
    }

    if request.method == 'POST':
        remove_clothes.delete()
        return render(request, 'view_closet.html', result) #상품목록으로 돌아가야함
    return render(request, 'remove_clothes.html', result)


@receiver(user_signed_up)
def add_social_user_name(sender, request, user, **kwargs):
    user.first_name = get_random_string(length=16)
    user.save()

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
                if result == 'modify':
                    return redirect(f'/{result}/')
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
def user_modify(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.name = request.POST["name"]
        user.sex = request.POST["sex"]
        user.height = request.POST["height"]
        user.weight = request.POST["weight"]
        user.save()
        return redirect('/')

    return render(request,"user_modify.html")
    

@login_required(login_url='login')
def blog(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    return render(request,"blog.html",{"user":user})

@login_required(login_url='login')
def virtual_fit(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return redirect(f'/virtual_fit/{request.user.first_name}')
    return render(request,"virtual_fit.html",{"user":user})


@login_required(login_url='login')
def blog(request, username):
    user = get_object_or_404(User, first_name=username)
    if user != request.user:
        return HttpResponseForbidden()
    return render(request,"blog.html",{"user":user})

def feature(request):
    return render(request,"feature.html")

# @login_required(login_url='login')
# def product(request, username):
#     user = User.objects.get(username=username)
#     return render(request,"product.html",{"user":user})


def about(request):
    return render(request,"about.html")

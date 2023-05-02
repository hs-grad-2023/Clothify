"""muproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from muapp import views
# index는 대문, blog는 게시판
# from main.views import index, blog, posting

# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    # path('404', views.404, name='404'),
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('codibook/<str:username>/',views.codibook, name='codibook'),
    path('login/', views.logins, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('upload_closet/<str:username>/',views.uploadCloset, name='uploadCloset'),
    path('view_closet/<str:username>/',views.view_closet, name='view_closet'),
    path('detail_closet/<str:username>/<str:groupID>/',views.detail_closet, name='detail_closet'),
    path('virtual_fit_photo/<str:username>/',views.virtual_fit_photo, name='virtual_fit_photo'),
    path('virtual_fit_photo_result/<str:username>/',views.virtual_fit_photo_result, name='virtual_fit_photo_result'),
    path('virtual_fit_video/<str:username>/',views.virtual_fit_video, name='virtual_fit_video'),
    path('virtual_fit_upload/<str:username>/',views.virtual_fit_upload, name='virtual_fit_upload'),
    path('update_closet/<str:username>/<str:groupID>/',views.updateCloset, name='updateCloset'),
    path('remove_closet/<str:username>/<str:groupID>/',views.remove_closet, name='remove_closet'),
    path('mypage/<str:username>/',views.mypage, name='mypage'),
    path('modify/',views.user_modify, name='user_modify'),
    path('mypage/userstyle/<str:username>',views.user_style, name='user_style'),
    path('blog/',views.blog, name='blog'),
    path('usercodi/',views.usercodi, name='usercodi'),
    path('usercodi/<str:id>/',views.detail_usercodi, name='detail_usercodi'),
    path('like/',views.like, name="likes"),
    path('like2/',views.like2, name="likes2"),
    path('virfit/', views.virfit, name='virfit'),
    path('userlike/', views.userlike, name='userlike'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
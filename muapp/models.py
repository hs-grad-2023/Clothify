import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe
from django.core.mail import send_mail

# Create your models here.

#class imgFiles(models.Model):
    #imgfile = models.ImageField(null=True, blank=True, upload_to="imgfiles/%m/%d", default='imgfiles/no_image.png')  # 이미지 컬럼 추가(사진을 여러개)
    #groupID = models.IntegerField()
    #upload_date = models.DateTimeField(default=timezone.now)

class clothes(models.Model):
    uploadUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploadUserName = models.CharField(max_length=30,default="unknown")
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    type1 = models.CharField(max_length=10)  
    type2 = models.CharField(max_length=50)
    tag = models.CharField(max_length=50, null=True,  blank=True)
    name = models.CharField(max_length=50)
    imgfile = models.ImageField(null=True, blank=True, upload_to="imgfiles/%m/%d", default='imgfiles/no_image.png')  # 이미지 컬럼 추가(사진을 여러개)
    details = models.CharField(max_length=200, default="", null=True,  blank=True, )
    upload_date = models.DateTimeField(default=timezone.now)
    id = models.AutoField(primary_key=True)
    groupID = models.CharField(max_length=10)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self): #식별자
        return self.type1 + " " + self.imgfile.name + " " +self.upload_date.strftime("%Y-%m-%d %H-%M:%S")

    def get_absolute_url(self): #옷에 따른 고유 번호 부여용
            """Returns the url to access a particular instance of MyModelName."""
            return reverse('model-detail-view', args=[str(self.id)])
    
class User(AbstractUser):
     height = models.IntegerField('키', null = True, blank = True)
     weight = models.IntegerField('몸무게', null = True, blank = True)
     sex = models.CharField('성별', max_length=1, blank=True, null=True)
     name = models.CharField('이름', max_length=4, blank=True, null=True)
     
     def email_user(self, subject, message, from_email=None, **kwargs): # 이메일 발송 메소드
          send_mail(subject, message, from_email, [self.email], **kwargs)


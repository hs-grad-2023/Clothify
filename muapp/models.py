from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import mark_safe

# Create your models here.


class clothes(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    type1 = models.CharField(max_length=10)  
    type2 = models.CharField(max_length=50)
    tag = models.CharField(max_length=50, null=True,  blank=True)
    name = models.CharField(max_length=50)
    imgfile = models.ImageField(null=True,  blank=True, upload_to="imgfiles/%m/%d",
                                default='imgfiles/no_image.png')  # 이미지 컬럼 추가(사진을 여러개)
    details = models.CharField(
        max_length=200, default="", null=True,  blank=True, )
    upload_date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self): #식별자
        return self.type1 + " " + self.imgfile.name + " " +self.upload_date.strftime("%Y-%m-%d %H-%M:%S")

    def get_absolute_url(self): #옷에 따른 고유 번호 부여용
            """Returns the url to access a particular instance of MyModelName."""
            return reverse('model-detail-view', args=[str(self.id)])
    

# class type1(models.Model):
#     name = models.CharField(max_length=200, help_text='상의, 하의.. ')
     
#     def __str__(self): #식별자
#         return self.name
    
# class type2(models.Model):
#     name = models.CharField(max_length=200, help_text='상의, 하의.. ')
     
#     def __str__(self): #식별자
#         return self.name
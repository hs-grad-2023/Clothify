from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import mark_safe

# Create your models here.


class clothes(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    type1 = models.CharField(max_length=10)  # 상의, 하의 , 아우터, 신발, 악세서리, 드레스
    # 상의(반팔, 긴팔...), 하의(반바지, 긴바지, 미니스커트, 미디스커트, 롱스커트, )
    type2 = models.CharField(max_length=50)
    # 재질이나 본인이 분류하고 싶은 내용 기재하면 좋을 듯(스웨이드, 앙고라, 가죽, 휴양지룩, 꾸안꾸룩...)
    tag = models.CharField(max_length=50, null=True,  blank=True)
    name = models.CharField(max_length=50, null=True,  blank=True)
    imgfile = models.ImageField(null=True,  blank=True, upload_to="imgfiles/%m/%d",
                                default='imgfiles/no_image.png')  # 이미지 컬럼 추가(사진을 여러개)
    # src = File.url if imgfile else None
    details = models.CharField(
        max_length=200, default="", null=True,  blank=True, )
    season = models.CharField(max_length=50, null=True,  blank=True)
    upload_date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    # price = models.IntegerField(default=0)
    # purchase_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

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
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class clothes(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    type1 = models.CharField(max_length=10) #상의, 하의 , 아우터, 신발, 악세서리, 드레스
    type2 = models.CharField(max_length=50) #상의(반팔, 긴팔...), 하의(반바지, 긴바지, 미니스커트, 미디스커트, 롱스커트, )
    tag = models.CharField(max_length=50) #재질이나 본인이 분류하고 싶은 내용 기재하면 좋을 듯(스웨이드, 앙고라, 가죽, 휴양지룩, 꾸안꾸룩...)
    name = models.CharField(max_length=50)
    imgfile = models.ImageField(null=True, upload_to="imgfiles/%m/%d", default='imgfiles/no_image.png', blank=True) # 이미지 컬럼 추가(사진을 여러개)
    details = models.CharField(max_length=200, default="")
    season = models.CharField(max_length=50)
    upload_date = models.DateField(auto_now=True)
    icode = models.IntegerField()
    # price = models.IntegerField(default=0)
    # purchase_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return self.name + " " + self.upload_date.strftime("%Y-%m-%d %H-%M:%S")
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    
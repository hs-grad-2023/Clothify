from django.db import models

# Create your models here.
# class clothes(models.Model):
#     type1 = models.CharField(max_length=10) #상의, 하의 , 아우터, 신발, 악세서리
#     type2 = models.CharField(max_length=50) #상의(반팔, 긴팔...), 하의(반바지, 긴바지, 미니스커트, 미디스커트, 롱스커트, )
#     tag = models.CharField(max_length=50) #재질이나 본인이 분류하고 싶은 내용 기재하면 좋을 듯(스웨이드, 앙고라, 가죽, 휴양지룩, 꾸안꾸룩...)
#     user
#     modify_date = models.DateTimeField(null=True, blank=True)
#     pcode = models.CharField(max_length=10)
#     pname = models.TextField()
#     unitprice = models.IntegerField(default=0)
#     discountrate = models.DecimalField(max_digits=11, decimal_places=2,default=0)
#     mainfunc = models.CharField(max_length=100, default="")
#     imgfile = models.ImageField(null=True, upload_to="", blank=True) # 이미지 컬럼 추가
#     detailfunc = models.CharField(max_length=200, default="")
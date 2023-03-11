from django.db import models

# Create your models here.


#이미지 파일이 저장된 경로를 저장할 db 테이블
class clothes(models.Model):        
    #컬럼 파일위치
    clothoes_path= models.FileField(upload_to='Uploded Files/%y/%m/%d/', blank=True)
    
    #컬럼_업로드 날짜
    clothes_date= models.DateField(auto_now=True)
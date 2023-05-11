import datetime, random, os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django_resized import ResizedImageField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class clothes(models.Model):
    uploadUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploadUserName = models.CharField(max_length=30,default="unknown")
    type1 = models.CharField(max_length=10)  
    type2 = models.CharField(max_length=50)
    tag = models.CharField(max_length=50, null=True,  blank=True)
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=200, default="", null=True,  blank=True, )
    upload_date = models.DateTimeField(default=timezone.now)
    groupID = models.CharField(max_length=10,primary_key=True)
    ucodi = models.BooleanField(null=True,  blank=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes' ,blank=True)
    # imgfile = models.ImageField(null=True, blank=True, upload_to="imgfiles/%m/%d", default='imgfiles/no_image.png')  # 이미지 컬럼 추가(사진을 여러개)    

    class Meta:
        ordering = ['-upload_date']

    def __str__(self): #식별자
        return self.type1 + " " + self.groupID + " " +self.upload_date.strftime("%Y-%m-%d %H-%M:%S")

    def get_absolute_url(self): #옷에 따른 고유 번호 부여용
            """Returns the url to access a particular instance of MyModelName."""
            return reverse('model-detail-view', args=[str(self.id)])
    

class photos(models.Model):
    groupID = models.ForeignKey(clothes, verbose_name="groupClothes", on_delete=models.CASCADE)
    photoID = models.AutoField(primary_key=True)
    imgfile = models.ImageField(null=True, blank=True, upload_to="imgfiles/%m/%d", default='imgfiles/no_image.png')  # 이미지 컬럼 추가(사진을 여러개)

# class virtual_fitting_photos(models.Model):
     

class User(AbstractUser):
     height = models.IntegerField('키', null = True, blank = True)
     weight = models.IntegerField('몸무게', null = True, blank = True)
     sex = models.CharField('성별', max_length=1, blank=True, null=True)
     name = models.CharField('이름', max_length=4, blank=True, null=True)
     style = models.CharField('스타일', max_length=50, null=True, blank=True)
     
     def email_user(self, subject, message, from_email=None, **kwargs): # 이메일 발송 메소드
          send_mail(subject, message, from_email, [self.email], **kwargs)


class Musinsa(models.Model):
    item_text = models.TextField()
    item_title = models.TextField()
    item_model = models.TextField()
    item_picture = models.URLField()
    item_page = models.URLField()
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes2' ,blank=True)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(clothes, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.post} - {self.text}'



class ResizedImageField(models.ImageField):
    def __init__(self, *args, size=None, **kwargs):
        self.size = size
        super().__init__(*args, **kwargs)

    def _resize_image(self, img):
        if self.size:
            img.thumbnail(self.size)
        return img

    def to_python(self, value):
        if isinstance(value, Image.Image):
            return value

        value = super().to_python(value)
        if value is None:
            return None

        with open(value.path, 'rb') as f:
            img = Image.open(BytesIO(f.read()))
            img = self._resize_image(img)

        # 이미지를 메모리에 저장
        img_file = BytesIO()
        img.save(img_file, 'JPEG')
        img_file.seek(0)

        return InMemoryUploadedFile(
            img_file, None, value.name, 'image/jpeg', img_file.getbuffer().nbytes, None)

def random_name_C(instance, filename):
    filename = format(random.randint(0,99999),"05d")     # 파일이 저장될 경로를 지정
    return os.path.join("datasets/cloth", filename+'.jpg')

def random_name_CM(instance, filename):
    filename = format(random.randint(0,99999),"05d")
    return os.path.join("datasets/cloth-mask", filename+'.jpg')

def random_name_M(instance, filename):
    filename = format(random.randint(0,99999),"05d")
    return os.path.join("datasets/image", filename+'.jpg')


class viton_upload_cloth(models.Model):
    clothesname = models.CharField(max_length=100,default="sample")
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[768, 1024], upload_to=random_name_C)
    maskimage = ResizedImageField(size=[768, 1024], upload_to="datasets/cloth-mask", null=True, blank=True)
    #image = ResizedImageField(size=[768, 1024], upload_to="datasets/cloth")
    uploadUser = models.CharField(max_length=30)
    uploadDate = models.DateTimeField(default=timezone.now)
    ID = models.AutoField(primary_key=True)
    class Meta:
        ordering = ['-ID']

    def save(self, *args, **kwargs):
        self.name = os.path.basename(self.image.name)
        # 이미지가 업로드되지 않았거나 이미지 크기가 조정되지 않았다면
        if not self.pk or self.image.width > self.image.field.size[0]:
            # 업로드된 이미지를 메모리에서 읽어와서 크기를 조정
            with BytesIO(self.image.read()) as f:
                img = Image.open(f)
                img = img.resize(self.image.field.size)
                img_file = BytesIO()
                img.save(img_file, 'JPEG')
                img_file.seek(0)

            # InMemoryUploadedFile로 변환하여 저장
            self.image = InMemoryUploadedFile(
                img_file, None, self.image.name, 'image/jpeg', img_file.getbuffer().nbytes, None)

        super().save(*args, **kwargs)

class viton_upload_model(models.Model):
    clothesname = models.CharField(max_length=100,default="sample")
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[768, 1024], upload_to=random_name_M)
    maskmodel = ResizedImageField(size=[768, 1024], upload_to="datasets/image-parse", null=True, blank=True)
    openposeImage = ResizedImageField(size=[768, 1024], upload_to="datasets/openpose-img", null=True, blank=True)
    openposeJson = models.FileField(upload_to="datasets/openpose-json", null=True, blank=True)
    #image = ResizedImageField(size=[768, 1024], upload_to="datasets/model")
    uploadUser = models.CharField(max_length=30)
    uploadDate = models.DateTimeField(default=timezone.now)
    ID = models.AutoField(primary_key=True)
    class Meta:
        ordering = ['-ID']
    def save(self, *args, **kwargs):
        # 이미지가 업로드되지 않았거나 이미지 크기가 조정되지 않았다면
        if not self.pk or self.image.width > self.image.field.size[0]:
            # 업로드된 이미지를 메모리에서 읽어와서 크기를 조정
            with BytesIO(self.image.read()) as f:
                img = Image.open(f)
                img = img.resize(self.image.field.size)
                img_file = BytesIO()
                img.save(img_file, 'JPEG')
                img_file.seek(0)

            # InMemoryUploadedFile로 변환하여 저장
            self.image = InMemoryUploadedFile(
                img_file, None, self.image.name, 'image/jpeg', img_file.getbuffer().nbytes, None)

        super().save(*args, **kwargs)

class viton_upload_result(models.Model):
    name = models.CharField(max_length=50, unique=True)
    model = models.ForeignKey("viton_upload_model", on_delete=models.CASCADE)
    cloth = models.ForeignKey("viton_upload_cloth", on_delete=models.CASCADE)
    image = ResizedImageField(size=[768, 1024], upload_to='datasets/results')
    uploadUser = models.CharField(max_length=50, default='sample')
    class Meta:
        ordering = ['-id']
    def save(self, *args, **kwargs):
        # 이미지가 업로드되지 않았거나 이미지 크기가 조정되지 않았다면
        if not self.pk or self.image.width > self.image.field.size[0]:
            # 업로드된 이미지를 메모리에서 읽어와서 크기를 조정
            with BytesIO(self.image.read()) as f:
                img = Image.open(f)
                img = img.resize(self.image.field.size)
                img_file = BytesIO()
                img.save(img_file, 'JPEG')
                img_file.seek(0)

            # InMemoryUploadedFile로 변환하여 저장
            self.image = InMemoryUploadedFile(
                img_file, None, self.image.name, 'image/jpeg', img_file.getbuffer().nbytes, None)

        super().save(*args, **kwargs)

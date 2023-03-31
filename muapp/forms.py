from django import forms
from .models import clothes
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

# class ProductForm(forms.ModelForm): # ModelForm 은 장고 모델 폼
#     class Meta: # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
#         model = clothes
#         fields = ['type1', 'type2', 'tag', 'name', 'imgfile', 'details','upload_date']
#         labels = {
#             'type1': '분류1',
#             'type2': '분류2',
#             'tag': '태그',
#             'name': '이름',
#             'imgfile': '사진',
#             'details': '상세정보',
#             'upload_date' : '업로드날짜',
#         }

User = get_user_model()
class UserForm(UserCreationForm):


    email = forms.EmailField(label="이메일", error_messages={'required': '이메일을 입력해주세요.','invalid': '올바른 이메일 주소를 입력해주세요.'})
    username = forms.CharField(label="아이디", error_messages={'required': '아이디를 입력해주세요.'})
    password1 = forms.CharField(label="비밀번호", error_messages={'required': '비밀번호를 입력해주세요.'})
    password2 = forms.CharField(label="비밀번호 확인", error_messages={'required': '비밀번호 확인을 입력해주세요.'})
    name = forms.CharField(label="이름", error_messages={'required': '이름을 입력해주세요.'})
    sex = forms.CharField(label="성별", error_messages={'required': '성별을 선택해주세요.'})
    height = forms.IntegerField(label="키", error_messages={'required': '키를 입력해주세요.'})
    weight = forms.IntegerField(label="몸무게", error_messages={'required': '몸무게를 입력해주세요.'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("이미 존재하는 아이디입니다.")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")
        return email
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "name", "sex", "height", "weight")
        
    
class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': '아이디나 비밀번호가 틀립니다.',
    }
    username = forms.CharField(label='아이디', error_messages={'required': '아이디를 입력해주세요.'})
    password = forms.CharField(label='비밀번호', error_messages={'required': '비밀번호를 입력해주세요.'})

class ModifyForm(UserChangeForm):
    email = forms.EmailField(label="이메일", error_messages={'required': '이메일을 입력해주세요.','invalid': '올바른 이메일 주소를 입력해주세요.'})
    username = forms.CharField(label="아이디", error_messages={'required': '아이디를 입력해주세요.'})
    name = forms.CharField(label="이름", error_messages={'required': '이름을 입력해주세요.'})
    sex = forms.CharField(label="성별", error_messages={'required': '성별을 선택해주세요.'})
    height = forms.IntegerField(label="키", error_messages={'required': '키를 입력해주세요.'})
    weight = forms.IntegerField(label="몸무게", error_messages={'required': '몸무게를 입력해주세요.'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and username != self.instance.username:
            raise ValidationError("이미 존재하는 아이디입니다.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            raise ValidationError("이미 존재하는 이메일입니다.")
        return email
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'name', 'sex', 'height', 'weight')

   
        


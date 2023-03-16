from django import forms
from .models import clothes

class ProductForm(forms.ModelForm): # ModelForm 은 장고 모델 폼
    class Meta: # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
        model = clothes
        fields = ['type1', 'type2', 'tags', 'name', 'imgfile', 'details', 'season','upload_date']
        labels = {
            'type1': '분류1',
            'type2': '분류2',
            'tags': '태그',
            'name': '이름',
            'imgfile': '사진',
            'details': '상세정보',
            'season': '계절',
            'upload_date' : '업로드날짜',
        }
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import clothes, User

# Register your models here.


#admin.site.register(clothes) #관리자가 옷(clothes)에 접근 가능
class clothesAdmin(admin.ModelAdmin):
    list_display = ('id','type1', 'type2', 'name', 'imgfile','upload_date')
    list_filter = ('type1', 'type2')
    fields = [('type1', 'type2'),'name','tags','imgfile','details']
    readonly_fields=('id','upload_date')

# Register the admin class with the associated model
admin.site.register(clothes, clothesAdmin)
admin.site.register(User, UserAdmin)

#모든 관리자 사이트 사용자화(customisation) 선택들(choices)의 완벽한 레퍼런스(reference)를 The Django Admin site(장고 문서)에서 찾을 수 있습니다.
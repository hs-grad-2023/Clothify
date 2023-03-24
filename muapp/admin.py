from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import clothes, User

# Register your models here.


#admin.site.register(clothes) #관리자가 옷(clothes)에 접근 가능
class clothesAdmin(admin.ModelAdmin):
    list_display = ('id','type1', 'type2', 'name', 'imgfile', 'upload_date')
    list_filter = ('type1', 'type2')
    fields = [('type1', 'type2'),'name','tag','imgfile','details']
    readonly_fields=('id','upload_date')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'first_name', 'password', 'email', 'height', 'weight', 'sex', 'joined_at', 'last_login_at', 'is_superuser')
    list_display_links = ('id', 'name', 'email', 'username')
    exclude = ('password',)

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")
    
    joined_at.admin_order_field = '-date_joined'      
    joined_at.short_description = '가입일'

    last_login_at.admin_order_field = 'last_login_at'
    last_login_at.short_description = '최근 로그인'

# Register the admin class with the associated model
admin.site.register(clothes, clothesAdmin)
admin.site.register(User, UserAdmin)

#모든 관리자 사이트 사용자화(customisation) 선택들(choices)의 완벽한 레퍼런스(reference)를 The Django Admin site(장고 문서)에서 찾을 수 있습니다.
from django.contrib import admin
from .models import User

# Register your models here.
# 신규 생성한 user 모델을 
class UserAdmin(admin.ModelAdmin):
    list_display=('user_id', 'registered_dttm')

admin.site.register(User, UserAdmin)
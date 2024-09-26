from django.db import models

# Create your models here.
class User(models.Model):
    user_id=models.CharField(max_length=64, verbose_name='사용자 아이디')
    useremail = models.EmailField(max_length=128, verbose_name="사용자 이메일")
    password=models.CharField(max_length=64, verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')    

    def __str__(self):
        # 오버라이딩하여 관리자페이지에서 원하는 문자열로 표기되게 설정
        # 유저 id로 표기되게 설정
        return self.user_id
    
    class Meta:
        # 모델의 클래스 이름이 아니라 특정 테이블과 모델을 연결하고 싶을 때
        db_table = 'tb_user' # 사용할 db 및 테이블 지정(마이그레이션 해야 함) # db에 user_user로 되어있던 테이블이 tb_user로 변경됨
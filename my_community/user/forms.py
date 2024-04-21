from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    # 장고 프레임의 form을 사용하여 로그인 폼 생성
    user_id = forms.CharField(max_length=64, label='사용자 아이디', error_messages={'required': "아이디를 입력해 주세요"})
    password = forms.CharField(max_length=64, label='비밀번호', widget=forms.PasswordInput, error_messages={'required': "비밀번호를 입력해 주세요"})

    def clean(self):
        # 기본적인 유효성 검증을 먼저 수행하기 위해 부모 클래스의 clean()을 먼저 실행
        # 값이 모두 들어있는지를 검사합니다.
        # 값이 모두 들어있지 않으면 여기에서 이미 실패처리가 됩니다.
        cleaned_data = super().clean()
    
        # cleaned_data는 부모 클래스의 유효성 검증 결과가 들어 있습니다.
        # form.POST 객체이며, 여기서 사용자가 입력한 데이터를 꺼내올 수 있습니다.
        user_id = cleaned_data.get("user_id")
        password = cleaned_data.get("password")
    
        # user_id와 패스워드가 모두 존재한다면
        if user_id and password:
            # user_id를 이용해 사용자 조회
            user = User.objects.get(user_id=user_id)
    
            if not check_password(password, user.password):
                # 비밀번호가 틀리면 에러 메시지 설정
                self.add_error("password", "비밀번호를 틀렸습니다.")
            else:
                # 비밀번호가 맞은 경우 사용자의 pk를 변수에 저장
                self.user_id=user.id
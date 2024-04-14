from django.shortcuts import render
from django.contrib.auth.hashers import make_password # 회원가입 시 비번 암호화
from .models import User # (특정앱의) models.py에 정의한 User 모델을 CRUD하기 위해 import

# Create your views here.
def register(request):
		# 사용자의 요청이 GET인 경우
    if request.method == 'GET':
        return render(request, 'register.html')
    

		# 사용자의 요청이 POST인 경우
    elif request.method == 'POST':
        # 각 input tag에서 name 속성값을 이용해 사용자가 보낸 값을 꺼내옵니다.
        user_id = request.POST.get('user_id', None) # 사용자가 보낸 데이터가 없는 경우 오류 페이지가 보이지 않고 None으로 표기
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)

        # 가입 시 비밀번호 일치 확인을 위해 받아옵니다.
        # 실제로는 frontend에서 담당하지만, 여기서는 backend에서 담당하도록 하겠습니다.
        re_password = request.POST.get('re-password', None)
        # print(f"user_id={user_id}")
        # print(f"useremail={useremail}")
        # print(f"password={password}")
        # print(f"re_password={re_password}")

        # 사용자에게 전달할 오류 메세지 정의
        # 사용자에게 전달할 데이터를 담을 딕셔너리 → attribute
        res_data = {} # attribute: 클라이언트에게 전달하는 데이터 지칭

        if not (user_id and useremail and password and re_password):
            res_data['error'] = "모든 값을 입력해야 합니다."
        elif password != re_password:
            res_data['error'] = "비밀번호가 다릅니다~!"
        else:
            # 정의한 User 모델에 입력받은 데이터 넣고 저장
            user = User(user_id=user_id,password=make_password(password))
            user.save() # Meta 클래스에 지정한 tb_user 테이블에 데이터 삽입됨
        print('print request: ', request)
        # 클라이언트에게 데이터 전달 시 에러메세지도 같이 전달
        return render(request, 'register.html', res_data)
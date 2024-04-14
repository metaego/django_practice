# redirect: 사용자를 강제로 다른 페이지로 요청 수행
from django.shortcuts import render, redirect

# HttpResponse: response로 특정 문자열 출력 
from django.http import HttpResponse 

# make_password: 회원가입 시 비번 암호화 # check_password: 암호화한 비번이 DB 사용자 pw와 일치하는지 확인하는 함수
from django.contrib.auth.hashers import make_password, check_password 

#(특정앱의) models.py에 정의한 User 모델을 CRUD하기 위해 import
from .models import User 



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
    
def login(request):
    
    # GET으로 들어오면 로그인 화면 렌더링
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)

        res_data = {}

        # 아이디나 패스워드를 입력하지 않은 경우
        if not (user_id and password):
            res_data['error'] = "모든 값을 입력해야 합니다."
        else:
            # 모든 값이 제대로 들어왔으면 로그인 로직 수행
            # user_id와 일치하는 정보가 있는지 조회
            user = User.objects.get(user_id=user_id) # db 조회해서 데이터 가져오기

            if check_password(password, user.password):
                # 비밀번호가 일치하면 로그인 처리 (세션)
                request.session['user'] = user.id

                # home으로 redirect
                return redirect('/')
            else:
                # 에러메시지 넣어주기
                res_data['error'] = "비밀번호가 틀렸습니다."

        return render(request, 'login.html', res_data)
    
def home(request):
    # 세션에 저장된 user의 id(uid) 가져오기
    uid = request.session.get('user')

    # uid가 존재한다면
    if uid:
        # 모델을 이용해 데이터베이스에서 uid를 넣어서 조회
        user = User.objects.get(pk=uid)
        return HttpResponse(f"{user.user_id}")
    
    # 간단한 응답 결과를 보여주기위해 HttpResponse 메소드 사용
    return HttpResponse('home')

def logout(request):
    # 현재 로그인한 사용자의 정보가 세션에 존재하면
    if request.session.get('user'):
        del(request.session['user']) # user 정보 삭제
    
    # 로그아웃 수행 후 홈 페이지로 이동
    return redirect("/")
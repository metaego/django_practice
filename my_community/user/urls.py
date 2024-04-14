from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register), # views.py 파일의 register라는 함수로 request 요청 실행
    path('login/', views.login),
    path('logout/', views.logout), 
]
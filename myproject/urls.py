"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import (
    login_v,signup, student_list, student_detail, score_list, score_detail, add_student, add_score
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', student_list, name='student_list'),
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('score/', score_list, name='score_list'), # 更新 score_list 路由
    path('score/<int:score_id>/', score_detail, name='score_detail'), # 更新 score_detail 路由
    path('add_student/', add_student, name='add_student'),
    path('add_score/', add_score, name='add_score'),

    # 登录
    path('login/', login_v, name='login_v'),
    # 注销
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 注册
    path('signup/', signup, name='signup'),
]
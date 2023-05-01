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
from django import views
from django.contrib import admin
from django.urls import include, path
from myapp.views import (
    checkin, dashboard, login_v,signup, student_list, student_detail, score_list, score_detail, add_student, add_score, unbind_student, user_center
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('checkin/', checkin, name='checkin'),
    path('admin/', admin.site.urls),
    path('student', student_list, name='student_list'),
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('score/', score_list, name='score_list'), # 更新 score_list 路由
    path('score/<int:score_id>/', score_detail, name='score_detail'), # 更新 score_detail 路由
    path('add_student/', add_student, name='add_student'),
    path('add_score/', add_score, name='add_score'),
    path('user_center/', user_center, name='user_center'),
    path('unbind_student/<int:student_id>/', unbind_student, name='unbind_student'),
    
    # 登录
    path('login/', login_v, name='login_v'),
    # 注销
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 注册
    path('signup/', signup, name='signup'),

    #使用Django-Plotly-Dash。
    
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
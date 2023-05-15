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
    checkin, checkin_list, create_class, dashboard, delete_class, get_all_classes, get_class, load_more_checkins, login_v, logout_view,signup, student_list, student_detail, score_list, score_detail, add_student, add_score, unbind_student, update_class, user_center
)
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', dashboard, name='dashboard'),
    # path('', student_list, name='student_list'),
    path('checkin/', checkin, name='checkin'),
    path('checkin_list',checkin_list,name='checkin_list'),
    path('admin/', admin.site.urls),
    path('student', student_list, name='student_list'),
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('score/', score_list, name='score_list'), # 更新 score_list 路由
    path('score/<int:score_id>/', score_detail, name='score_detail'), # 更新 score_detail 路由
    path('add_student/', add_student, name='add_student'),
    path('add_score/', add_score, name='add_score'),
    path('user_center/', user_center, name='user_center'),
    path('unbind_student/<int:student_id>/', unbind_student, name='unbind_student'),
    path('load-more-checkins/', load_more_checkins, name='load_more_checkins'),
    # 登录
    path('login/', login_v, name='login_v'),
    # 注销
    path('logout/', logout_view, name='logout'),
    # 注册
    path('signup/', signup, name='signup'),

    #使用Django-Plotly-Dash。
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    path('create_class/', create_class, name='create_class'),
    path('classes/<int:class_id>/', update_class, name='update_class'),
    path('classes/<int:class_id>/delete/', delete_class, name='delete_class'),
    path('classes/<int:class_id>/', get_class, name='get_class'),
    path('classes/', get_all_classes, name='get_all_classes'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
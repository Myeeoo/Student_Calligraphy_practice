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
    password_reset,browse_xlsx, checkin, checkin_list, commit_logs, create_class, dashboard, delete_class, execute_update_commit_logs, get_all_classes, get_class, like_checkin, load_more_checkins, login_v, logout_view,signup, student_list, student_detail, score_list, score_detail, add_student, add_score, submit_feedback, unbind_student, update_class, update_student, user_center
)
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('browse_xlsx/', browse_xlsx, name='browse_xlsx'),
    path('feedback/', submit_feedback, name='submit_feedback'),
    path('', dashboard, name='dashboard'),
    path('checkin/', checkin, name='checkin'),
    path('checkin_list',checkin_list,name='checkin_list'),
    path('admin/', admin.site.urls),
    path('student', student_list, name='student_list'),
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('student/<int:student_id>/update/', update_student, name='update_student'),
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
    path('like_checkin/<int:checkin_id>/', like_checkin, name='like_checkin'),
    path('commit-logs/', commit_logs, name='commit_logs'),
    path('execute-update-commit-logs/', execute_update_commit_logs, name='execute_update_commit_logs'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
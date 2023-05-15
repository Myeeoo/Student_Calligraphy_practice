from copy import copy
import datetime
from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from pyexpat.errors import messages as msg
from telnetlib import LOGOUT
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from myapp.templatetags.custom_filters import time_since_checkin
from .models import Student, Score
from .forms import BindStudentForm, ScoreForm
from django.forms import modelformset_factory
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Checkin,Classes
from .forms import CheckinForm
from django.contrib.auth import logout
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime , timedelta
from django.shortcuts import render
from .models import Checkin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_class(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Classes.create(name=name)
            return JsonResponse({'success': True, 'message': 'Class created successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid data.'})

@csrf_exempt
def update_class(request, class_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            class_obj = Classes.get_by_id(class_id)
            if name:
                class_obj.update(name=name)
                return JsonResponse({'success': True, 'message': 'Class updated successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data.'})
        except Classes.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Class does not exist.'})

@csrf_exempt
def delete_class(request, class_id):
    try:
        Classes.delete_by_id(class_id)
        return JsonResponse({'success': True, 'message': 'Class deleted successfully.'})
    except Classes.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Class does not exist.'})

def get_class(request, class_id):
    try:
        class_obj = Classes.get_by_id(class_id)
        class_data = {'id': class_obj.id, 'name': class_obj.name}
        return JsonResponse({'success': True, 'class': class_data})
    except Classes.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Class does not exist.'})

def get_all_classes(request):
    classes = Classes.get_all()
    class_list = [{'id': c.id, 'name': c.name} for c in classes]
    return JsonResponse({'success': True, 'classes': class_list})

def load_more_checkins(request):
    page_number = request.GET.get('page')
    per_page = 5
    if page_number is not None:
        start_index = (int(page_number) - 1) * per_page
        end_index = start_index + per_page
    else:
        start_index = 0
        end_index = per_page

    checkins = Checkin.objects.all().order_by('-checkin_date')[start_index:end_index]
    
    # 将打卡记录数据转化为 JSON 格式
    checkins_data = []
    for checkin in checkins:
        checkin_data = {
            'name': checkin.student.name,
            'class': checkin.student.Classes.name,
            'checkin_date': checkin.checkin_date.strftime('%Y-%m-%d %H:%M:%S'),
            'checkin_text': checkin.checkin_text,
            'checkin_image_url': checkin.checkin_image.url if checkin.checkin_image else '',
            'score':checkin.score,
            # 其他字段...
        }
        checkins_data.append(checkin_data)
    has_next_page = len(checkins) == per_page
    # print('len(checkins):',len(checkins))
    # print(has_next_page)
    response_data = {
        'checkins': checkins_data,
        'has_next_page': has_next_page,
    }

    return JsonResponse(response_data)


def checkin_list(request):
    checkins = Checkin.objects.all().order_by('-checkin_date')
    return render(request, 'checkin_list.html', {'checkins': checkins})

def dashboard(request):
    today = datetime.now().date()

    # 本周的起始日期和结束日期
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = this_week_start + timedelta(days=6)


    # 统计学生总数
    Score_num_students = Student.objects.count()

    # 总分排行榜
    Score_top_students = Score.objects.values('student__name').annotate(total_score=Sum('score')).order_by('-total_score')[:10]
    
    Score_topOne = Score.objects.values('student__name').annotate(total_score=Sum('score')).order_by('-total_score').first()
    # 本周最高分
    Score_this_week_high_score = Score.objects.filter(date__range=[this_week_start, this_week_end]).order_by('-score').first()

    # 本周最高加分
    Score_this_week_high_add_score = Score.objects.filter(date__range=[this_week_start, this_week_end]).order_by('-add_score').first()
    # Get the number of students
    num_students = Student.objects.count()

    # 本周打卡人数
    num_checkins_this_week = Checkin.objects.filter(checkin_date__date__range=[this_week_start, this_week_end]).count()

    # 总打卡人数
    num_checkins_total = Checkin.objects.all().count()

    # Get the number of students who have checked in today
    num_checkins_today = Checkin.objects.filter(checkin_date__date=datetime.now().date()).count()

    # Get the top 10 students with the most points
    top_students = Student.objects.annotate(total_score=Sum('checkin__score')).order_by('-total_score')[:10]


    # Get the total number of points
    total_points = Checkin.objects.aggregate(Sum('score'))['score__sum'] or 0

    # print(num_students)
    checkins = Checkin.objects.all().order_by('-checkin_date')[:5]

    context = {
        'Score_topOne':Score_topOne,
        'Score_num_students':Score_num_students,
        'Score_top_students':Score_top_students,
        'Score_this_week_high_score':Score_this_week_high_score,
        'Score_this_week_high_add_score':Score_this_week_high_add_score,
        'num_checkins_this_week':num_checkins_this_week,
        'num_checkins_total':num_checkins_total,
        'num_students': num_students,
        'num_checkins_today': num_checkins_today,
        'top_students': top_students,
        'total_points': total_points,
        'checkins': checkins,
    }

    return render(request, 'dashboard.html', context)


@login_required
def unbind_student(request, student_id):
    # 获取当前登录用户
    user = request.user
    
    # 根据 student_id 获取学生实例
    student = get_object_or_404(Student, pk=student_id)
    
    # 判断当前用户是否绑定了该学生
    if user.student_set.filter(pk=student_id).exists():
        
        # 解绑学生和用户之间的 ManyToManyField 关系
        user.student_set.remove(student)
        
        # 返回成功信息
        messages.success(request, f"解绑 {student.name} 成功！")
    else:
        # 返回失败信息
        messages.error(request, f"你没有绑定 {student.name}！")
    
    # 重定向回用户中心页面
    return redirect('user_center')

@login_required
def user_center(request):
    All_students = Student.objects.all()#user.student_set.all()
    mystudent = request.user.student_set.all()
    print(mystudent)
    form = BindStudentForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        student = form.cleaned_data['student']
        form.cleaned_data['user']= request.user
        form.save()
        messages.success(request, '绑定成功！')
        return redirect('user_center')
    else:
        try:
            user = request.user
            
            # student = request.user.student
            student = request.user.student_set.first()
        except Student.DoesNotExist:
            student = None
        context = {
            'Student': mystudent,
            'students':All_students,
            'form': form
            }
        return render(request, 'user_center.html', context)
    
@login_required
def checkin(request):
    if request.method == 'POST':
        form = CheckinForm(request.user, request.POST, request.FILES)
        print(form)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.checkin_date = datetime.now().date()  # 设置为今天的日期
            checkin.student = form.cleaned_data['student']

            # 检查是否已经打卡
            existing_checkin = Checkin.objects.filter(student=checkin.student, checkin_date__date=checkin.checkin_date).first()

            if existing_checkin:
                messages.error(request, f'{checkin.student.name}今天已经打过卡了！')
                return redirect('/')
            
            checkin.score = calculate_score(checkin)
            checkin.save()
            messages.success(request, f'{checkin.student.name}打卡成功！刻苦练习获得{checkin.score}积分！')
            return redirect('/')
        else:
            messages.error(request, '打卡出错！')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CheckinForm(request.user)
        
        # print(form)

    
    # print(form.as_p()) # 打印表单HTML的渲染结果
    # 获取当前用户的绑定学生列表
    # mystudent = request.user.studentuser_set.all().values_list('student', flat=True)
    mystudent = Student.objects.filter(user=request.user)
    
    # 将 mystudent 传递到模板中
    return render(request, 'checkin.html', {'form': form, 'mystudent': mystudent})

def calculate_score(checkin):
    print(checkin)
    print(checkin.checkin_date)
    # 基础积分为 3 分
    score = 3
    # 如果打卡文字和图片都有，则额外加 2 分
    if checkin.checkin_text and checkin.checkin_image:
        score += 2
    # 如果是周末，则额外加 2 分
    if checkin.checkin_date.weekday() >= 5:
        score += 2
    # 如果是连续打卡，则额外加 3 分
    student = checkin.student
    if student.last_checkin_date and \
            (checkin.checkin_date - student.last_checkin_date).days == 1:
        score += 3
    student.last_checkin_date = checkin.checkin_date
    student.save()
    return score

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, '注册成功！')
            return redirect('/')
        else:
            messages.error(request, '注册失败！')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_v(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, '用户名或密码错误')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, '成功退出！')
    return redirect('/')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    scores = Score.objects.filter(student=student)
    return render(request, 'student_detail.html', {'student': student, 'scores': scores})

def score_list(request):
    # 查询 Score 模型并按日期分组
    scores = Score.objects.order_by('date').values('date').distinct()
    print(scores)
    score_list = {}
    for score in scores:
        date = score['date']
        score_list[date] = Score.objects.filter(date=date)
    return render(request, 'score_list.html', {'scores': score_list})

def score_detail(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    return render(request, 'score_detail.html', {'score': score})

def add_student(request):
    # 处理添加学生信息的逻辑
    if request.method == 'POST':
        # 获取表单提交的数据
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        grade = request.POST.get('grade')

        # 创建学生对象并保存到数据库
        # student = Student.objects.create(student_id=student_id, name=name, sex=sex, age=age, grade=grade)
        student = Student.objects.create(
            name=name, sex=sex, age=age, grade=grade)
        student.save()
        # 重定向到学生列表页面
        return redirect('student_list')
    classes = Classes.objects.all()
    print(classes)
    context = {
        'classes': classes
    }
    return render(request, 'add_student.html',context)

   #原
def add_score(request):

    if request.method == 'POST':
        students = Student.objects.all()
        print(request.POST)
        post_data = request.POST.copy()
        # forms = [ScoreForm(post_data,student_id=student.student_id) for student in students]
        forms = [ScoreForm(request.POST, student=student,student_id=student.student_id) for student in students]
        print(len(forms))
        
        for student, form in zip(students, forms):
                form.fields['score'].widget.attrs.update({'name': f'score_{student.pk}'})
                form.fields['add_score'].widget.attrs.update({'name': f'add_score_{student.pk}'})
                
                
        
        # for form, student in zip(forms, students):
        #     form.fields['student'].queryset = Student.objects.filter(pk=student.pk)        
        if all(form.is_valid() for form in forms):
            for student, form in zip(students, forms):
                #form.student=student
                form.cleaned_data['student'] = student  # 将学生实例添加到表单数据中
                form.score = request.POST.get('score_%d' % student.pk)
                form.add_score = request.POST.get('add_score_%d' % student.pk)
                form.cleaned_data['score'] = request.POST.get('score_%d' % student.pk)
                form.cleaned_data['add_score'] = request.POST.get('add_score_%d' % student.pk)
                #print(form.score)
                
                # print(form.student)
                # print("姓名：", form.data.get('student'))
                # print("学生编号：", form.cleaned_data.get('student_id'))
                # print("得分:",form.cleaned_data['score'])
                
                # print(form.cleaned_data)
                # form.cleaned_data['student'] = student
                if form.is_valid():
                    form.save()# 保存表单数据到数据库
                else:
                    print("出错:")
                    print("姓名：", form.data.get('student'))
                    print("学生编号：", form.cleaned_data.get('student_id'))
                    print("得分:",form.cleaned_data['score'])
            return redirect('score_list')  # 保存成功后重定向到分数列表页面
        else:
            for field_name, error_messages in form.errors.items():
                print(field_name)
                for error_message in error_messages:
                    print(error_message)
            print("数据验证不合法！")
        
    else:
        students = Student.objects.all()
        forms = [ScoreForm(initial={'student': student, 'student_id': student.student_id,'score': 80, 'add_score': 0}) for student in students]
        for form ,student  in zip(forms,students):
            if form:
                student_pk = student.pk
                form.fields['score'].widget.attrs.update({'id': f'score_{student_pk}'})
                form.fields['add_score'].widget.attrs.update({'id': f'add_score_{student_pk}'})

                # 通过构造函数初始化表单类实例，并将提交的表单数据作为参数传递给它
                score = request.POST.get('score_%d' % student_pk)
                add_score = request.POST.get('add_score_%d' % student_pk)
                form = ScoreForm(request.POST, instance=form.instance, initial={'score': score, 'add_score': add_score})

        # 执行验证和清理，并将结果存储在 cleaned_data 字典中
        if form.is_valid():
            score = form.cleaned_data['score']
            add_score = form.cleaned_data['add_score']
            # do something with score and add_score
    context = {
        'students_forms': zip(students, forms)
    }
    return render(request, 'add_score.html', context)

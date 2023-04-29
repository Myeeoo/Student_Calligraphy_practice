from copy import copy
import datetime
from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from pyexpat.errors import messages as msg
from telnetlib import LOGOUT
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Score
from .forms import ScoreForm
from django.forms import modelformset_factory
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
    LOGOUT(request)
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

    return render(request, 'add_student.html')
# def add_score(request):
    ScoreFormSet = modelformset_factory(
        Score, form=ScoreForm, extra=0, fields=['student', 'score', 'add_score', 'date'])
    if request.method == 'POST':
        formset = ScoreFormSet(request.POST)
        if formset.is_valid():
            # 处理表单数据
            for form in formset:
                if form.is_valid():
                    student_pk = form.cleaned_data['student'].pk
                    score = request.POST.get('%s_%d' % (form.fields['score'].widget.attrs['name'], student_pk))
                    add_score = request.POST.get('%s_%d' % (form.fields['add_score'].widget.attrs['name'], student_pk))
                    date = request.POST.get('%s_%d' % (form.fields['date'].widget.attrs['name'], student_pk))
                    score_obj = form.save(commit=False)
                    score_obj.score = score
                    score_obj.add_score = add_score
                    score_obj.date = date
                    score_obj.save()
            messages.success(request, '分数保存成功！')
            return redirect('list_score')
        else:
            # 表单验证失败，返回带有错误信息的表单页面
            queryset = Student.objects.all().order_by('student_id')
            students_forms = []
            for form, student in zip(formset, queryset):
                students_forms.append((student, form))
            context = {
                'formset': formset,
                'students_forms': students_forms,
            }
             # 添加错误信息到上下文中
            errors_forms = []
            errors = formset.errors
            for error, field_errors in zip(errors, form.errors.values):
                errors_forms.append((error, field_errors))

            if errors:
                context['errors'] = errors_forms
            return render(request, 'add_score.html', context)
    else:
        queryset = Student.objects.all().order_by('student_id')
        formset = ScoreFormSet(queryset=queryset)
        students_forms = []
        for form, student in zip(formset, queryset):
            students_forms.append((student, form))
        context = {
            'formset': formset,
            'students_forms': students_forms,
        }
        return render(request, 'add_score.html', context)

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

# def add_score(request):
#     ScoreFormSet = modelformset_factory(Score, form=ScoreForm, extra=0, fields=['student', 'score', 'add_score'])
#     queryset = Student.objects.all()
#     formset = ScoreFormSet(queryset=queryset)
    
#     if request.method == 'POST':
#         formset = ScoreFormSet(request.POST)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 student_id = instance.student_id
#                 student = Student.objects.get(pk=student_id)
#                 instance.student = student
#                 instance.save()
#             return redirect('score_list')
#         else:
#             print("数据验证不合法！")
#     else:
#         queryset = Student.objects.all()
#         formset = ScoreFormSet(queryset=queryset)
        
#     context = {
#         'formset': formset
#     }
#     return render(request, 'add_scorenew.html', context)

def add_score2(request):
    # 获取所有学生列表
    students = Student.objects.all()

    # 构造所有学生对应的成绩表单
    ScoreFormSet = modelformset_factory(Score, form=ScoreForm, extra=0)
    scores = Score.objects.filter(student__in=students)
    formset = ScoreFormSet(queryset=scores)

# 手动指定每个表单的 queryset
    for form, student in zip(formset.forms, students):
        form.fields['student'].queryset = Student.objects.filter(pk=student.pk)
        
    # 将所有学生和对应的成绩表单组合成一个二元组，并传递给模板
    students_forms = zip(students, formset.forms)
    context = {'students_forms': students_forms}

    if request.method == 'POST':
        formset = ScoreFormSet(request.POST)#[ScoreFormSet(request.POST) for student in students] #ScoreFormSet(request.POST)
        print(formset)
        #if all(form.is_valid() for form in forms):
        for form in formset:
            print(form)
            print("1")
        if all(form.is_valid() for form in formset):
            formset.save()
            print('成绩更新成功！')
            return redirect('score_list')
        else:
            for field_name, error_messages in form.errors.items():
                print(field_name)
                for error_message in error_messages:
                    print(error_message)
            print("数据验证不合法！")
    
    else:
        forms = []
        for student in students:
            form_data = {
                'student': student,
                'score': 80,
                'add_score': 0,
                'date': datetime.date.today(),
            }
            form = ScoreForm(data=form_data)
            forms.append(form)
            
    context = {
        'students_forms': zip(students, forms)
    }
    return render(request, 'add_score.html', context=context)
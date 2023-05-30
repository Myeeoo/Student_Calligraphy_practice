from django import forms
from .models import Score, Student, Checkin, StudentUser, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BindStudentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(user=None), label='学生姓名',widget=forms.Select(attrs={'class': 'form-control'}))
    user = forms.ModelChoiceField(queryset=User.objects.none(), widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BindStudentForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['user'].queryset = User.objects.filter(id=self.user.id)
            self.fields['user'].initial = self.user

    class Meta:
        model = StudentUser
        fields = ['student','user']


class CheckinForm(forms.ModelForm):
    checkin_text = forms.CharField(initial="成长可见，未来可期！",max_length=200, required=True, widget=forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),label='打卡感言')  # 一句话
    checkin_image = forms.ImageField(required=True,label='打卡感言')  # 练习照片

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['student'].queryset = Student.objects.filter(user=user)
        else:
            self.fields['student'].queryset = Student.objects.none()



    class Meta:
        model = Checkin
        fields = ['student', 'checkin_text', 'checkin_image']

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='必填项')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets ={
            'username': forms.TextInput(attrs={'class': 'form-control'}), 
            'email' : forms.TextInput(attrs={'class': 'form-control'}), 
            'password1':forms.PasswordInput(attrs={'class': 'form-control'}), 
            'password2':forms.PasswordInput(attrs={'class': 'form-control'})
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已被注册，请使用其他邮箱")
        return email
                               
class ScoreForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(),
                                     initial=1,
                                     widget=forms.Select(attrs={'class': 'form-control'}),label='学生姓名')
    student_id = forms.IntegerField()
    score = forms.IntegerField(label='Score', initial=80,required=False,widget=forms.NumberInput())
    add_score = forms.IntegerField(label='add_Score', initial=0,required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date =forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='日期时间选择器')

    class Meta:
        model = Score
        fields = ['student', 'student_id', 'score', 'add_score','date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'add_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateField(),
        }
        labels = {
            'student': Student.name,
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.student = self.cleaned_data['student']  # 将学生实例添加到模型实例中
        score = self.cleaned_data.get('score', 0)
        add_score = self.cleaned_data.get('add_score', 0)
        instance = super().save(commit=False)
        instance.score = score
        instance.add_score = add_score
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        # 从 kwargs 中获取 student_id，并将其作为初始值设置给 student 字段
        self.student = kwargs.pop('student', None)
        self.student_id = kwargs.pop('student_id', None)
        super(ScoreForm, self).__init__(*args, **kwargs)
        if self.student:
            self.fields['student'].initial = self.student
        
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        self.fields['score'].widget.attrs.update({'class': 'form-control'})
        self.fields['add_score'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})

        mutable_data = self.data.copy()  # 创建可修改的 data 字典副本
        mutable_data['student_id'] = self.student_id  # 设置 student_id 到副本中
        self.data = mutable_data  # 将副本赋值给表单的 data 字典

class FeedbackForm(forms.ModelForm):
    title = forms.CharField(label='标题', widget=forms.Textarea(attrs={'rows': 1,'class': 'form-control'}),max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='具体内容')
    is_bug = forms.CheckboxInput()
    class Meta:
        model = Feedback
        fields = ['title', 'content', 'is_bug']
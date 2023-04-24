from django import forms
from .models import Score, Student

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
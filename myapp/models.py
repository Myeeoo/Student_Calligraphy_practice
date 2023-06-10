from ipaddress import summarize_address_range
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime , timedelta

class Classes(models.Model):
    name = models.CharField(max_length=20,default='NewDream')
    # 添加其他班级信息字段

    def __str__(self):
        return self.name
    
    @classmethod
    def create(cls, name):
        return cls.objects.create(name=name)

    def update(self, name):
        self.name = name
        self.save()

    @classmethod
    def delete_by_id(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    Classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    user = models.ManyToManyField(User,through='StudentUser')
    last_checkin_date = models.DateField(null=True, blank=True)
    consecutive = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def get_checkin_count(self):
        return Checkin.objects.filter(student=self).count()

    def get_total_score(self):
        return Score.objects.filter(student=self).aggregate(total_score=models.Sum('score'))['total_score'] or 0

    def get_total_checkin_score(self):
        return Checkin.objects.filter(student=self).aggregate(total_checkin_score=models.Sum('score'))['total_checkin_score'] or 0
    
    def get_total_checkin_score_this_week(self):
        today = datetime.now().date()
        yesterday = today-timedelta(days=1)
        # 本周的起始日期和结束日期
        this_week_start = today - timedelta(days=today.weekday())
        this_week_end = this_week_start + timedelta(days=6)

        Last_week_start = this_week_start-timedelta(days=7)
        Last_week_end = this_week_end-timedelta(days=7)
        return Checkin.objects.filter(student=self).filter(checkin_date__range=[this_week_start, this_week_end]).aggregate(total_checkin_score=models.Sum('score'))['total_checkin_score'] or 0
    
    def get_total_checkin_score_this_month(self):
        today = datetime.now().date()
        this_month_start = today.replace(day=1)
        next_month_start = this_month_start.replace(month=this_month_start.month + 1) if this_month_start.month < 12 else this_month_start.replace(year=this_month_start.year + 1, month=1)

        return Checkin.objects.filter(student=self).filter(checkin_date__range=[this_month_start, next_month_start - timedelta(days=1)]).aggregate(total_checkin_score=models.Sum('score'))['total_checkin_score'] or 0

    def get_last_checkin_date(self):
        last_checkin = Checkin.objects.filter(student=self).order_by('-checkin_date').first()
        return last_checkin.checkin_date if last_checkin else '暂无打卡记录'
    
    def get_highest_consecutive_checkins(self):
        consecutive_checkins = Checkin.objects.filter(student=self).order_by('-consecutive_checkins').first()
        if consecutive_checkins:
            
            return consecutive_checkins.consecutive_checkins
        else:
            return 0
        
    def get_likes_count(self):
        likes_count = Like.objects.filter(checkin__student=self).count()
        return likes_count
    
    def get_Top_Num(self):
        top_students = Student.objects.exclude(Classes__id=2).annotate(total_score=models.Sum('checkin__score')).order_by('-total_score')
    
        # 获取当前学生的排名
        try:
            rank = list(top_students).index(self) + 1
        except ValueError:
            rank = '不参与排名'
        return rank

class StudentUser(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    add_score = models.IntegerField(default=0,null=True)  # 添加一个新的字段
    date = models.DateField()

    def __str__(self):
        return f"Score: {self.student.name} - {self.score} ({self.date})"

class Checkin(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    checkin_date = models.DateTimeField(auto_now_add=True)
    checkin_text = models.CharField(max_length=200)
    checkin_image = models.ImageField(upload_to='checkin_images', blank=True, null=True)
    score = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, through='Like')
    consecutive_checkins = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.name} - {self.checkin_date}"
    def get_likes_count(self):
        return self.likes.count()
    def get_likes_list(self):
        return self.likes 
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkin = models.ForeignKey(Checkin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like: {self.user.username} - {self.checkin}"

class CommitLog(models.Model):
    author = models.CharField(max_length=100)
    date = models.DateTimeField()
    message = models.TextField()

class Feedback(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    submit_time = models.DateTimeField(auto_now_add=True)
    is_bug = models.BooleanField(default=False)

    def __str__(self):
        return self.title
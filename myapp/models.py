from django.db import models
from django.contrib.auth.models import User


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
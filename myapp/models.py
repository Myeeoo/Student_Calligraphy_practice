from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)
    user = models.ManyToManyField(User,through='StudentUser')
    last_checkin_date = models.DateField(null=True, blank=True)
    
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
    checkin_date = models.DateField(auto_now_add=True)
    checkin_text = models.CharField(max_length=200)
    checkin_image = models.ImageField(upload_to='checkin_images', blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.checkin_date}"
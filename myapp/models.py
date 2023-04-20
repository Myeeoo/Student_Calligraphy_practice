from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    add_score = models.IntegerField(default=0,null=True)  # 添加一个新的字段
    date = models.DateField()

    def __str__(self):
        return f"Score: {self.student.name} - {self.score} ({self.date})"

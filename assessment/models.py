
from django.db import models

from courses.models import Course
from users.models import CustomUser

# Create your models here.


class Assessment(models.Model):

    TYPE = (
        ('mcq', 'MCQ'),
        ('short answer', 'Short Answer'),
        ('essay', 'Essay'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # duration = models.CharField(max_length = 100)
    duration = models.DurationField()
    type = models.CharField(max_length=100,
                            choices=TYPE, default='mcq')

    def __str__(self):
        return self.title


class Question(models.Model):

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option


class Answer(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=True)


class Rating(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.user} rated {self.rating} star for {self.assessment}'

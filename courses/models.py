

from django.db import models

from users.models import CustomUser


class Course(models.Model):

    DURATION = (
        ('1 year', '1 year'),
        ('6 months', '6 months'),
        ('3 months', '3 months'),
    )

    TYPE = (
        ('online', 'Online'),
        ('blended', 'Blended'),
        ('offline', 'Offline'),
    )

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='course')
    duration = models.CharField(max_length=100,
                                choices=DURATION, default='3 months')
    fees = models.IntegerField()
    type = models.CharField(max_length=100,
                            choices=TYPE, default='offline')
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Lecture(models.Model):

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    duration = models.CharField(max_length=100)
    lecture = models.FileField(upload_to='lectures/')

    def __str__(self):
        return self.title


class Pdf(models.Model):

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    page = models.IntegerField()
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.title


class EmbedLecture(models.Model):

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title


class Document(models.Model):

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title

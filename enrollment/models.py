

from django.core import validators
from django.db import models

from courses.models import Course
from users.models import CustomUser


class EnrolledCourse(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    course = models.ForeignKey(to=Course,
                               on_delete=models.PROTECT)

    amount = models.IntegerField()
    session_id = models.CharField(max_length=200)

    paid = models.BooleanField(default=False,
                               verbose_name='Payment Status')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.name

from django.contrib import admin

from assessment.models import Answer, Assessment, Choice, Question, Rating

# Register your models here.

admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Rating)

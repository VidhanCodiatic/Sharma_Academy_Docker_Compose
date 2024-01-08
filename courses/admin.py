

from django.contrib import admin

from courses.forms import (CourseForm, DocumentForm, EmbedLectureForm,
                           LectureForm, PdfForm)
from courses.models import Course, Document, EmbedLecture, Lecture, Pdf

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    form = CourseForm


admin.site.register(Course, CourseAdmin)


class LectureAdmin(admin.ModelAdmin):
    form = LectureForm


admin.site.register(Lecture, LectureAdmin)


class PdfAdmin(admin.ModelAdmin):
    form = PdfForm


admin.site.register(Pdf, PdfAdmin)


class EmbedAdmin(admin.ModelAdmin):
    form = EmbedLectureForm


admin.site.register(EmbedLecture, EmbedAdmin)


class DoxAdmin(admin.ModelAdmin):
    form = DocumentForm


admin.site.register(Document, DoxAdmin)

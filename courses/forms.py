from django import forms

from courses.models import Course, Document, EmbedLecture, Lecture, Pdf
from users.models import CustomUser


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = CustomUser.objects.filter(
            type='instructor')


class LectureForm(forms.ModelForm):

    class Meta:
        model = Lecture
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = CustomUser.objects.filter(
            type='instructor')


class PdfForm(forms.ModelForm):

    class Meta:
        model = Pdf
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PdfForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = CustomUser.objects.filter(
            type='instructor')


class EmbedLectureForm(forms.ModelForm):

    class Meta:
        model = EmbedLecture
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmbedLectureForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = CustomUser.objects.filter(
            type='instructor')


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = CustomUser.objects.filter(
            type='instructor')

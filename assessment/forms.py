
from django import forms

from assessment.models import Answer, Assessment, Choice, Question, Rating


class AssessmentForm(forms.ModelForm):

    class Meta:
        model = Assessment
        fields = '__all__'
        # widgets = {
        #     'duration' : forms.TextInput(attrs={'class':'durationInputWidget'})
        # }


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = '__all__'


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = '__all__'


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        # fields = ['content']
        fields = '__all__'
        widgets = {
            'question': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'rating': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(AnswerForm, self).__init__(*args, **kwargs)
    #     if user:
    #         self.fields['user'].initial = user

    # def __init__(self, *args, **kwargs):
    #     super(AnswerForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].queryset = CustomUser.objects.filter(type = 'instructor')


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = '__all__'

        widgets = {
            'user': forms.HiddenInput(),
            'assessment': forms.HiddenInput(),
            'rating': forms.HiddenInput(),
        }

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from assessment.forms import (AnswerForm, AssessmentForm, ChoiceForm,
                              QuestionForm, RatingForm)
from assessment.models import (Answer, Assessment, Choice, Course, Question,
                               Rating)
# from assessment.utils import send_email_with_marks
from assessment.tasks import send_email_with_marks


class ShowAssessmentView(View):

    " Showing all assessment present in project "

    template_name = 'assessment/assessment.html'

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            q = request.GET['q']
            assessment = Assessment.objects.filter(title__icontains=q)
        else:
            assessment = Assessment.objects.all()
        assessment = assessment.annotate(
            avg_rating=Avg('rating__rating', default=0))
        assessment_per_page = 5
        paginator = Paginator(assessment, assessment_per_page, orphans=2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'assessment': assessment,
                                                    'page_obj': page_obj})


class AddAssessmentView(View):

    " Define assessment type and course "

    form_class = AssessmentForm
    template_name = 'assessment/addassessment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Assessment added successfully'})
            else:
                print(form.errors)
                return JsonResponse({'message': 'Assessment added failed'})
        else:
            return JsonResponse({'message': 'user is not instructor'})


class AddQuestionView(View):

    " Adding questions for assessment "

    form_class = QuestionForm
    template_name = "assessment/addQuestion.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            if form.is_valid():
                form.save()
                messages.error(request, 'Question added successfully.')
                return HttpResponseRedirect(reverse('add-question'))
            else:
                messages.error(request, 'Question add failed.')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User is not instructor.')
            return HttpResponseRedirect(reverse('index'))


class AddChoiceView(View):

    " Adding questions for assessment "

    form_class = ChoiceForm
    template_name = "assessment/addChoice.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            if form.is_valid():
                form.save()
                messages.success(request, 'Choice added successfully.')
                return HttpResponseRedirect(reverse('add-choice'))
            else:
                messages.success(request, 'Choice add Failed.')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User is not instructor.')
            return HttpResponseRedirect(reverse('index'))


class ShowQuizView(View):

    " Showing quiz according to user request "

    def get(self, request, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=self.kwargs['pk'])
            if assessment.type == 'mcq':
                questions = assessment.question_set.all()
                return render(request, 'assessment/quiz.html', {'questions': questions,
                                                                'assessment': assessment, })
            else:
                questions = assessment.question_set.all()
                count = questions.count()
                user = request.user.id
                AnswerFormSet = modelformset_factory(
                    Answer, form=AnswerForm, extra=count)
                # AnswerFormSet.form = staticmethod(curry(AnswerForm, user=request.user.id))
                formset = AnswerFormSet(queryset=Answer.objects.none())
                return render(request, 'assessment/showquiz.html', {'questions': questions,
                                                                    'formset': formset,
                                                                    'user': user,
                                                                    'assessment': assessment, })
        except Exception as e:
            messages.success(
                request, e)
            return HttpResponseRedirect(reverse("show-assessment"))

    def post(self, request, *args, **kwargs):
        assessment = Assessment.objects.get(id=self.kwargs['pk'])
        if assessment.type == 'mcq':
            if assessment.id in request.session:
                messages.success(request, 'Assessment already submitted.')
                return HttpResponseRedirect(reverse("show-assessment"))
            score = 0
            for q in Question.objects.all():
                select_option_id = request.POST.get(f'q_{q.id}')
                if select_option_id:
                    select_option = Choice.objects.get(pk=select_option_id)
                    if select_option.correct:
                        score += 1
            request.session['assessment.id'] = True
            form = RatingForm
            # send_email_with_marks(request, score)
            email = request.user.email
            send_email_with_marks.apply_async(args=[email, score])
            messages.success(
                request, 'Answer submmited successfully. Check your email for score.')
            return render(request, 'assessment/score.html', {'score': score, 'form': form,
                                                             'assessment': assessment})
        else:
            questions = assessment.question_set.all()
            count = questions.count()
            AnswerFormSet = modelformset_factory(
                Answer, form=AnswerForm, extra=count)
            # AnswerFormSet.form = staticmethod(curry(AnswerForm, user=request.user.id))
            formset = AnswerFormSet(
                request.POST, queryset=Answer.objects.none())
            if formset.is_valid():
                if 'assessment_submitted' in request.session:
                    messages.success(request, 'Assessment already submitted.')
                    return HttpResponseRedirect(reverse("show-assessment"))
                request.session['assessment_submitted'] = True
                formset.save()
                form = RatingForm
                messages.success(request, 'Assessment submited successfully.')
                return render(request, 'assessment/score.html', {'form': form,
                                                                 'assessment': assessment})
            messages.success(request, 'Assessment submit failed.')
            return HttpResponseRedirect(reverse("show-assessment"))


def rating_quiz(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rating submmited successfully.')
            return HttpResponseRedirect(reverse("show-assessment"))
        else:
            messages.error(request, 'Assessment Rating Failed.')
            return HttpResponseRedirect(reverse("show-assessment"))


class QuestionListView(ListView):
    model = Question
    template_name = "assessment/question.html"

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = '/assessment/show-question/'
    template_name = "assessment/question_confirm_delete.html"


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question']
    success_url = '/assessment/show-question/'
    template_name = "assessment/question_confirm_update.html"



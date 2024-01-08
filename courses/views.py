

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views import View

from courses.forms import DocumentForm, EmbedLectureForm, LectureForm, PdfForm
from courses.models import Course, Document, EmbedLecture, Lecture, Pdf
from Sharma_Academy import settings


class LectureView(View):

    """ Lecture create for courses """

    form_class = LectureForm
    template_name = "courses/addLecture.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            form = LectureForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Lecture added successfully.')
                return HttpResponseRedirect(reverse('addlecture'))
            else:
                messages.error(request, 'Lecture added failed.')
                return HttpResponseRedirect(reverse('addlecture'))
        else:
            messages.error(request, 'User is not instructor.')
            return HttpResponseRedirect(reverse('index'))


class EmbedLectureView(View):

    """ EmbedLecture create for courses """

    form_class = EmbedLectureForm
    template_name = "courses/addEmbedLecture.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            form = EmbedLectureForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Embed Lecture added successfully.')
                return HttpResponseRedirect(reverse('addembed'))
            else:
                messages.error(request, 'Embed Lecture added failed.')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User is not instuctor.')
            return HttpResponseRedirect(reverse('index'))


class DocumentView(View):

    """ Documentation create for courses """

    form_class = DocumentForm
    template_name = "courses/addDocument.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Document url added successfully.')
                return HttpResponseRedirect(reverse('adddox'))
            else:
                messages.error(request, 'Document url added failed.')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User is not instructor.')
            return HttpResponseRedirect(reverse('index'))


class PdfView(View):

    """ Pdf create for courses """

    form_class = PdfForm
    template_name = "courses/addPdf.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        user = request.user

        if user.type == 'instructor':
            form = PdfForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Pdf added successfully.')
                return HttpResponseRedirect(reverse('addpdf'))
            else:
                messages.success(request, 'Pdf added failed.')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User is not instructor.')
            return HttpResponseRedirect(reverse('index'))


class ShowLectureView(View):
    template_name = "courses/showLectures.html"

    def get(self, request, *args, **kwargs):
        videoLecture = Lecture.objects.all()
        video_per_page = 2
        paginator = Paginator(videoLecture, video_per_page)
        video_page_number = request.GET.get("page")
        video_page_obj = paginator.get_page(video_page_number)
        embedLecture = EmbedLecture.objects.all()
        document = Document.objects.all()
        files = Pdf.objects.all()
        return render(request, self.template_name, {'videoLecture': videoLecture,
                                                    'embedLecture': embedLecture,
                                                    'document': document,
                                                    'video_page_obj': video_page_obj,
                                                    'files': files})


class ShowCourseView(View):
    template_name = "courses/showCourses.html"

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs['pk'])
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, self.template_name, {'course': course,
                                                    'stripe_publishable_key': stripe_publishable_key})

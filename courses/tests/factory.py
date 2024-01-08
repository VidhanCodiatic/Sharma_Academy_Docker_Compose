
import factory
from faker import Factory

from courses.models import Course, Document, EmbedLecture, Lecture, Pdf
from users.tests.factory_user import UserFactory

faker = Factory.create()


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    instructor = factory.SubFactory(UserFactory)
    name = faker.text(10)
    image = factory.django.ImageField(filename='test_image.jpg')
    duration = '3 months'
    fees = faker.random_number(5)
    type = 'online'
    description = faker.text(15)


class LectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lecture

    instructor = factory.SubFactory(UserFactory) # Assuming CustomUserFactory exists
    course = factory.SubFactory(CourseFactory)  # Assuming CourseFactory exists
    title = faker.text(5)
    duration = faker.random_number(3)
    lecture = factory.django.FileField(filename='test_lecture.mp4', data=b'')  # Replace 'test_lecture.mp4' with your test file name


class PdfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pdf

    instructor = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    title = faker.text(5)
    page = faker.random_number(3)
    file = factory.django.FileField(filename='test_lecture.dox')


class EmbedLectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmbedLecture

    instructor = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    title = faker.text(5)
    url = faker.url()


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    instructor = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    title = faker.text(5)
    url = faker.url()
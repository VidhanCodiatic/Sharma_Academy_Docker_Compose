from django.test import TestCase
from django.urls import reverse
from faker import Factory

from courses.tests.factory import CourseFactory, EmbedLectureFactory
from courses.views import EmbedLectureView
from users.tests.factory_user import UserFactory

faker = Factory.create()

class EmbedLectureViewTestCase(TestCase):

    def test_create_embedlecture(self):
        instructor = UserFactory()
        course = CourseFactory(instructor=instructor)
        self.assertIsNotNone(course)
        embedlecture = EmbedLectureFactory(instructor=instructor, course=course)
        self.assertIsNotNone(embedlecture)

    def test_create_embedlecture_fail(self):

        test_password = faker.password()
        non_instructor = UserFactory(password=test_password, type='student')
        self.client.login(email=non_instructor.email, password=test_password)

        response = self.client.post(reverse('addembed'), data={})

        self.assertRedirects(response, reverse('index'))
import factory
from django.test import TestCase
from django.urls import reverse
from faker import Factory

from courses.tests.factory import CourseFactory, LectureFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()


class LectureViewTestCase(TestCase):

    def test_create_lecture(self):
        
        instructor = UserFactory()
        course = CourseFactory(instructor=instructor)
        self.assertIsNotNone(course)
        lecture = LectureFactory(instructor=instructor, course=course)
        self.assertIsNotNone(lecture)

    def test_create_lecture_fail(self):

        test_password = faker.password()
        non_instructor = UserFactory(password=test_password, type='student')
        self.client.login(email=non_instructor.email, password=test_password)

        response = self.client.post(reverse('addlecture'), data={})

        self.assertRedirects(response, reverse('index'))
        

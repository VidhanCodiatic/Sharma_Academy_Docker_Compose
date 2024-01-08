from django.test import TestCase
from django.urls import reverse
from faker import Factory

from courses.tests.factory import CourseFactory, DocumentFactory
from courses.views import DocumentView
from users.tests.factory_user import UserFactory

faker = Factory.create()

class DocumentViewTestCase(TestCase):

    def test_create_document(self):
        instructor = UserFactory()
        course = CourseFactory(instructor=instructor)
        self.assertIsNotNone(course)
        document = DocumentFactory(instructor=instructor, course=course)
        self.assertIsNotNone(document)

    def test_create_document_fail(self):

        test_password = faker.password()
        non_instructor = UserFactory(password=test_password, type='student')
        self.client.login(email=non_instructor.email, password=test_password)

        response = self.client.post(reverse('adddox'), data={})

        self.assertRedirects(response, reverse('index'))
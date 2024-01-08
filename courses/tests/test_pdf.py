

from django.test import TestCase
from django.urls import reverse
from faker import Factory

from courses.tests.factory import CourseFactory, PdfFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()

class PdfViewTestCase(TestCase):

    def test_create_embedlecture(self):
        instructor = UserFactory()
        course = CourseFactory(instructor=instructor)
        self.assertIsNotNone(course)
        pdf = PdfFactory(instructor=instructor, course=course)
        self.assertIsNotNone(pdf)

    def test_create_pdf_fail(self):

        test_password = faker.password()
        non_instructor = UserFactory(password=test_password, type='student')
        self.client.login(email=non_instructor.email, password=test_password)

        response = self.client.post(reverse('addpdf'), data={})

        self.assertRedirects(response, reverse('index'))
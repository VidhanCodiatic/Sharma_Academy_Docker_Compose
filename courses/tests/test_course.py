from django.test import TestCase
from faker import Factory

from courses.tests.factory import CourseFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()

class CourseTestCase(TestCase):

    def test_create_course(self):

        course = CourseFactory()
        self.assertIsNotNone(course)
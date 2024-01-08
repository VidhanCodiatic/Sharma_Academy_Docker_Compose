from django.test import TestCase
from faker import Factory

from assessment.tests.factory import (AnswerFactory, AssessmentFactory,
                                      QuestionFactory)
from courses.tests.factory import CourseFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()


class AnswerViewTestCase(TestCase):

    def test_create_answer(self):
        email = faker.email()
        phone = faker.random_number(10)
        user = UserFactory(email=email, phone=phone)
        course = CourseFactory()
        assessment = AssessmentFactory(course=course)
        question = QuestionFactory(assessment=assessment)
        answer = AnswerFactory(user=user, question=question)
        self.assertIsNotNone(answer)

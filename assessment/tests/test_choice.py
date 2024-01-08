from django.test import TestCase
from django.urls import reverse
from faker import Factory

from assessment.tests.factory import ChoiceFactory, QuestionFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()


class ChoiceViewTestCase(TestCase):

    def test_create_assessment(self):
        question = QuestionFactory()
        choice = ChoiceFactory(question=question)
        self.assertIsNotNone(choice)

    def test_create_choice_fail(self):

        test_password = faker.password()
        non_instructor = UserFactory(password=test_password, type='student')
        self.client.login(email=non_instructor.email, password=test_password)

        response = self.client.post(reverse('add-choice'), data={})

        self.assertRedirects(response, reverse('index'))
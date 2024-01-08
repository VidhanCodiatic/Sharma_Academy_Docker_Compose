
import factory
from faker import Factory

from assessment.models import Answer, Assessment, Choice, Question
from courses.tests.factory import CourseFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()


class AssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assessment

    course = factory.SubFactory(CourseFactory)
    title = faker.text(10)
    duration = '01:02'
    type = 'mcq'

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    assessment = factory.SubFactory(AssessmentFactory)
    question = faker.words(10)

class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    option = faker.words(5)
    correct = False

class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    user = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)
    content = faker.text(15)
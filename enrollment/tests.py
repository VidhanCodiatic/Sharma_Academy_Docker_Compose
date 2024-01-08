from django.test import Client, SimpleTestCase, TestCase
from django.urls import resolve, reverse

from enrollment.views import (PaymentFailedView, PaymentSuccessView,
                              create_checkout_session, stripe_webhook)

# Create your tests here.

class EnrollmentViewTest(TestCase):
    """Test case for the Course Purchase view."""

    

# class TestUrls(SimpleTestCase):

#     def test_success_url_is_resolved(self):
#         url = reverse('success')
#         self.assertEquals(resolve(url).func.view_class, PaymentSuccessView)

#     def test_failed_url_is_resolved(self):
#         url = reverse('failed')
#         self.assertEquals(resolve(url).func.view_class, PaymentFailedView)

#     def test_checkout_url_is_resolved(self):
#         url = reverse('api_checkout_session', args = ['1'])
#         self.assertEquals(resolve(url).func, create_checkout_session)

#     def test_webhook_url_is_resolved(self):
#         url = reverse('webhook')
#         self.assertEquals(resolve(url).func, stripe_webhook)
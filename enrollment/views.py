

import json

import stripe
from django.conf import settings
from django.http.response import (HttpResponse, HttpResponseNotFound,
                                  JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView

from courses.models import Course
from enrollment.models import EnrolledCourse
from Sharma_Academy import settings as paymentSetting


@csrf_exempt
def create_checkout_session(request, id):
    """ Checkout session for stripe payment """

    request_data = json.loads(request.body)
    course = get_object_or_404(Course, pk=id)

    stripe.api_key = paymentSetting.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': course.name,
                    },
                    'unit_amount': int(course.fees*100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )
    enroll = EnrolledCourse()
    enroll.customer_email = request_data['email']
    enroll.user = request.user
    enroll.course = course
    enroll.session_id = checkout_session['id']
    enroll.amount = int(course.fees)
    enroll.save()

    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):

    """ Payment Success for stripe payment """

    template_name = "enrollment/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(EnrolledCourse, session_id=session_id)
        order.paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):

    """ Payment Failed for stripe payment """

    template_name = "payments/payment_failed.html"


@csrf_exempt
def stripe_webhook(request):
    """ Connect webhook with stripe payment """

    stripe.api_key = paymentSetting.STRIPE_SECRET_KEY
    endpoint_secret = paymentSetting.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


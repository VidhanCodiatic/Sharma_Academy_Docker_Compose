

from django.urls import path

from enrollment.views import (PaymentFailedView, PaymentSuccessView,
                              create_checkout_session, stripe_webhook)

urlpatterns = [
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    # path('history/', OrderHistoryListView.as_view(), name='history'),
    path('api/checkout-session/<id>/', create_checkout_session,
         name='api_checkout_session'),
    path('webhook/', stripe_webhook, name='webhook'),

    # ./stripe listen --forward-to localhost:8000/enrollment/webhook/
]

from celery import shared_task
from time import sleep
# from django_celery_beat.models import PeriodicTask, IntervalSchedule

from django.template.loader import render_to_string
from users.tokens import email_verification_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from users.models import CustomUser
from celery.exceptions import MaxRetriesExceededError
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name='register_email', serializer='json', max_retries=3)
def register_email(email, domain):
    try:
        user = CustomUser.objects.get(email=email)
        subject = 'Activate Your Account'
        html_content = render_to_string(
            'users/email_verification.html',
            {
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            }
        )
        plain_text = strip_tags(html_content)
        message = EmailMultiAlternatives(
            to=[email], subject=subject, body=plain_text)
        message.content_subtype = "html"
        message.send()
        logger.info("Email sent successfully")
        return "Email sent successfully"
    except Exception as e:
        # Log the error
        logger.error(f"Error sending email: {e}")
        # Retry the task (up to 3 times)
        try:
            raise register_email.retry(exc=e)
        except MaxRetriesExceededError:
            # Max retries exceeded, log and return an error message
            logger.error("Max retries exceeded for sending email.")
            return "Error sending email. Please try again later."
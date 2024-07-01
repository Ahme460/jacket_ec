from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome!',
        'Thank you for signing up!',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )

#celery -A project worker --loglevel=info
#celery -A project beat --loglevel=info





@shared_task
def send_reset_password_email(user_email):
    try:
        user = User.objects.get(email=user_email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f'http://your-domain.com/reset-password/{uid}/{token}/'

        send_mail(
            'Password Reset',
            f'Click the link below to reset your password:\n{reset_link}',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass




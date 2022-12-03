from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.sites.models import Site


from django.template.loader import render_to_string

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    print(f"post save signal {instance.email}")
    if created:
        print(f"sending email to {instance.email}")
        if not instance.is_email_verified:
            token = Token.objects.get_or_create(user=instance)
            current_site = Site.objects.get_current()
            verify_route ="http://localhost:8000/" + reverse('email_verification')
            verification_message =f"Please visit the following link to verify your email in E-Shop \n{verify_route}?token={token[0].key}"
            send_mail(
                "E-Shop: Verify Email Address",
                message=verification_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],)
        

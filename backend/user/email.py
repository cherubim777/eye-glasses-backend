from django.core.mail import send_mail
from django.conf import settings


def sendMail(email, code):
    subject = "this email is sent to you based on your request to reset your password"
    message = f"enter this code to reset you pasword {code}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

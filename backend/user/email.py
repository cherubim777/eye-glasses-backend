import smtplib
from django.core.mail import send_mail
from django.conf import settings


def sendMail(email, code):
    subject = "this email is sent to you based on your request to reset your password"
    message = f"enter the code {code} to reset you pasword"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_activation_email(user_email):
    subject = "Your account has been activated"
    message = "Dear user,\n\nYour account has been activated. You can now log in to our website and start using our services.\n\nBest regards,\nThe Website Team"
    email_from = "noreply@example.com"
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

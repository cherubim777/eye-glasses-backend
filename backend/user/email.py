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


# import ssl
# from smtplib import SMTPException
# from django.core.exceptions import ValidationError


# def sendMail(email, code):
#     # your existing code
#     subject = "this email is sent to you based on your request to reset your password"
#     message = f"enter the code {code} to reset you pasword"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     EMAIL_HOST_USER = settings.EMAIL_HOST_USER
#     EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
#     EMAIL_HOST = settings.EMAIL_HOST
#     EMAIL_PORT = settings.EMAIL_PORT

#     try:
#         context = ssl.create_default_context()
#         context.check_hostname = False
#         context.verify_mode = ssl.CERT_NONE
#         print(ssl.get_default_verify_paths())
#         with smtplib.SMTP_SSL(
#             EMAIL_HOST, EMAIL_PORT, context=ssl.create_default_context()
#         ) as server:
#             server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#             server.sendmail(email_from, recipient_list, message)
#         return True
#     except SMTPException as e:
#         # Handle SMTP errors
#         print(e)
#         raise ValidationError("Failed to send email")
#     except ssl.SSLError as e:
#         # Handle SSL errors
#         print(e)
#         raise ValidationError("SSL error")

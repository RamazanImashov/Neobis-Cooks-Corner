from config.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_code(username, email, activation_code):
    context = {
        "text_detail": "Thank for registration",
        "username": username,
        "email": email,
        "domain": "http://34.72.24.139",
        "activation_code": activation_code,
    }
    message_html = render_to_string("email_url.html", context)
    message = strip_tags(message_html)
    send_mail(
        "Activation account",
        message,
        "admin@gmail.com",
        [email],
        html_message=message_html,
        fail_silently=False,
    )


@app.task
def send_activation_code_celery(username, email, activation_code):
    send_activation_code(username, email, activation_code)


def send_password(username, email, activation_code):
    context = {
        "text_detail": "Password recovery",
        "username": username,
        "email": email,
        "forgot_password_code": activation_code,
    }
    message_html = render_to_string("lose_password.html", context)
    message = strip_tags(message_html)
    send_mail(
        "Password recovery",
        message,
        "admin@gmail.com",
        [email],
        html_message=message_html,
        fail_silently=False,
    )


@app.task
def send_password_celery(username, email, activation_code):
    send_password(username, email, activation_code)

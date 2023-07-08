from website import mail
from flask_mail import Message


def send_password_reset_mail(email: str, reset_link: str):
    subject = "Reset Password"
    body = f"Click the following link to reset your password: {reset_link}"
    recipients = [email]

    message = Message(subject=subject, body=body, recipients=recipients)
    mail.send(message)

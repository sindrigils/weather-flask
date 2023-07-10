from website import mail, app
from flask_mail import Message


def send_password_reset_mail(email: str, reset_link: str):
    """
    Sends a password reset email to the specified email address.

    Args:
        email: A string representing the recipient's email address.
        reset_link: A string representing the password reset link to be included in the email.

    This function composes and sends an email to the specified email address for the purpose
    of password reset. The email contains a subject, body, and recipient. The subject is set
    to "Reset Password", and the body includes the provided reset link. The email is sent
    using the configured mail server.

    """
    subject = "Reset Password"
    body = f"Click the following link to reset your password: {reset_link}"
    recipients = [email]

    message = Message(subject=subject, body=body, recipients=recipients)
    mail.send(message)


def send_email_to_website(text: str):
    """
    Sends an email to the website with the provided text.

    Args:
        text (str): The content of the email message.
    """

    subject = "Message from contact page"
    body = text
    recipients = [app.config["MAIL_USERNAME"]]

    message = Message(subject=subject, body=body, recipients=recipients)
    mail.send(message)

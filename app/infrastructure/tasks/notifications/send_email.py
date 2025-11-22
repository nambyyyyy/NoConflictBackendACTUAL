from celery import shared_task
from settings import vars
from typing import Optional
from urllib.parse import urljoin
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from uuid import UUID



def send_mail(
    subject: str,
    message: str,
    recipient_list: list[str],
    fail_silently: bool = False,
):

    msg = MIMEMultipart()
    msg["From"] = vars.MAIL_FROM
    msg["To"] = ", ".join(recipient_list)
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(vars.MAIL_SERVER, vars.MAIL_PORT) as server:
            server.starttls()
            server.login(vars.MAIL_USERNAME, vars.MAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        if not fail_silently:
            raise e


    
@shared_task(
    name="send_verification_email",
)
def send_verification_email(
    user_id: str,
    user_email: str,
    token: str,
    base_url: Optional[str] = None,
) -> None:
    
    try:
        UUID(user_id)
    except ValueError as e:
        raise e

    uidb64 = base64.urlsafe_b64encode(user_id.encode()).decode()
    path = f"{vars.AUTH_PREFIX}/verify-email/{uidb64}/{token}"
    base = base_url or vars.SITE_URL
    verify_url = urljoin(base, path)

    subject = "Подтверждение e‑mail"
    body = (
        "Здравствуйте!\n\n"
        f"Для подтверждения почты перейдите по ссылке:\n{verify_url}\n\n"
        "Если вы не регистрировались — игнорируйте это письмо."
    )

    send_mail(
        subject=subject,
        message=body,
        recipient_list=[user_email],
        fail_silently=False,
    )

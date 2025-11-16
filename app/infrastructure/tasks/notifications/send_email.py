from celery import shared_task
from infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from domain.entities.user import User
from infrastructure.database.sessions import get_db_session
from config import settings
from uuid import UUID
from typing import Optional
from urllib.parse import urljoin
import base64
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



async def send_mail(
    subject: str,
    message: str,
    recipient_list: list[str],
    from_email: str | None = None,
    fail_silently: bool = False,
):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join(recipient_list)
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            start_tls=settings.EMAIL_USE_TLS,
        )
    except Exception as e:
        if not fail_silently:
            raise e
        
        
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=30,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
async def send_verification_email(
    self,
    user_id: str,
    token: str,
    base_url: Optional[str] = None,
) -> None:
    user_repo = SQLAlchemyUserRepository(db_session=await get_db_session()) 
    user_entity: Optional[User] = await user_repo.get_by_id(UUID(user_id))

    if not user_entity or user_entity.email_confirmed:
        return

    uidb64 = base64.urlsafe_b64encode(str(user_entity.id).encode()).decode()
    path = f"/verify-email/{uidb64}/{token}"
    base = base_url or getattr(settings, "SITE_URL", "http://localhost:8000")
    verify_url = urljoin(base, path)

    subject = "Подтверждение e‑mail"
    body = (
        "Здравствуйте!\n\n"
        f"Для подтверждения почты перейдите по ссылке:\n{verify_url}\n\n"
        "Если вы не регистрировались — игнорируйте это письмо."
    )

    await send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_entity.email],
        fail_silently=False,
    )

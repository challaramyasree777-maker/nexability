
import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_otp_email(email: str, otp: str) -> None:
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        raise RuntimeError("Gmail SMTP configuration is missing")

    message = EmailMessage()

    message["From"] = f"NexAbility <{settings.SMTP_EMAIL}>"
    message["To"] = email
    message["Subject"] = "Your NexAbility verification code"

    message.set_content(
        f"Your NexAbility verification code is {otp}.\n"
        "This code expires in 5 minutes.\n"
        "If you did not request this code, ignore this email."
    )

    message.add_alternative(
        f"""
        <div>
            <h2>Verify your email</h2>
            <p>Your NexAbility verification code is:</p>
            <h1>{otp}</h1>
            <p>This code expires in 5 minutes.</p>
            <p>If you did not request this code, ignore this email.</p>
        </div>
        """,
        subtype="html",
    )

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD.replace(" ", ""),
        )
        server.send_message(message)

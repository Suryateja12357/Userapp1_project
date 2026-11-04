import smtplib
import ssl
from email.message import EmailMessage


def send_reset_otp(to_email:str,otp:str):
    smtp_email="steja432505@gmail.com"
    smtp_password="jwem jvkk xqdu zftn"
    message=EmailMessage()
    message["Subject"]="Password Reset OTP"
    message["From"]="SMTP_EMAIL"
    message["To"]=to_email

    message.set_content(f"Your password reset OTP is {otp}."
                        "It expires in 5 minutes")
    with smtplib.SMTP("smtp.gmail.com",587,timeout=30) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo
        server.login(smtp_email,smtp_password)
        server.send_message(message)
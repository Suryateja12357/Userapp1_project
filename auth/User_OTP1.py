import smtplib 
from email.message import EmailMessage

SMTP_EMAIL="steja432505@gmail.com"
SMTP_PASSWORD="ltgs ycnk crkk bkxk"

def send_otp_email(to_email:str,otp:str):
    message=EmailMessage()
    message["Subject"]="Your OTP Verification code"
    message["From"]=SMTP_EMAIL
    message["To"]=to_email

    message.set_content(
        f"your otp is {otp}.\n"
        "This OTP is valid for 5 minutes.\n"
        "Please do not share it anyone."
    )
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(SMTP_EMAIL,SMTP_PASSWORD)
        server.send_message(message)
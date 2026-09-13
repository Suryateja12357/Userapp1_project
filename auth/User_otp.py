import random
import smtplib
from fastapi.templating import Jinja2Templates
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

templates=Jinja2Templates(directory="templates")

SENDER_EMAIL="steja432505@gmail.com"
APP_PASSWORD="idtx mdms moum qolg"

def generate_otp():
    return(random.randint(100000,999999))

def send_otp_email(receiver_email:str,otp:int):
    template=templates.get_template("otp.html")
    body=template.render(name="name",otp=otp)
    message=MIMEMultipart()
    message["From"]="steja432505@gmail.com"
    message["To"]="alice@gmail.com"
    message["Subject"]="Password reset OTP"
    message.attach(MIMEText(body,"html"))
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(SENDER_EMAIL,APP_PASSWORD)
        server.sendmail(SENDER_EMAIL,receiver_email,message.as_string())
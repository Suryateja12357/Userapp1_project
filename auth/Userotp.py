import random
import smtplib
from fastapi.templating import Jinja2Templates
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

templates=Jinja2Templates(directory="templates")

def generate_otp():
    return str(random)
def send_resend_otp(receiver_email:str,otp:str):

    SENDER_EMAIL="steja432505@gmail.com"
    app_password="zubx hccu ugyv yrji"

    template=templates.get_template("notification1.html")
    body=template.render(name="user.full_name",otp=otp)
    message=MIMEMultipart()
    message["From"]="steja432505@gmail.com"
    message["To"]="alice@gmail.com"
    message["Subject"]="Reset Password OTP"
    message.attach(MIMEText(body,"html"))
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(SENDER_EMAIL,app_password)
        server.sendmail(SENDER_EMAIL,receiver_email,message.as_string())
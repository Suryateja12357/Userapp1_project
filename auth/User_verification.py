import smtplib
from fastapi.templating import Jinja2Templates
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

templates=Jinja2Templates(directory="templates")

SENDER_EMAIL="steja432505@gmail.com"
SENDER_PASSWORD="ebpv fxeq poia ltpl"

def send_verification_email(receiver_email:str,token:str):
    verification_link=(
        f"http://127.0.0.1:8000/user/verify_email?token={token}"
    )
    template=templates.get_template("welcome.html")
    body=template.render(name="name",verification_link=verification_link)
    message=MIMEMultipart()
    message["From"]="steja432505@gmail.com"
    message["To"]="alice@gmail.com"
    message["Subject"]="Welcome to Our Application"
    message.attach(MIMEText(body,"html"))
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)
        server.sendmail(
            SENDER_EMAIL,
            receiver_email,
            message.as_string()
        )
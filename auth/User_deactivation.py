import smtplib
from fastapi.templating import Jinja2Templates
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

templates=Jinja2Templates(directory="templates")

SENDER_EMAIL="steja432505@gmail.com"
APP_PASSWORD="zwgm zjsj aiah jkhg"

def send_deactivate_email(receiver_email:str):
    template=templates.get_template("notification.html")
    body=template.render(name="name")
    message=MIMEMultipart()
    message["From"]="steja432505@gmail.com"
    message["To"]="alice@gmail.com"
    message="User deactivated"
    message.attach(MIMEText(body,"html"))
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(SENDER_EMAIL,APP_PASSWORD)
        server.sendmail(SENDER_EMAIL,receiver_email,message.as_string())
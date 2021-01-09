from email.mime import text
from email.mime.base import MIMEBase
import smtplib, ssl
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import os
from typing import final

# App password aafegkoygzcznzdw
def email_alert(subject, body, reciever_email):
    # get hidden username and password
    user = os.getenv("PERSONAL_EMAIL")
    pass_word = os.getenv("GMAIL_APP_PASS")

    # create email message
    msg = EmailMessage()
    msg.set_content(body)

    msg["from"] = user
    msg["to"] = reciever_email
    msg["subject"] = subject
    # connect to gmail server an send message
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user=user, password=pass_word)
    server.send_message(msg)
    server.quit()


def send_image_email(subject, image_filename, body, reciever_email):
    image_data = open(image_filename, "rb").read()

    port = 587
    # get hidden username and password
    sender_email = os.getenv("PERSONAL_EMAIL")
    sender_password = os.getenv("GMAIL_APP_PASS")

    # instantiate message object
    msg = MIMEMultipart()
    msg["to"] = reciever_email
    msg["from"] = sender_email
    msg["Subject"] = subject

    # attach text to msg object
    text = MIMEText("test")
    msg.attach(text)

    # attatch image to msg object
    image = MIMEImage(image_data, name=os.path.basename(image_filename))

    msg.attach(image)
    # connect to gmail server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        # try to send message
        server.starttls()
        server.ehlo()
        server.login(user=sender_email, password=sender_password)
        server.sendmail(sender_email, reciever_email, msg.as_string())
    except Exception as e:
        print(f"Something went wrong when connecting to server!\n{e}")
    finally:
        server.quit()


if __name__ == "__main__":
    target = os.getenv("PROFESSIONAL_EMAIL")
    sub = "test"
    body = "Hello you sexy beast"
    send_image_email(
        subject=sub, image_filename="intruder.jpg", body=body, reciever_email=target
    )

# from realpython.com tutorial
import smtplib
import ssl

message = """\
Subject: Note App Signup

Thank you for signing up!"""


def send_email(user):
    sender = "sltsapp20@gmail.com"
    password = "slts2020"

    port = 465

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, user, message)

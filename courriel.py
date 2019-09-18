
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import exists
import os



def message_courriel(destination, token, body, subject):
    source = os.environ.get('EMAIL')
    motpasse = os.environ.get('password')
    site = os.environ.get('site')
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source
    msg['To'] = destination
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP(os.environ.get('smtp'), os.environ.get('number'))
    server.starttls()
    server.login(source, motpasse)
    text = msg.as_string()
    server.sendmail(source, destination, text)
    server.quit()

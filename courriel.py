# coding: utf8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from os.path import exists
import os



def message_courriel(destination, token, body, subject):
    source = os.environ.get('EMAIL')
    motpasse = os.environ.get('password')
    print source
    print motpasse
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source
    msg['To'] = destination
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(source, motpasse)
    text = msg.as_string()
    server.sendmail(source, destination, text)
    server.quit()

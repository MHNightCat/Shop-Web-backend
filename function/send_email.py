import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

sender_email_address = os.getenv('email')
email_smtp = os.getenv("email_smtp")
email_password = os.getenv("email_password")

def send_email(title:str, address:str, content:str,):
    email_subject = title
    receiver_email_address = address
    
    # create an email message object
    message = EmailMessage()
    
    # configure email headers
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
    
    # set email body text
    message.add_alternative(content, subtype='html')
    # set smtp server and port
    server = smtplib.SMTP(email_smtp, '587')
    # identify this client to the SMTP server
    server.ehlo()
    # secure the SMTP connection
    server.starttls()
    
    # login to email account
    server.login(sender_email_address, email_password)
    # send email
    server.send_message(message)
    # close connection to server
    server.quit()
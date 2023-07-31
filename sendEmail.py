import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, content, password):
    # Extract email address from the content string
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    match = re.search(email_pattern, content)

    if not match:
        return "No email address detected in the content"

    user_email = match.group()
    message = content.replace(user_email, "")  # Remove email from the message

    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = password
    msg["From"] = "muthuiwilson37@gmail.com"
    msg["To"] = user_email
    msg["Subject"] = subject

    # add in the message body
    msg.attach(MIMEText(message, "plain"))

    # create server
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # starting the server instance
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg["From"], password)

    # send the message via the server
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

    return f"Email successfully sent to {user_email}"
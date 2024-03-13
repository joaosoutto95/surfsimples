import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EmailSender: 
    def __init__(self, sender, password, smtp_server='smtp-mail.outlook.com', port=587):
        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.port = port

    def send_email(self, subject, html, attachment_path=None, attachment_name=None):
        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = ", ".join(['thadeu@surfins.com.br'])
        message["Subject"] = subject
        
        message.attach(MIMEText(html, "html"))

        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEApplication(attachment.read(), _subtype='xlsx')
                part.add_header('Content-Disposition', 'attachment', filename=attachment_name)

                encoders.encode_base64(part)
                message.attach(part)
            
        context = ssl.create_default_context()
        with smtplib.SMTP(host=self.smtp_server, port=self.port) as server:
            server.starttls(context=context)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, ['thadeu@surfins.com.br'], message.as_string())
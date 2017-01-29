import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from email.mime.multipart import MIMEMultipart
from config import KINDLE_EMAIL,AMAZON_EMAIL,SMTP_HOST_NAME,SMTP_PORT,EMAIL_PASSWORD

def setup_email(SMTP_PORT=465):
    try:
        smtpObj = smtplib.SMTP_SSL(SMTP_HOST_NAME, SMTP_PORT)
        if smtpObj.ehlo()[0]==250:
            try:
                smtpObj.login(AMAZON_EMAIL, EMAIL_PASSWORD)
                return smtpObj
            except smtplib.SMTPAuthenticationError:
                #TODO Use sys.exit and logging
                return 'Check email/password'
    except:
        return 'Nodename nor servername not identified.'

def send_email(mobi_file):
    smtpObj = setup_email()
    msg = MIMEMultipart()
    msg['From'] = AMAZON_EMAIL
    msg['To'] = KINDLE_EMAIL
    # As suggested here https://www.amazon.com/gp/help/customer/display.html?nodeId=201974220
    msg['Subject'] = "Convert"
    body = ""
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(mobi_file, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % mobi_file)

    msg.attach(part)

    text = msg.as_string()
    smtpObj.sendmail(AMAZON_EMAIL, KINDLE_EMAIL, text)
    smtpObj.quit()

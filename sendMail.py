import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender_email = 'icodeinnovahostingservice@gmail.com'
sender_password = 'hnykgvqgyvorghrb'
receiver = 'i211.lbreports@gmail.com'

def send_mail_pdf(body , subject , pdfname):
    # put your email here
    # receiver = 'subath.abeysekara@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))


    # open the file in bynary
    binary_pdf = open(pdfname, 'rb')

    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    # payload = MIMEBase('application', 'pdf', Name=pdfname)
    payload.set_payload((binary_pdf).read())

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    # enable security
    session.starttls()

    # login with mail_id and password
    session.login(sender_email, sender_password)

    text = message.as_string()
    session.sendmail(sender_email, receiver, text)
    session.quit()
    return {
        "state": True,
        "message": 'mail sent'
    }

def send_mail():
    body = '''Get Your Report Here
        '''
    pdfname = 'GFG.pdf'
    subject = 'Lunchbucket Report'
    return send_mail_pdf(body, subject, pdfname)

def send_mail_bill():
    body = '''Get Your Document Here
    '''
    subject = 'Manufacture Bill Document'
    pdfname = "bill_document.pdf"
    return send_mail_pdf(body, subject, pdfname)

def send_ml_limits():
    body = '''Get Your Document Here
    '''
    subject = 'ML Predicted Limits Document'
    pdfname = "ml_limit_report.pdf"
    return send_mail_pdf(body, subject, pdfname)

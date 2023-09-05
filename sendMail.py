import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail():
    body = '''Get Your Report Here
    '''
    # put your email here
    sender_email = 'icodeinnovahostingservice@gmail.com'  # Replace with your email address
    sender_password = 'hnykgvqgyvorghrb'
    # put the email of the receiver here
    receiver = 'subath.abeysekara@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver
    message['Subject'] = 'Lunchbucket Report'

    message.attach(MIMEText(body, 'plain'))

    pdfname = 'GFG.pdf'

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
        "state":True,
        "message":'mail sent'
    }
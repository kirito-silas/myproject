import smtplib
from project.config import settings
from project.otp import routerotp

def sendemail(sender: str, otp: str):
    TO = sender  # 'silashk_trikhatri@srmus.edu.in'
    SUBJECT = 'TEST MAIL'
    TEXT = otp  # 'Here is a message from python.'

    # Gmail Sign In
    gmail_sender = 'silashkhatri@outlook.com'
    gmail_passwd = 'IT@03101998'

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo() #later added
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print('email sent')
    except:
        print('error sending mail')

    server.quit()

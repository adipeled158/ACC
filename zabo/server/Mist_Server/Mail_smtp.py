__author__ = 'Tomer zaboklitski'



def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        print "all good 1"
        server_ssl.ehlo() # optional, called by login()
        print "all good 2"
        server_ssl.login(gmail_user, gmail_pwd)
        print "all good"
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        return True
    except:
        print False
#send_email("Help.Mist1802","Tomerzabo1","shai120899@gmail.com","this is a test subject","ShaiGod")
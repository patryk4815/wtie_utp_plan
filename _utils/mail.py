import smtplib
import dns.resolver


def send_email(title, body, to_email, from_email, username=None, password=None):
    mx_hostname = to_email.split('@')[-1]
    answers = dns.resolver.query(mx_hostname, 'MX')
    if len(answers) <= 0:
        raise ConnectionResetError('Problem z pobraniem rekordu MX z dns')
    server = str(answers[0].exchange)

    sender = from_email
    receivers = [to_email]
    message = "From: {}\r\nSubject: {}\r\n\r\n{}".format(sender, title, body)

    server = smtplib.SMTP(server[:-1])
    try:
        server.set_debuglevel(True)
        server.ehlo()

        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()

        if username:
            server.login(username, password)

        server.sendmail(sender, receivers, message)
    finally:
        server.quit()

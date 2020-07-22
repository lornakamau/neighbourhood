from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_signup_email_admin(name,receiver):
    # Creating message subject and sender
    subject = 'Welcome to MyNeighbourhood'
    sender = 'lornadeveloper@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/email-admin.txt',{"name": name})
    html_content = render_to_string('email/email-admin.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


def send_signup_email_resident(name,username,password,admin,hood,receiver):
    # Creating message subject and sender
    subject = 'Welcome to MyNeighbourhood'
    sender = 'lornadeveloper@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/email-occupant.txt',{"name": name, "username":username, "password":password, "admin":admin, "hood":hood})
    html_content = render_to_string('email/email-occupant.html',{"name": name, "username":username, "password":password, "admin":admin, "hood":hood})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
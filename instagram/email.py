from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(name,receiver):
    #Creating message subject and sender
    subject = 'Welcome to the My-Insta Site'
    sender = 'ter.terfirst@gmail.com'

    #Passing in the context variables
    text_content = render_to_string('email/welcomemail.txt',{"name":name})
    html_content = render_to_string('email/welcomemail.html',{"name":name})


    msg = EmailMultiAlternatives(subject, sender, text_content,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
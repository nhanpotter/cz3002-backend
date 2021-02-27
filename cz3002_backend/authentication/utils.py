from django.core.mail import EmailMessage
from django.conf import settings
class Util:
    @staticmethod
    def send_email(data):
        #from_email = settings.EMAIL_DEFAULT_SENDER 
        email=EmailMessage(to=[data['to_email']],subject=data['subject'],body=data['body'])
        email.send()


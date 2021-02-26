from django.core.mail import EmailMessage
#import settings
class Util:
    @staticmethod
    def send_email(data):
        #from_email = settings.EMAIL_HOST_USER
        email=EmailMessage(to=[data['to_email']],subject=data['subject'],body=data['body'])
        email.send()


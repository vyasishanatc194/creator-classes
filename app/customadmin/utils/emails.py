from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

class Emails:
    subject = ""
    message = ""
    from_email = ""
    recipient_list = ""
    html_message = ""
    base_emails_html_path = "core/emails/html/"
    base_emails_text_path = "core/emails/text/"


    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
         
        if self.from_email == "":
            self.from_email = 'from@example.com'

        if type(self.recipient_list) != list:
            self.recipient_list = [self.recipient_list]
            
    def set_subject(self, subject):
        self.subject = subject

    def set_message(self, message):
        self.message = message
    
    def set_from_email(self, from_email):
        self.from_email = from_email
    
    def set_recipient_list(self, recipient_list):
        self.recipient_list = recipient_list
    
    def set_html_message(self, html_temp, context):
        htmly     = get_template(self.base_emails_html_path+html_temp)
        self.html_message = htmly.render(context)
     
#    def set_message(self, txt_temp, context):
#        plaintext      = get_template(self.base_emails_text_path+txt_temp)
#        self.message = plaintext.render(context)


    def send(self):

        # plaintext = get_template('test.txt')
        
        if self.html_message == "":
            self.html_message = self.message

        if len(self.recipient_list) == 0 or self.html_message == "":
            return False

        return send_mail(
                self.subject,
                self.message,
                self.from_email,
                self.recipient_list,
                fail_silently=False,
                html_message=self.html_message
            )

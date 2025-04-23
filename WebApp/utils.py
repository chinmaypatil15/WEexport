from django.core.mail import EmailMultiAlternatives
from .models import EmailLog

def send_logged_email(subject, message, from_email, recipient_list, 
                     html_message=None, submission=None):
    try:
        email = EmailMultiAlternatives(
            subject,
            message,
            from_email,
            recipient_list,
        )
        if html_message:
            email.attach_alternative(html_message, "text/html")
            
        email.send()
        
        # Log successful email
        for recipient in recipient_list:
            EmailLog.objects.create(
                to_email=recipient,
                subject=subject,
                status=EmailLog.SENT,
                related_submission=submission
            )
        return True
        
    except Exception as e:
        # Log failed email
        for recipient in recipient_list:
            EmailLog.objects.create(
                to_email=recipient,
                subject=subject,
                status=EmailLog.FAILED,
                related_submission=submission,
                error_message=str(e)
            )
        return False
from django.db import models

# Create your models here.

class ContactSubmission(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('sales', 'Sales Question'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    country = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class EmailLog(models.Model):
    SENT = 'sent'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (FAILED, 'Failed'),
    ]
    
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    related_submission = models.ForeignKey(
        ContactSubmission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    error_message = models.TextField(blank=True)
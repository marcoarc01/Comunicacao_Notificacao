from django.db import models

class Notification(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    recipient_id = models.CharField(max_length=50)
    recipient_type = models.CharField(max_length=20,
        choices=[
            ('patient', 'Patient'),
            ('doctor', 'Doctor'),
            ('staff', 'Staff'),
        ]
    )

    channel = models.CharField(max_length=20,
        choices=[
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('push', 'Push'),
            ('whatsapp', 'WhatsApp'),
        ]
    )

    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()

    status = models.CharField(max_length=20,
        choices=[
            ('queued', 'Queued'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
        ],default='queued'
    )

    priority = models.CharField(max_length=20,
        choices=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],default='normal'
    )
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.id} - {self.recipient_id} ({self.status})"
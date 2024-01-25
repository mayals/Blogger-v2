from django.db import models

class ContactMessage(models.Model):
    sender_name    = models.CharField(max_length=100)
    sender_email   = models.EmailField(null=True, blank=False)
    sender_message = models.TextField(blank=False)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender_name} - {self.sender_email}'

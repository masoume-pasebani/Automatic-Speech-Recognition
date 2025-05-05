from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models

class Transcription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,
        blank=True 
    )
    audio_file = models.FileField(upload_to='uploads/')
    text = models.TextField(blank=True)
    translation = models.TextField(blank=True)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id}"

from django.contrib import admin

# Register your models here.
# transcriber/admin.py
from django.contrib import admin
from .models import Transcription

admin.site.register(Transcription)

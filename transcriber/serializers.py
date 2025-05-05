from rest_framework import serializers
from .models import Transcription

class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id',  'user' ,'audio_file', 'text', 'translation', 'created_at']  # List all the fields you want to serialize

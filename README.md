# Automatic-Speech-Recognition

# Persian Audio Speech Recognition (ASR) and Translation

This project is a Persian Audio Speech Recognition (ASR) system built with Django in the backend and Bootstrap for the frontend. It allows users to upload Persian audio files (in formats such as MP3, MP4, or WAV), and the system will transcribe the audio into text. Additionally, the transcription can be downloaded as a .txt or .srt file.

The system also provides English translations of the transcribed text, enabling bilingual access to the content.

## Features

- Audio File Upload: Upload Persian audio files (MP3, MP4, WAV) for transcription.

- Speech Recognition (ASR): Converts spoken Persian audio into written Persian text using Google Speech Recognition or Whisper.

- Text and Subtitle Download: Provides downloadable .txt and .srt files containing the transcription.

- English Translation: Generates and displays an English translation of the Persian transcription using Deep Translator.

- Django Backend: Handles user requests, audio processing, and file management.

- Bootstrap Frontend: User-friendly web interface for easy interaction with the app.

Technologies Used
Backend: Django (Python)

Frontend: Bootstrap, HTML, CSS

ASR Models:

Google Speech Recognition

Whisper Large V3 via Hugging Face

Audio Handling: Pydub

Translation: Deep Translator (Google Translate)

Database: SQLite3 (default in Django)



- **Audio File Upload**: Upload Persian audio files (MP3, MP4, WAV) for transcription.
- **Speech Recognition (ASR)**: Converts spoken Persian audio into written text.
- **Text and Subtitle Download**: Provides downloadable `.txt` and `.srt` files containing the transcription.
- **English Translation**: Generates and displays an English translation of the Persian transcription.
- **Django Backend**: Handles user requests, audio processing, and file management.
- **Bootstrap Frontend**: User-friendly web interface for easy interaction with the app.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: Bootstrap, HTML, CSS
- **Audio Processing**: Whisper or other ASR models
- **Translation**: Google Translate API 
- **Database**: SQLite3 (or another preferred database)
  
## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/masoume-pasebani/Automatic-Speech-Recognition.git
   cd Automatic-Speech-Recognition

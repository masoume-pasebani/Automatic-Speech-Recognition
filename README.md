
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

## Technologies Used
- Backend: Django (Python)

- Frontend: Bootstrap, HTML, CSS

- ASR Models:
- Google Speech Recognition
- Whisper Large V3 via Hugging Face
- Audio Handling: Pydub
- Translation: Deep Translator (Google Translate)
- Database: SQLite3 (default in Django)



## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/masoume-pasebani/Automatic-Speech-Recognition.git
   cd Automatic-Speech-Recognition


## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/masoume-pasebani/Automatic-Speech-Recognition.git
cd Automatic-Speech-Recognition
2. Create and Activate Virtual Environment
bash
Copy
Edit
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4. Download and Configure FFmpeg (Windows Only)
Download FFmpeg from:

👉 https://www.gyan.dev/ffmpeg/builds/

Unzip the archive.

Copy the full path to ffmpeg.exe.

In your views.py, configure the path like this:

python
Copy
Edit
AudioSegment.ffmpeg = "C:/path/to/ffmpeg/bin/ffmpeg.exe"
5. Run Django Migrations
bash
Copy
Edit
python manage.py migrate
6. Start the Development Server
bash
Copy
Edit
python manage.py runserver
Usage
Open your browser and go to: http://127.0.0.1:8000/

Upload a Persian audio file (MP3, MP4, or WAV).

The system will:

Transcribe the audio and show the Persian text.

Display the English translation of the transcription.

You can also:

Download the transcription as a .txt file.

Download subtitles in .srt format for media use.


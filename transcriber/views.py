from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Transcription
from django.contrib.admin.views.decorators import staff_member_required
import os
import math
from pydub import AudioSegment
import speech_recognition as sr
from deep_translator import GoogleTranslator 
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def welcome(request):
    return render(request, 'transcriber/Welcome.html')



def Login(request):
    form = SignUpForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)


        if not user:
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'transcriber/Login.html')

        login(request, user)
        return redirect('transcriber:upload_audio') 

    return render(request, 'transcriber/Login.html', {'form': form})


def Register(request):
    form = SignUpForm()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.error(request, 'Password should be at least 6 characters for greater security')
            return redirect('transcriber:register')

        if password1 != password2:
            messages.error(request, 'Password Mismatch! Your Passwords Do Not Match')
            return redirect('transcriber:register')

        if not username:
            messages.error(request, 'Username is required!')
            return redirect('transcriber:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken! Choose another one')
            return redirect('transcriber:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken! Choose another one')
            return redirect('transcriber:register')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()

        login(request, user)  # Automatically log the user in after registration
        messages.success(request, 'Successful SignUp!')
        return redirect('transcriber:upload_audio')  # Redirect to index page after registration

    return render(request, 'transcriber/Register.html', {'form': form})



def Logout(request):
    
    logout(request)
    messages.success(request, 'Successfully Logged Out!')

    return redirect(reverse('transcriber:login'))


#-------------------------------------------------------------------#S


AudioSegment.ffmpeg = "C:/Users/Mohammad Derakhshani/Downloads/ffmpeg-7.1.1-full_build-shared/ffmpeg-7.1.1-full_build-shared/bin/ffmpeg.exe"

def convert_to_wav(filepath):
    """Converts any audio file to WAV format using pydub."""
    filename, ext = os.path.splitext(filepath)
    ext = ext.lower().replace('.', '')
    if ext != 'wav':
        audio = AudioSegment.from_file(filepath, format=ext)
        new_filename = filename + ".wav"
        counter = 1
        while os.path.exists(new_filename):
            new_filename = f"{filename}({counter}).wav"
            counter += 1
        audio.export(new_filename, format="wav")
        return new_filename
    else:
        return filepath

def split_audio(audio_path, chunk_length_ms=60000):
    """Splits audio into chunks (default: 60 seconds)."""
    audio = AudioSegment.from_wav(audio_path)
    duration_ms = len(audio)
    chunks = []
    for i in range(0, duration_ms, chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_filename = f"chunk_{i//chunk_length_ms}.wav"
        chunk.export(chunk_filename, format="wav")
        chunks.append(chunk_filename)
    return chunks


import re


def split_text_into_sentences(text):
    """Split text into sentences, preserving sentence boundaries."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences

def split_text(text, max_length=400):
    """Split the text into chunks of appropriate length, avoiding splitting sentences."""
    sentences = split_text_into_sentences(text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if sum(len(s) + 1 for s in current_chunk + [sentence]) <= max_length:
            current_chunk.append(sentence)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]  # Start a new chunk with the current sentence

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def to_en(textfa):
    """Translate Persian text to English in safe chunks, keeping sentences intact."""
    try:
        chunks = split_text(textfa)
        translations = []

        for i, chunk in enumerate(chunks):
            try:
                translated = GoogleTranslator(source='fa', target='en').translate(chunk)
                translations.append(translated)
            except Exception as e:
                translations.append(f"[Error in chunk {i}: {str(e)}]")

        return "\n".join(translations)

    except Exception as e:
        return f"[Translation error: {str(e)}]"


def recognize_audio(filepath):
    """Recognizes speech from (possibly large) audio file."""
    filepath = convert_to_wav(filepath)
    chunk_files = split_audio(filepath)
    
    r = sr.Recognizer()
    full_text = ""

    for chunk_file in chunk_files:
        with sr.AudioFile(chunk_file) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='fa-IR')
            full_text += text + " "
        except Exception as e:
            full_text += f"[Error in {chunk_file}: {str(e)}] "
        os.remove(chunk_file)

    return full_text.strip()
from django.contrib.auth.decorators import login_required

def upload_audio(request):
    transcription = None

    if request.method == 'POST':
        form = TranscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            transcription = form.save(commit=False)

            if request.user.is_authenticated:
                transcription.user = request.user  # Only assign if logged in

            transcription.save()

            # Run transcription pipeline
            audio_path = transcription.audio_file.path
            text_fa = recognize_audio(audio_path)
            text_en = to_en(text_fa)

            transcription.text = text_fa
            transcription.translation = text_en
            transcription.save()

            return render(request, 'transcriber/upload.html', {
                'form': TranscriptionForm(),
                'transcription': transcription,
                'translation': transcription.translation,
            })
    else:
        form = TranscriptionForm()

    return render(request, 'transcriber/upload.html', {'form': form})


@staff_member_required
def list_transcriptions(request):
    transcriptions = Transcription.objects.all().order_by('-created_at')
    return render(request, 'transcriber/list.html', {'transcriptions': transcriptions})

def download_transcription_txt(request, pk):
    transcription = get_object_or_404(Transcription, pk=pk)
    response = HttpResponse(transcription.text, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=transcription_{pk}.txt'
    return response

def generate_srt(text, chunk_duration=5):
    """Generate a simple SRT string from plain text using fixed time intervals."""
    words = text.split()
    words_per_chunk = 15
    srt_blocks = []
    num_chunks = math.ceil(len(words) / words_per_chunk)

    for i in range(num_chunks):
        chunk_words = words[i * words_per_chunk : (i + 1) * words_per_chunk]
        start_seconds = i * chunk_duration
        end_seconds = (i + 1) * chunk_duration

        def format_time(seconds):
            hrs = seconds // 3600
            mins = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d},000"

        start_time = format_time(start_seconds)
        end_time = format_time(end_seconds)
        subtitle_text = ' '.join(chunk_words)

        srt_block = f"{i+1}\n{start_time} --> {end_time}\n{subtitle_text}\n"
        srt_blocks.append(srt_block)

    return '\n'.join(srt_blocks)

def download_srt(request, pk):
    transcription = get_object_or_404(Transcription, pk=pk)
    srt_content = generate_srt(transcription.text)
    response = HttpResponse(srt_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=transcription_{pk}.srt'
    return response


import torch
from transformers import pipeline

def transcribe_with_whisper_model(audio_path):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    pipe = pipeline(
        "automatic-speech-recognition",
        model="sadeghk/whisper-large-v3",
        device=device,
        chunk_length_s=30,
        stride_length_s=5,
        generate_kwargs={"task": "transcribe", "language": "<|fa|>"},
    )

    result = pipe(audio_path)
    return result["text"]


#---------------------------------------------------------------------#

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcription
from .serializers import TranscriptionSerializer
from rest_framework.permissions import IsAdminUser

from rest_framework import viewsets
from .models import Transcription
from .serializers import TranscriptionSerializer


class TranscriptionList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        transcriptions = Transcription.objects.all()
        serializer = TranscriptionSerializer(transcriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TranscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TranscriptionViewSet(viewsets.ModelViewSet):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    permission_classes = [IsAdminUser]
# transcriber/urls.py
from django.urls import path
from . import views
from .views import TranscriptionList

app_name = 'transcriber'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('list/', views.list_transcriptions, name='list_transcriptions'),
    path('download/<int:pk>/', views.download_transcription_txt, name='download_transcription_txt'),
    path('download_srt/<int:pk>/', views.download_srt, name='download_transcription_srt'),
    path('api/transcriptions/', TranscriptionList.as_view(), name='transcription-list'),
    path('login/', views.Login, name='login'), 
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),

]



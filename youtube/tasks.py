from celery import shared_task
from django.core.mail import send_mail
import youtube_dl
from .models import YoutubeModel

DOWNLOAD_OPTIONS_MP3 = {
            'format': 'bestaudio/best',
            'outtmpl': 'media/%(id)s.%(ext)s',
            'nocheckcertificate' : True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

@shared_task
def send_email_task(email, url):
    send_mail('Download your mp3', url, 'adidovvv.arslan@gmail.com', [email])
    return None

@shared_task
def download_music(url):
    with youtube_dl.YoutubeDL(DOWNLOAD_OPTIONS_MP3) as dl:
        dl.download([url])
    return None


def get_info(url):
    with youtube_dl.YoutubeDL(DOWNLOAD_OPTIONS_MP3) as dl:
        result = dl.extract_info(url, download=False)
        return result
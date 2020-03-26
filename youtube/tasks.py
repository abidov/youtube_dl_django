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
def do_all(email, url, download_url):
    with youtube_dl.YoutubeDL(DOWNLOAD_OPTIONS_MP3) as dl:
        result = dl.extract_info(url)
        download_url += result.get('id')
        try:
            YoutubeModel.objects.create(url=url, mp3_title=result.get('title'), mp3_id=result.get('id'))
        except:
            pass
        send_mail('Download your mp3', download_url, 'adidovvv.arslan@gmail.com', [email])
    return None
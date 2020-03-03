from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from . import tasks
from django.http import HttpResponse, Http404
from .models import YoutubeModel

# Create your views here.
class index(View):
    def get(self, request):
        form = YoutubeForm()
        return render(request, 'index.html', {'form': form})
    def post(self, request):
        form = YoutubeForm(request.POST)
        if form.is_valid():
            mp3_data = tasks.get_info(request.POST.get('url'))
            tasks.download_music.delay(request.POST.get('url'))
            try:
                YoutubeModel.objects.create(url=request.POST.get('url'), mp3_title=mp3_data.get('title'), mp3_id=mp3_data.get('id'))
            except:
                pass
            tasks.send_email_task.delay(request.POST.get('email'), f'{request.build_absolute_uri()}download/{mp3_data.get("id")}')
        return render(request, 'done.html', {})

def download(request, mp3_id):
    try:
        file_ = open(f'media/{mp3_id}.mp3', 'rb').read()
        response = HttpResponse(file_, content_type='audio/mpeg')
        youtube_mp3_title = YoutubeModel.objects.get(mp3_id=mp3_id).mp3_title
        response['Content-Disposition'] = f"attachment; filename={youtube_mp3_title}.mp3"
    except:
        raise Http404('Error')
    return response
# запустить воркера celery в manage.py и запустить redis в отдельном терминале.
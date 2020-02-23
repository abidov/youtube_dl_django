from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from . import task
from django.http import HttpResponse, Http404

# Create your views here.
class index(View):
    def get(self, request):
        form = YoutubeForm()
        return render(request, 'index.html', {'form': form})
    def post(self, request):
        form = YoutubeForm(request.POST)
        if form.is_valid():
            mp3_data = task.download_music(request.POST.get('url'))
            task.send_email_task(request.POST.get('email'), f'{request.build_absolute_uri()}download/{mp3_data}')
        return render(request, 'done.html', {})

def download(request, mp3_id):
    try:
        file = open(f'media/{mp3_id}.mp3', 'rb').read()
        response = HttpResponse(file, content_type='audio/mpeg')
        response['Content-Disposition'] = "attachment; filename=%s.mp3" % (mp3_id)
    except:
        raise Http404('Error')
    return response
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from . import tasks
from django.http import HttpResponse, Http404
from .models import YoutubeModel
from django.conf import settings

# Create your views here.
class index(View):
    def get(self, request):
        form = YoutubeForm()
        return render(request, 'index.html', {'form': form})
    def post(self, request):
        form = YoutubeForm(request.POST)
        if form.is_valid():
            tasks.do_all.delay(request.POST.get('email'), request.POST.get('url'), f'{request.build_absolute_uri()}download/')
        return render(request, 'done.html', {})

def download(request, mp3_id):
    file_ = open(f'{settings.BASE_DIR}/media/{mp3_id}.mp3', 'rb').read()
    response = HttpResponse(file_, content_type='audio/mpeg')
    youtube_mp3_title = YoutubeModel.objects.get(mp3_id=mp3_id).mp3_title
    response['Content-Disposition'] = f"attachment; filename={youtube_mp3_title}.mp3"
    return response
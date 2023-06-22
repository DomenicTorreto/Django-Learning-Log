from django.shortcuts import render
from .models import Topic


def index(request):
    """Home page of application learning log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Page wits topics"""
    topics = Topic.objects.all
    context = {"topics": topics}
    return render(request, 'learning_logs/topics.html', context)

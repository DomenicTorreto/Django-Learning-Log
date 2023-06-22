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


def topic(request, topic_id):
    """Output one page and all its of record"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


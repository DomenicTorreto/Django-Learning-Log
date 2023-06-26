from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm


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


def new_topic(request):
    """Defines a new topic"""
    if request.method != 'POST':
        # The date was not sent; empty form is created
        form = TopicForm()
    else:
        # Sent data POST; processing data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # Output an empty or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """Home page of application learning log"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Page wits topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics": topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Output one page and all its of record"""
    topic = Topic.objects.get(id=topic_id)
    # Checking that the topic belongs to the current user
    check_topic_owner(request=request, topic=topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Defines a new topic"""
    if request.method != 'POST':
        # The date was not sent; empty form is created
        form = TopicForm()
    else:
        # Sent data POST; processing data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Output an empty or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adding new entry on a specific topic """
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request=request, topic=topic)
    if request.method != 'POST':
        # The date was not sent; empty form is created
        form = EntryForm()
    else:
        # Sent data POST; processing data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Output an empty or invalid form
    context = {'topic': topic,
               'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edits existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request=request, topic=topic)

    if request != 'POST':
        # Original request; Form is filled in with the data of the current record
        form = EntryForm(instance=entry)
    else:
        # Sending data of POST; Processing data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry,
               'topic': topic,
               'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404


@api_view(['GET'])
def test_page(request):
    return Response('Hello, this a test page')

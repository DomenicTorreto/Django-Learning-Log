from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


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


def new_entry(request, topic_id):
    """Adding new entry on a specific topic """
    topic = Topic.objects.get(id=topic_id)
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


def edit_entry(request, entry_id):
    """Edits existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

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

from django.shortcuts import render


def index(request):
    """Home page of application learning log"""
    return render(request, 'learning_logs/index.html')

"""Defining the URL scheme for learning_logs"""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page with list of all topics
    path('topics/', views.topics, name='topics'),
    # Page with detailed information on a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]

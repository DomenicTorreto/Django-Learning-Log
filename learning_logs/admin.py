from django.contrib import admin
from .models import Topic, Entry


class TopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Topic)
admin.site.register(Entry)

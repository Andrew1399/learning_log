from django.contrib import admin
from topics.models import Topic, Entry

# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):
#     list_display = ['title', 'date_added']
#     list_filter = ['date_added']
#
# @admin.register(Entry)
# class EntryAdmin(admin.ModelAdmin):
#     list_display = ['topic', 'text', 'date_added', 'date_updated']

admin.site.register(Topic)
admin.site.register(Entry)


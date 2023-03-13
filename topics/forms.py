from django import forms
from topics.models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'description', 'public', 'favorite')
        labels = {'title': 'Title of your topic'}
        widgets = {'description': forms.Textarea(attrs={'cols': 40})}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
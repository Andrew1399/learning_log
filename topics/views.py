from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from users.models import Profile
from topics.models import Topic, Entry
from topics.forms import TopicForm, EntryForm


def index(request):
    return render(request, 'topics/index.html')


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404

@login_required
def get_topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'topics/topics.html', {'topics': topics})


@login_required
def get_single_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    return render(request, 'topics/topic.html', {'topic': topic, 'entries': entries})


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_top = form.save(commit=False)
            new_top.owner = request.user
            if new_top.public:
                new_top.public = True
            if new_top.favorite:
                new_top.favorite = True
            new_top.save()
            return redirect('topics:topics')
    return render(request, 'topics/new_topic.html', {'form': form})


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.save()
        return redirect('topics:topic', topic_id=topic_id)
    return render(request, 'topics/new_entry.html', {'topic': topic, 'form': form})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('topics:topic', topic_id=topic.id)
    return render(request, 'topics/edit_entry.html', {'entry': entry, 'topic': topic, 'form': form})


@login_required
def users_public_topics(request):
    public_topics = Topic.objects.filter(public=True)
    return render(request, 'topics/public_topics.html', {'public_topics': public_topics})


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    topic.delete()
    return HttpResponseRedirect(reverse_lazy('topics:topics'))


@login_required
def delete_entry(request, entry_id, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    entry = get_object_or_404(Entry, id=entry_id, topic=topic)
    entry.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_topic(request, pk):
    topic = get_object_or_404(Topic, id=request.POST.get('topic_id'))
    liked = False

    if topic.likes.filter(id=request.user.id).exists():
        topic.likes.remove(request.user)
        liked = False
    else:
        topic.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


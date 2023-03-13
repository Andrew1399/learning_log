from django.db import models
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class ProfileManager(models.Manager):

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):

    first_name = models.CharField(max_length=120, db_index=True)
    last_name = models.CharField(max_length=120, db_index=True)
    email = models.EmailField(max_length=350, db_index=True)
    about = models.CharField(max_length=100)
    bio = models.TextField(max_length=2000, db_index=True)
    age = models.CharField(max_length=2)
    birthday_year = models.CharField(max_length=4)
    country = models.CharField(max_length=60, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', db_index=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def save(self, *args, **kwargs):
        # self.slug = slugify(f"{self.first_name} - {self.last_name}")
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={"slug": self.slug})

    def get_topics_list(self):
        return self.user.topics.count()

    def count_favorite_topics(self):
        from topics.models import Topic
        topics = Topic.objects.filter(owner__username=self.user, favorite=True)
        return topics.count()

    def count_users_entries(self):
        from topics.models import Entry, Topic
        topic = Topic.objects.filter(owner__username=self.user)
        entry = Entry.objects.filter(topic__id__in=topic)
        return entry.count()

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%d.%m.%Y')}"

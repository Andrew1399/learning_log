from django.db import models
from django.contrib.auth.models import User
from users.models import Profile


class Topic(models.Model):
    title = models.CharField(max_length=210)
    # image = models.ImageField(upload_to='images', db_index=True)
    description = models.TextField(max_length=300, blank=True)
    public = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        ordering = ('-date_added',)

    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        if self.text > self.text[:50]:
            return f'{self.text[:50]}...'
        else:
            return self.text


# class Like(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

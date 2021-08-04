from django.db import models
from django.utils import timezone
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now())
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'notes:note_detail',
            kwargs={'slug': self.slug})

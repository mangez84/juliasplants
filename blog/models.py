from django.db import models
from profiles.models import UserProfile
from plants.models import Plant


class BlogPost(models.Model):
    """A model to store blog posts."""
    class Meta:
        verbose_name_plural = 'Blog Posts'

    title = models.CharField(max_length=150, null=False, blank=False)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=False, blank=False)
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.title)

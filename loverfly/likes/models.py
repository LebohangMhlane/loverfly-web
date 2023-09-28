from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Liker(models.Model):
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, blank=False, null=True)
    liker = models.ForeignKey(
        "accounts.UserProfile", on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.id) + " - " + self.liker.username

    def delete(self):
        self.post.likes = self.post.likes - 1
        self.post.save()
        super().delete()


@receiver(post_save, sender=Liker)
def set_like_count(instance, **kwargs):
    instance.post.likes = Liker.objects.filter(post=instance.post.id).count()
    instance.post.save()

from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Post

# Create your models here.


class Comment(models.Model):
    owner = models.ForeignKey(
        to="accounts.UserProfile", on_delete=models.CASCADE)
    comment = models.CharField(
        max_length=50, blank=False, null=False, default="")
    date_posted = models.DateTimeField(auto_now=True, blank=False, null=True)
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, blank=False, null=True)
    comment_likes = models.PositiveBigIntegerField(default=0, blank=True)

    def __str__(self):
        return self.owner.username


class CommentLike(models.Model):
    owner = models.ForeignKey(
        to="accounts.UserProfile", on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, blank=True, null=True, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now=True, blank=False, null=True)

    def __str__(self):
        return self.owner.username + " - " + str(self.comment.id)

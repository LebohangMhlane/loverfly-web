from django.db import models
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from posts.models import Post
from accounts.models import UserProfile

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
    

@receiver(pre_save, sender=Comment)
def update_comment_likes(instance, **kwargs):
    if instance.id:
        comment_like_count = CommentLike.objects.filter(comment=instance).count()
        instance.comment_likes = comment_like_count


class CommentLike(models.Model):
    owner = models.ForeignKey(
        to="accounts.UserProfile", on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, blank=True, null=True, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now=True, blank=False, null=True)

    def __str__(self):
        return self.owner.username + " - " + str(self.comment.id)


class CommentReply(models.Model):
    comment_replied_to = models.ForeignKey(to=Comment, blank=False, null=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    replier = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    comment_reply = models.CharField(max_length=50, blank=False, null=True)


class CommentReplyLike(models.Model):
    comment_reply = models.ForeignKey(to=CommentReply, on_delete=models.CASCADE)
    liker = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)


    
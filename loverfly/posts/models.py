import django
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from couples.models import Couple
from likes.models import Liker

class Post(models.Model):
    class Meta:
        get_latest_by = "time_posted"

    couple = models.ForeignKey(
        Couple, related_name="post_owner", blank=True, null=True, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(default=django.utils.timezone.now)
    caption = models.CharField(max_length=25, null=True, blank=True)
    post_image = models.CharField(max_length=2000, null=False, default="")
    likes = models.PositiveBigIntegerField(default=0, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.couple) + " - " + str(self.caption)
    
@receiver(pre_save, sender=Post)
def update_likes(instance, **kwargs):
    if instance.id:
        number_of_likes = Liker.objects.filter(post=instance).count()
        instance.likes = number_of_likes

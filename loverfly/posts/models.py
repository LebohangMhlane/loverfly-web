import django
from django.db import models
from couples.models import Couple

# Create your models here.


class Post(models.Model):
    class Meta:
        get_latest_by = "time_posted"

    couple = models.ForeignKey(
        Couple, related_name="post_owner", blank=True, null=True, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(default=django.utils.timezone.now)
    caption = models.CharField(max_length=25, null=True, blank=True)
    image = models.CharField(max_length=1000, null=True, blank=True)
    likes = models.PositiveBigIntegerField(default=0, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.couple) + " - " + str(self.caption)

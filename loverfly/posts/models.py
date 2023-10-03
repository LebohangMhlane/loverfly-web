import django
from django.db import models
from couples.models import Couple

# Create your models here.

def post_image_location(post, filename):
    return f"post_images/{post.couple.id}/{filename}"

class Post(models.Model):
    class Meta:
        get_latest_by = "time_posted"

    couple = models.ForeignKey(
        Couple, related_name="post_owner", blank=True, null=True, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(default=django.utils.timezone.now)
    caption = models.CharField(max_length=25, null=True, blank=True)
    post_image = models.ImageField(upload_to=post_image_location, blank=False, null=True)
    likes = models.PositiveBigIntegerField(default=0, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.couple) + " - " + str(self.caption)
    


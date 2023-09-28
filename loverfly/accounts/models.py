from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from favourites.models import Fan
from likes.models import Liker


class UserProfile(models.Model):
    is_active = models.BooleanField(default=True)
    is_straight = models.BooleanField(default=True)
    user = models.OneToOneField(
        User, blank=False, null=True, related_name="user", on_delete=models.CASCADE
    )
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.CharField(max_length=500, null=True, blank=True)
    my_partner = models.OneToOneField(
        to="self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="partner",
    )
    account_linkage_code = models.CharField(
        max_length=5, unique=True, blank=True, null=True)
    number_of_favourite_couples = models.PositiveBigIntegerField(default=0)
    number_of_liked_posts = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_profile(instance, **kwargs):
    try:
        # create the user profile is it doesn't exist:
        _ = UserProfile.objects.get_or_create(
            user=instance,
            username=instance.username,
            email=instance.email,
        )
    except Exception as e:
        print(
            f"An error occured during signal function : create_user_profile : {str(e)}")


@receiver(pre_save, sender=UserProfile)
def set_couple_and_like_counts(instance, **kwargs):
    if instance.id:
        try:
            # set the numerical count of all the couples that i follow:
            instance.number_of_favourite_couples = len(
                Fan.objects.filter(fan=instance))
            instance.number_of_liked_posts = len(
                Liker.objects.filter(liker=instance))
        except:
            print("Error in: set_couple_and_like_counts")

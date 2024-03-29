from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from admirers.models import Admirer
from likes.models import Liker

class UserProfile(models.Model):
    is_active = models.BooleanField(default=True)
    is_straight = models.BooleanField(default=True)
    user = models.OneToOneField(
        User, blank=False, null=True, related_name="user", on_delete=models.CASCADE
    )
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.OneToOneField(to="ProfilePicture", blank=True, null=True, on_delete=models.CASCADE)
    my_partner = models.OneToOneField(
        to="self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="partner",
    )
    account_linkage_code = models.CharField(
        max_length=5, unique=True, blank=True, null=True)
    number_of_admired_couples = models.PositiveBigIntegerField(default=0)
    number_of_liked_posts = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def create_user_profile(instance, **kwargs):
    try:
        # create the user profile is it doesn't exist:
        user_profile, created = UserProfile.objects.get_or_create(
            user=instance,
            username=instance.username,
            email=instance.email,
        )
        # once a user profile is created create a profile picture instance for it:
        ProfilePicture.objects.create(user_profile=user_profile)
    except Exception as e:
        print(
            f"An error occured during signal function : create_user_profile : {str(e)}")

@receiver(pre_save, sender=UserProfile)
def set_couple_and_like_counts(instance, **kwargs):
    if instance.id:
        try:
            # set the numerical count of all the couples that i follow:
            instance.number_of_admired_couples = Admirer.objects.filter(admirer=instance).count()
            instance.number_of_liked_posts = Liker.objects.filter(liker=instance).count()
        except:
            print("Error in: set_couple_and_like_counts")

def set_profile_picture_location(profile_picture, filename):
    return f"profile_pictures/{profile_picture.user_profile.id}"

class ProfilePicture(models.Model):
    user_profile = models.OneToOneField(to=UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    image = models.CharField(max_length=2000, null=False, default="")

    def __str__(self) -> str:
        return f"{self.user_profile.id} - {self.user_profile.username}"

@receiver(post_save, sender=ProfilePicture)
def set_profile_picture_on_profile(instance, **kwargs):
    try:
        instance.user_profile.profile_picture = instance
        instance.user_profile.save()
    except:
        pass

class UserSetting(models.Model):

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    dark_mode_on = models.BooleanField(default=False)
    hide_posts = models.BooleanField(default=False)

    def set_dark_mode(self, value:bool):
        self.dark_mode_on = value

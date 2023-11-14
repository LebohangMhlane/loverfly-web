
import django
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from accounts.models import UserProfile
from admirers.models import Admirer

class Couple(models.Model):
    partner_one = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="partner_one")
    partner_two = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="partner_two")
    couple_data = models.CharField(max_length=800, blank=True, null=True)
    started_dating = models.DateField(default=django.utils.timezone.now)
    anniversaries = models.PositiveBigIntegerField(default=0)
    admirers = models.PositiveBigIntegerField(default=0, blank=True)
    last_anniversary = models.DateField(default=django.utils.timezone.now)
    next_anniversary = models.DateField(default=django.utils.timezone.now)
    relationship_status = models.CharField(max_length=100, default="Dating")
    is_straight_couple = models.BooleanField(default=True)
    limbo = models.BooleanField(default=False)
    limbo_date = models.DateField(default=django.utils.timezone.now)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    has_posts = models.BooleanField(default=False)

    def __str__(self):
        return self.partner_one.username + " + " + self.partner_two.username

    def get_next_anniversary(self):
        return self.next_anniversary.date

    def get_started_dating(self):
        return self.started_dating.date

    def get_last_anniversary(self):
        return self.last_anniversary.date

# TODO: come back to this later. it may not be needed:
@receiver(pre_save, sender=Couple)
def set_partner_data(instance, *args, **kwargs):
    if not instance.partner_one.my_partner or not instance.partner_two.my_partner:
        instance.partner_one.my_partner = instance.partner_two
        instance.partner_two.my_partner = instance.partner_one
        instance.partner_one.save()
        instance.partner_two.save()

@receiver(pre_save, sender=Couple)
def update_admirer_counts(instance, *args, **kwargs):
    instance.admirers = Admirer.objects.filter(couple=instance).count()

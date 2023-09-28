from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Fan(models.Model):
    couple = models.ForeignKey(
        "couples.Couple", on_delete=models.CASCADE, blank=False, null=True)
    fan = models.ForeignKey(
        "accounts.UserProfile", on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.couple.id) + " - " + self.fan.username

    def delete(self):
        self.couple.fans = self.couple.fans - 1
        self.couple.save()
        super().delete()


@receiver(post_save, sender=Fan)
def set_fan_count(instance, **kwargs):
    instance.couple.fans = instance.couple.fans + 1
    instance.couple.save()

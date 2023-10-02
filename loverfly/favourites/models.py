from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Admirer(models.Model):
    couple = models.ForeignKey(
        "couples.Couple", on_delete=models.CASCADE, blank=False, null=True)
    admirer = models.ForeignKey(
        "accounts.UserProfile", on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.couple.id) + " - " + self.admirer.username

    def delete(self):
        self.couple.admirers = self.couple.admirers - 1
        self.couple.save()
        super().delete()


@receiver(post_save, sender=Admirer)
def set_admirer_count(instance, **kwargs):
    instance.couple.admirers = instance.couple.admirers + 1
    instance.couple.save()

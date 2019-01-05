from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Match(models.Model):
    playerA = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, related_name="matches_as_player_a")
    playerB = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, related_name="matches_as_player_b")
    
class Game(models.Model):
    TYPE_CHOICES = (
        (0, 'Draw'),
        (1, 'PlayerA'),
        (2, 'PlayerB'),
    )

    result = models.PositiveIntegerField(
        choices=TYPE_CHOICES, default=0, verbose_name='wynik')
    match = models.ForeignKey(Match, models.SET_NULL, blank=True, null=True)
    moves = models.TextField()




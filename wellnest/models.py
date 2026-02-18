from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from datetime import date

# Create your models here.

class User(AbstractUser):
    pass

# Each entry belongs to one user, stores text and automatically saves date & time
class Entry(models.Model):
    MOOD_CHOICES = [
        (1, "Very bad"),
        (2, "Bad"),
        (3, "Neutral"),
        (4, "Good"),
        (5, "Very good"),
    ]

    DAY_QUALITY = [
        (1, "Very bad"),
        (2, "Bad"),
        (3, "Neutral"),
        (4, "Good"),
        (5, "Very good"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    text = models.TextField()
    mood = models.IntegerField(choices=MOOD_CHOICES)
    quality = models.IntegerField(choices=DAY_QUALITY)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class DailyCheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_checkins")
    date = models.DateField(default=date.today)

    MOOD_CHOICES = [
        (1, "Very bad"),
        (2, "Bad"),
        (3, "Okay"),
        (4, "Good"),
        (5, "Great"),
    ]

    ENERGY_CHOICES = [
        (1, "Very low"),
        (2, "Low"),
        (3, "Okay"),
        (4, "Good"),
        (5, "Very good"),
    ]

    STRESS_CHOICES = [
        (1, "Very low"),
        (2, "Low"),
        (3, "Moderate"),
        (4, "High"),
        (5, "Very high"),
    ]

    SLEEP_CHOICES = [
        (1, "Very poor"),
        (2, "Poor"),
        (3, "Okay"),
        (4, "Good"),
        (5, "Great"),
    ]

    SOCIAL_CHOICES = [
        (1, "None"),
        (2, "Some"),
        (3, "A few"),
        (4, "A lot"),
        (5, "Very social day"),
    ]

    ACTIVITY_CHOICES = [
        (1, "Not at all"),
        (2, "A little"),
        (3, "Some"),
        (4, "Quite a bit"),
        (5, "A lot"),
    ]

    mood = models.IntegerField(choices=MOOD_CHOICES)
    energy = models.IntegerField(choices=ENERGY_CHOICES)
    stress = models.IntegerField(choices=STRESS_CHOICES)
    sleep = models.IntegerField(choices=SLEEP_CHOICES)
    social = models.IntegerField(choices=SOCIAL_CHOICES)
    activity = models.IntegerField(choices=ACTIVITY_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user} - {self.date}"

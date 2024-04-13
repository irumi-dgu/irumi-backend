from django.db import models

class Lamplight(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(
        max_length=10,
        null=False,
        blank=False)
    content = models.TextField(
        max_length=300,
        null=False,
        blank=False
    )
    email = models.EmailField(
        null=False,
        blank=False
    )
    THEME_CHOICES = [
        (1, '1'), #1학기가 끝난 뒤
        (2, '2'), #올해가 끝난 뒤
        (3, '3') #내년 오늘
    ]
    theme = models.IntegerField(choices=THEME_CHOICES, default=1)
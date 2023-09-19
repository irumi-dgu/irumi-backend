from django.db import models
from django.core.validators import RegexValidator

class Lantern(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        validators=[RegexValidator(r'^[^\s]{1,10}$', "공백없이 닉네임을 입력해주세요.")],
        help_text="공백없이 닉네임을 입력해주세요."
    )    
    content = models.TextField(max_length=100, null=False, blank=False)
    password = models.CharField(
        max_length=4, 
        validators=[RegexValidator(r'^\d{4}$', "네 자리 숫자를 입력해주세요.")], 
        help_text="네 자리 숫자를 입력해주세요."
    )

class LanternReaction(models.Model):
    REACTION_CHOICES = (("like", "Like"), ("dislike", "Dislike"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    lantern = models.ForeignKey(Lantern, on_delete=models.CASCADE, related_name='reactions')
    user_id = models.CharField(max_length=36)


from django.db import models
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string

class Lantern(models.Model):

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        #validators=[RegexValidator(r'^[^\s]{1,10}$', "공백없이 닉네임을 입력해주세요.")],
        #help_text="공백없이 닉네임을 입력해주세요."
    )
    content = models.TextField(max_length=100, null=False, blank=False)
    password = models.CharField(
        max_length=4, 
        #validators=[RegexValidator(r'^\d{4}$', "네 자리 숫자를 입력해주세요.")], 
        #help_text="네 자리 숫자를 입력해주세요."
    )
    light_bool = models.BooleanField(blank=True, default=False)
    is_liked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    COLOR_CHOICES = [
        (1, '1'), # red
        (2, '2'), # yellow
        (3, '3'), # green
        (4, '4'), # blue
        (5, '5'), # purple
    ]
    lantern_color = models.IntegerField(choices=COLOR_CHOICES, default=1)

class LanternReaction(models.Model):
    REACTION_CHOICES = (("like", "Like"), ("dislike", "Dislike"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    lantern = models.ForeignKey(Lantern, on_delete=models.CASCADE, related_name='reactions')
    user_id = models.CharField(max_length=36)

class Fortune(models.Model):
    user_id = models.CharField(max_length=36, unique=True)
    fortune = models.TextField()

class ReportCategory(models.Model):
    CATEGORY_CHOICES = (
        ('abuse', '욕설 및 비하'),
        ('fraud', '개인정보 유출 및 사칭, 사기'),
        ('explicit', '음란물 또는 불건전한 대화'),
        ('promotion', '영리목적이나 홍보성 게시글'),
    )
    name = models.CharField(choices=CATEGORY_CHOICES, max_length=50, unique=True)

class Report(models.Model):
    lantern = models.ForeignKey(Lantern, on_delete=models.CASCADE)
    categories = models.ManyToManyField(ReportCategory)
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=10, default=get_random_string(length=10))
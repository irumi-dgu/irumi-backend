from django.db import models
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
# django-multiselectfield 오버라이딩
from multiselectfield import MultiSelectField as MSField

class MultiSelectField(MSField):
    """
    Custom Implementation of MultiSelectField to achieve Django 5.0 compatibility

    See: https://github.com/goinnn/django-multiselectfield/issues/141#issuecomment-1911731471
    """

    def _get_flatchoices(self):
        flat_choices = super(models.CharField, self).flatchoices

        class MSFFlatchoices(list):
            # Used to trick django.contrib.admin.utils.display_for_field into not treating the list of values as a
            # dictionary key (which errors out)
            def __bool__(self):
                return False

            __nonzero__ = __bool__

        return MSFFlatchoices(flat_choices)

    flatchoices = property(_get_flatchoices)

class Lantern(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(
        max_length=8,
        null=False,
        blank=False,
        #validators=[RegexValidator(r'^[^\s]{1,10}$', "공백없이 닉네임을 입력해주세요.")],
        #help_text="공백없이 닉네임을 입력해주세요."
    )
    content = models.TextField(max_length=100, null=False, blank=False)
    password = models.CharField(
        max_length=255, 
        #validators=[RegexValidator(r'^\d{4}$', "네 자리 숫자를 입력해주세요.")], 
        #help_text="네 자리 숫자를 입력해주세요."
    )
    light_bool = models.BooleanField(blank=True, default=False)
    is_liked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    COLOR_CHOICES = [
        ('pink', 'pink'), # pink
        ('green', 'green'), # green
        ('purple', 'purple'), # purple
        ('blue', 'blue'), # blue
        ('yellow', 'yellow'), # yellow
    ]
    lanternColor = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES, 
        default='pink')

class LanternReaction(models.Model):
    REACTION_CHOICES = (("like", "Like"), ("dislike", "Dislike"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    lantern = models.ForeignKey(Lantern, on_delete=models.CASCADE, related_name='reactions')
    user_id = models.CharField(max_length=36, null=True)

class Fortune(models.Model):
    user_id = models.CharField(max_length=36, unique=True)
    fortune = models.TextField()
    

class Report(models.Model):
    lantern = models.ForeignKey(Lantern, on_delete=models.CASCADE)
    CATEGORY_CHOICES = (
        ('abuse', '욕설 및 비하'),
        ('fraud', '개인정보 유출 및 사칭, 사기'),
        ('explicit', '음란물 또는 불건전한 대화'),
        ('promotion', '영리목적이나 홍보성 게시글'),
    )
    category = MultiSelectField(choices=CATEGORY_CHOICES, max_choices=4, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=36, null=True)
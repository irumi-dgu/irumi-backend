from django.db import models

class Lantern(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=10, null=False, blank=False)
    content = models.TextField(max_length=100, null=False, blank=False)
    password = models.CharField(
        max_length=4, 
        min_length=4, 
        validators=[RegexValidator(r'^\d{4}$', "네 자리 숫자를 입력해주세요.")], 
        help_text="네 자리 숫자를 입력해주세요."
    )
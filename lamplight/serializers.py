from rest_framework import serializers

from .models import *

class LamplightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lamplight
        fields = [
            'id',
            'nickname',
            'content',
            'email',
            'theme'
        ]

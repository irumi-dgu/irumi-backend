from django.contrib import admin
from .models import *

class LamplightAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'content', 'email', 'theme')
    list_filter = ('theme', )
    search_fields = ('email', 'theme')
    
    def lamp_content(self, obj):
        return obj.lamp.content
    lamp_content.short_description = "Lamp Content"

admin.site.register(Lamplight, LamplightAdmin)
from django.contrib import admin
from .models import *

#신고 관련 어드민 내용
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'lantern_content', 'reported_categories', 'user_id', 'created_at')
    list_filter = ('created_at', )
    search_fields = ('lantern__content', 'user_id')
    
    def lantern_content(self, obj):
        return obj.lantern.content
    lantern_content.short_description = "Lantern Content"

    def reported_categories(self, obj):
        return ', '.join([dict(Report.CATEGORY_CHOICES).get(cat) for cat in obj.category])
    reported_categories.short_description = "Reported Categories"

admin.site.register(Report, ReportAdmin)
admin.site.register(Lantern)
admin.site.register(LanternReaction)
admin.site.register(Fortune)
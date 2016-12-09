from django.contrib import admin

# Register your models here.
from student import models

class StuAdmin(admin.ModelAdmin):
    raw_id_fields = ('stu_name',)


class ReferralAdmin(admin.ModelAdmin):
    search_fields = ('qq','referralfrom__stu_name__qq')
    def get_actions(self, request):
        actions = super(ReferralAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(models.StuAccount)
admin.site.register(models.Referral, ReferralAdmin)
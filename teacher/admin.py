from django.contrib import admin

# Register your models here.
from teacher import models


class StudyConsultRecordAdmin(admin.ModelAdmin):
    search_fields = ('enrollment__customer__qq',)
    raw_id_fields = ('enrollment',)


admin.site.register(models.StudyConsultRecord, StudyConsultRecordAdmin )
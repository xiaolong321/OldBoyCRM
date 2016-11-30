from django.contrib import admin

# Register your models here.
from student import models

class StuAdmin(admin.ModelAdmin):
    raw_id_fields = ('stu_name',)

admin.site.register(models.StuAccount)
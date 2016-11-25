from django.contrib import admin

# Register your models here.
from student import models


admin.site.register(models.Stutest)
admin.site.register(models.StuAccount)
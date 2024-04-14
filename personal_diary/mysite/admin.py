from django.contrib import admin
from mysite import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Diary)
admin.site.register(models.Vote)
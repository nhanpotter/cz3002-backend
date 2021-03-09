from django.contrib import admin

from .models import Patient, GameTest, TrailMakingTest, PictureObjectMatchingTest

admin.site.register(Patient)
admin.site.register(GameTest)
admin.site.register(TrailMakingTest)
admin.site.register(PictureObjectMatchingTest)

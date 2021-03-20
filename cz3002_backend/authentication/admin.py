from django.contrib import admin

from .models import User


@admin.register(User)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'birthday')

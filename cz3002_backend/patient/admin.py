from django.contrib import admin

from .models import Patient, GameTest, TrailMakingTest, PictureObjectMatchingTest


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class PatientAdminInline(admin.TabularInline):
    model = Patient


class TrailMakingTestAdminInline(admin.TabularInline):
    model = TrailMakingTest


class PictureObjectMatchingAdminInline(admin.TabularInline):
    model = PictureObjectMatchingTest


@admin.register(GameTest)
class GameTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_user')
    inlines = (TrailMakingTestAdminInline, PictureObjectMatchingAdminInline)

    def patient_user(self, obj):
        return obj.patient.user

    patient_user.admin_order_field = 'patient__user'


@admin.register(TrailMakingTest)
class TrailMakingTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_test', 'game_test_patient_user', 'score', 'errors', 'time_taken')

    def game_test_patient_user(self, obj):
        return obj.game_test.patient.user

    game_test_patient_user.admin_order_field = 'game_test__patient__user'


@admin.register(PictureObjectMatchingTest)
class PictureObjectMatchingTest(admin.ModelAdmin):
    list_display = ('id', 'game_test', 'game_test_patient_user', 'score', 'errors', 'time_taken')

    def game_test_patient_user(self, obj):
        return obj.game_test.patient.user

    game_test_patient_user.admin_order_field = 'game_test__patient__user'

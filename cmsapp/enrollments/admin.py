from django.contrib import admin
from .models import Enrollment, Progress, CourseCompletion, Attendance

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled', 'status')
    search_fields = ('student__username', 'course__name')
    list_filter = ('status', 'course')
    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'date_enrolled', 'status'),
        }),
        ('Advanced options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (),
        }),
    )

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'date_completed')
    search_fields = ('student__username', 'lesson__title')
    list_filter = ('completed',)
    fieldsets = (
        (None, {
            'fields': ('student', 'lesson', 'completed', 'date_completed'),
        }),
        ('Advanced options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (),
        }),
    )

class CourseCompletionAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'completion_date', 'final_grade')
    search_fields = ('student__username', 'course__name')
    list_filter = ('final_grade',)
    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'completion_date', 'final_grade'),
        }),
        ('Advanced options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (),
        }),
    )

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'attended_on', 'status')
    search_fields = ('student__username', 'lesson__title')
    list_filter = ('status', 'attended_on')
    fieldsets = (
        (None, {
            'fields': ('student', 'lesson', 'attended_on', 'status'),
        }),
        ('Advanced options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (),
        }),
    )

# Register the models with the admin site
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(CourseCompletion, CourseCompletionAdmin)
admin.site.register(Attendance, AttendanceAdmin)

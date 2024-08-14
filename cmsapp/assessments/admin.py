from django.contrib import admin
from .models import Assessment, Submission

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1
    readonly_fields = ('submitted_on',)
    can_delete = True
    classes = ('grp-collapse grp-open',)  # Grappelli collapsible settings
    inline_classes = ('grp-collapse grp-open',)
    sortable_field_name = "id"  # Add sorting functionality

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'unit', 'lesson_plan', 'max_score', 'due_date', 'status', 'average_score', 'completion_rate')
    list_filter = ('status', 'course', 'unit', 'lesson_plan', 'due_date')
    search_fields = ('name', 'description')
    inlines = [SubmissionInline]
    readonly_fields = ('average_score', 'completion_rate')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'course', 'unit', 'lesson_plan', 'study_materials', 'max_score', 'due_date', 'status')
        }),
        ('Statistics', {
            'classes': ('grp-collapse grp-closed',),  # Grappelli collapsible settings
            'fields': ('average_score', 'completion_rate'),
        }),
    )
    ordering = ('due_date',)
    change_list_template = "admin/change_list_filter_sidebar.html"  # Sidebar filters template

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'student', 'submitted_on', 'grade')
    list_filter = ('assessment', 'submitted_on', 'grade')
    search_fields = ('assessment__name', 'student__username')
    readonly_fields = ('submitted_on',)
    ordering = ('-submitted_on',)
    change_list_template = "admin/change_list_filter_sidebar.html"  # Sidebar filters template

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Submission, SubmissionAdmin)

from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Content, Assignment

class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = ('title', 'due_date')  # Removed 'position' since it's not a field in the Assignment model
    classes = ('grp-collapse grp-open',)  # Collapsible inline with open state
    extra = 1  # Number of empty forms

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content Information', {
            'fields': ('title', 'description'),
        }),
        ('Additional Information', {
            'classes': ('grp-collapse grp-closed',),  # Collapsible fieldset with closed state
            'fields': ('created_at',),
        }),
    )
    inlines = [AssignmentInline]
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/path/to/your/tinymce_setup.js',
        ]

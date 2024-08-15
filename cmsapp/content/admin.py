from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Content, Assignment, ContentVersion, Interaction, ContentAccess, Tag, ContentAnalytics

class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = ('title', 'due_date')
    classes = ('grp-collapse grp-open',)
    extra = 1

class ContentVersionInline(admin.TabularInline):
    model = ContentVersion
    fields = ('version_number', 'file', 'url', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 1

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content Information', {
            'fields': ('title', 'description', 'content_type', 'file', 'url', 'course', 'unit'),
        }),
        ('Additional Information', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('created_at', 'version', 'tags', 'released_at'),
        }),
    )
    inlines = [ContentVersionInline, AssignmentInline]
    list_display = ('title', 'content_type', 'course', 'created_at', 'is_released')  # 'is_released' now correctly references the method
    search_fields = ('title', 'description', 'course__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/path/to/your/tinymce_setup.js',
        ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(ContentAccess)
class ContentAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'access_date', 'completed')
    search_fields = ('user__username', 'content__title')

@admin.register(ContentAnalytics)
class ContentAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'view_count', 'last_viewed')
    search_fields = ('content__title', 'user__username')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'interaction_type', 'timestamp')
    search_fields = ('user__username', 'content__title', 'interaction_type')

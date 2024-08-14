from django.contrib import admin
from .models import Course, Unit, Lesson, LessonPlan, StudyMaterial, Enrollment, Progress, Semester  
from content.models import Content
class StudyMaterialInline(admin.TabularInline):
    model = StudyMaterial
    extra = 1
    classes = ('grp-collapse grp-open',)
    sortable_field_name = "id"  # Enable sorting for study materials inline

class LessonPlanInline(admin.StackedInline):
    model = LessonPlan
    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    sortable_field_name = "id"  # Enable sorting for lessons inline

class ContentInline(admin.TabularInline):
    model = Lesson.contents.through  # Many-to-many relationship between Lesson and Content
    extra = 1
    classes = ('grp-collapse grp-open',)
    sortable_field_name = "id"  # Enable sorting for contents inline

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'required_for_completion')
    search_fields = ('name',)
    inlines = [LessonInline]  # Show Lessons inline in the Unit admin

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'schedule_date', 'start_time', 'end_time')
    search_fields = ('title', 'description')
    filter_horizontal = ('contents',)  # Allows for easy selection of content in admin
    inlines = [StudyMaterialInline, LessonPlanInline]  # Show Study Materials and Lesson Plan inline in the Lesson admin
    fieldsets = (
        (None, {
            'fields': ('title', 'unit', 'description', 'schedule_date', 'start_time', 'end_time'),
        }),
        ('Contents', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('contents',),
        }),
    )

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'start_date', 'end_date', 'instructor')
    search_fields = ('name', 'description')
    inlines = [LessonInline]  # Show Lessons inline in the Course admin
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'semester', 'instructor', 'start_date', 'end_date'),
        }),
        ('Units and Lessons', {
            'classes': ('grp-collapse grp-open',),
            'fields': (),
        }),
    )

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    search_fields = ('student__username', 'course__name')
    list_filter = ('course',)

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'date_completed')
    search_fields = ('student__username', 'lesson__title')
    list_filter = ('completed',)

# Registering models with custom admin
admin.site.register(Semester)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Progress, ProgressAdmin)

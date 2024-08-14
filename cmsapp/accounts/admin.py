from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile
from grappelli.forms import GrappelliSortableHiddenMixin

class UserProfileInline(GrappelliSortableHiddenMixin, admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = (UserProfileInline,)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'bio', 'is_student', 'is_instructor'),
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_instructor'),
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_student', 'is_instructor')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    # Relationships to other apps
    courses = models.ManyToManyField('courses.Course', related_name='students', blank=True)
    assessments = models.ManyToManyField('assessments.Assessment', related_name='students', blank=True)

    # Add unique related_name attributes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change this line
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change this line
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='user',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def is_student_user(self):
        return self.is_student

    def is_instructor_user(self):
        return self.is_instructor

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['username']

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()




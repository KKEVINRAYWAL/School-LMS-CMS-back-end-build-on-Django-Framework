"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'cmsapp.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for the CMS application.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # Group for Administration and Applications
        self.children.append(modules.Group(
            _('Group: Administration & Applications'),
            column=1,
            collapsible=True,
            children=[
                modules.AppList(
                    _('Administration'),
                    column=1,
                    collapsible=True,
                    models=('django.contrib.*',),
                ),
                modules.AppList(
                    _('User Management'),
                    column=1,
                    collapsible=True,
                    models=('accounts.*',),
                ),
                modules.AppList(
                    _('Course Management'),
                    column=1,
                    collapsible=True,
                    models=('courses.*', 'enrollments.*'),
                ),
                modules.AppList(
                    _('Assessment Management'),
                    column=1,
                    collapsible=True,
                    models=('assessments.*',),
                ),
                modules.AppList(
                    _('Content Management'),
                    column=1,
                    collapsible=True,
                    models=('content.*',),
                ),
            ]
        ))

        # Recent Actions Module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            collapsible=True,
            column=2,
        ))

        # Custom Modules for specific statistics and management
        self.children.append(modules.LinkList(
            _('Quick Links'),
            column=2,
            children=[
                {
                    'title': _('Manage Users'),
                    'url': reverse('admin:accounts_customuser_changelist'),
                    'external': False,
                },
                {
                    'title': _('Manage Courses'),
                    'url': reverse('admin:courses_course_changelist'),
                    'external': False,
                },
                {
                    'title': _('Manage Assessments'),
                    'url': reverse('admin:assessments_assessment_changelist'),
                    'external': False,
                },
                {
                    'title': _('Manage Content'),
                    'url': reverse('admin:content_content_changelist'),
                    'external': False,
                },
                {
                    'title': _('Enrollment Reports'),
                    'url': reverse('admin:enrollments_enrollment_changelist'),
                    'external': False,
                },
            ]
        ))

        # Custom Module for User Statistics
        self.children.append(modules.ModelList(
            _('User Statistics'),
            column=2,
            collapsible=True,
            models=('accounts.CustomUser', 'accounts.UserProfile'),
        ))

        # Static Content Module
        self.children.append(modules.LinkList(
            _('CMS Documentation'),
            column=3,
            children=[
                {
                    'title': _('User Guide'),
                    'url': 'https://example.com/user_guide',
                    'external': True,
                },
                {
                    'title': _('Developer Documentation'),
                    'url': 'https://example.com/developer_docs',
                    'external': True,
                },
            ]
        ))
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
        # A simple module to display some statistics
        self.children.append(modules.Feed(
            _('Latest News'),
            column=3,
            feed_url='https://example.com/rss',
            limit=5
        ))
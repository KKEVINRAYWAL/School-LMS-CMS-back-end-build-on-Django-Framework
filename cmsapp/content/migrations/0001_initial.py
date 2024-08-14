# Generated by Django 5.0.8 on 2024-08-14 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Assignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("due_date", models.DateTimeField()),
                ("file_submission", models.BooleanField(default=True)),
                ("text_submission", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "content_type",
                    models.CharField(
                        choices=[
                            ("video", "Video"),
                            ("pdf", "PDF"),
                            ("text", "Text"),
                            ("slide", "Slide"),
                            ("quiz", "Quiz"),
                            ("link", "Link"),
                            ("interactive", "Interactive"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="course_content/"
                    ),
                ),
                ("url", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("version", models.IntegerField(default=1)),
                ("released_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ContentAccess",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("access_date", models.DateTimeField(auto_now_add=True)),
                ("completed", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="ContentAnalytics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("view_count", models.IntegerField(default=0)),
                ("last_viewed", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ContentVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("version_number", models.IntegerField()),
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="content_versions/"
                    ),
                ),
                ("url", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Interaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "interaction_type",
                    models.CharField(
                        choices=[
                            ("view", "View"),
                            ("download", "Download"),
                            ("like", "Like"),
                            ("comment", "Comment"),
                        ],
                        max_length=50,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
    ]

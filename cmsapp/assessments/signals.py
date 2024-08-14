from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission

@receiver(post_save, sender=Submission)
def update_assessment_stats(sender, instance, **kwargs):
    # Trigger re-calculation of stats when a new submission is saved
    instance.assessment.save()

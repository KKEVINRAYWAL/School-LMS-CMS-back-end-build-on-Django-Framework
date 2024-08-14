from django.apps import AppConfig

class AssessmentsConfig(AppConfig):
    name = 'assessments'

    def ready(self):
        import assessments.signals  # Import the signals module to ensure signals are registered

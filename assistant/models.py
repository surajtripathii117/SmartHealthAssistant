from django.db import models


class SymptomCheck(models.Model):
    """
    Model representing a user's symptom analysis check.
    Stores the entered symptoms, the analyzed result summary,
    and the timestamp when the check was performed.
    """
    symptoms = models.TextField(
        help_text="Comma-separated or listed symptoms entered by user"
    )
    result = models.TextField(
        help_text="Summary of analysis outcome (condition, match score, or emergency status)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the symptom check was conducted"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Symptom Check'
        verbose_name_plural = 'Symptom Checks'

    def __str__(self):
        created_str = self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else 'Unknown date'
        return f"Check #{self.pk} - {created_str} - {self.result[:50]}"

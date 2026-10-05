from django.contrib import admin
from .models import SymptomCheck


@admin.register(SymptomCheck)
class SymptomCheckAdmin(admin.ModelAdmin):
    """
    Admin configuration for SymptomCheck model.
    Provides list display, search capabilities, filters, and read-only timestamps.
    """
    list_display = ('id', 'short_symptoms', 'result', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('symptoms', 'result')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 25

    def short_symptoms(self, obj):
        """Truncate long symptoms strings for neat tabular display."""
        if len(obj.symptoms) > 60:
            return obj.symptoms[:57] + '...'
        return obj.symptoms
    short_symptoms.short_description = 'Symptoms'

from django import forms
from .symptom_data import PREDEFINED_SYMPTOMS


class SymptomForm(forms.Form):
    """
    Form for entering and selecting symptoms.
    Provides:
    1. Selectable symptom checkboxes (from standard catalog)
    2. Free text input for custom or comma-separated symptoms
    """
    selected_symptoms = forms.MultipleChoiceField(
        choices=[(sym, sym) for sym in PREDEFINED_SYMPTOMS],
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        ),
        required=False,
        label="Select Common Symptoms"
    )
    custom_symptoms = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g., Fever, Cough, Headache (comma separated)',
                'id': 'custom_symptoms_input'
            }
        ),
        required=False,
        label="Or Type Symptoms",
        help_text="Separate multiple symptoms with commas or type any additional symptoms here."
    )

    def clean(self):
        cleaned_data = super().clean()
        selected = cleaned_data.get('selected_symptoms') or []
        custom = cleaned_data.get('custom_symptoms') or ''

        # Parse custom symptoms
        custom_list = [s.strip() for s in custom.split(',') if s.strip()]

        combined = list(selected) + custom_list

        if not combined:
            raise forms.ValidationError(
                "Please select at least one symptom from the list or enter your symptoms in the text box."
            )

        cleaned_data['all_symptoms'] = combined
        return cleaned_data


class ContactForm(forms.Form):
    """
    Academic contact form with client and server-side validation.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }
        ),
        label="Your Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': True
            }
        ),
        label="Email Address"
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your message or inquiry here...',
                'required': True
            }
        ),
        label="Your Message"
    )

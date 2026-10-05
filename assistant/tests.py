from django.test import TestCase, Client
from django.urls import reverse
from assistant.models import SymptomCheck
from assistant.symptom_data import (
    analyze_symptoms,
    check_emergency_symptoms,
    PREDEFINED_SYMPTOMS,
    CONDITIONS_DATABASE,
)


class SymptomDataLogicTests(TestCase):
    """
    Test suite for rule-based matching engine and emergency symptom detection.
    """

    def test_emergency_symptom_detection_exact(self):
        """Emergency symptoms should be identified accurately."""
        is_emer, detected, msg = check_emergency_symptoms(["Severe chest pain"])
        self.assertTrue(is_emer)
        self.assertIn("Severe chest pain", detected)
        self.assertIn("emergency medical care", msg.lower())

    def test_emergency_symptom_detection_case_insensitive(self):
        """Emergency detection should be case-insensitive and handle variations."""
        is_emer, detected, msg = check_emergency_symptoms(["difficulty breathing", "cough"])
        self.assertTrue(is_emer)
        self.assertTrue(len(detected) > 0)

    def test_emergency_analysis_bypasses_routine_conditions(self):
        """Emergency findings must immediately return emergency flag and empty condition diagnoses."""
        analysis = analyze_symptoms(["Severe chest pain", "Fever"])
        self.assertTrue(analysis["is_emergency"])
        self.assertEqual(analysis["emergency_title"], "Seek Emergency Medical Care")
        self.assertEqual(len(analysis["results"]), 0)

    def test_valid_symptom_matching_cold(self):
        """Matching symptoms should calculate positive match scores for Cold."""
        analysis = analyze_symptoms(["Runny nose", "Sneezing", "Sore throat"])
        self.assertFalse(analysis["is_emergency"])
        self.assertTrue(len(analysis["results"]) > 0)
        
        # Common Cold should be among top results
        condition_names = [r["condition"] for r in analysis["results"]]
        self.assertIn("Common Cold", condition_names)

        cold_res = next(r for r in analysis["results"] if r["condition"] == "Common Cold")
        self.assertGreater(cold_res["match_score"], 0)
        self.assertIn("Runny nose", cold_res["matching_symptoms"])

    def test_valid_symptom_matching_flu(self):
        """Flu symptoms should calculate accurate match score."""
        analysis = analyze_symptoms(["Fever", "Cough", "Body ache", "Fatigue"])
        self.assertFalse(analysis["is_emergency"])
        self.assertTrue(len(analysis["results"]) > 0)
        top_result = analysis["results"][0]
        self.assertEqual(top_result["condition"], "Flu (Influenza)")
        self.assertGreaterEqual(top_result["match_score"], 50.0)

    def test_empty_symptoms_analysis(self):
        """Empty input should yield zero results without errors."""
        analysis = analyze_symptoms([])
        self.assertFalse(analysis["is_emergency"])
        self.assertEqual(len(analysis["results"]), 0)
        self.assertEqual(analysis["total_user_symptoms"], 0)


class SymptomCheckModelTests(TestCase):
    """
    Test suite for SymptomCheck database model.
    """

    def test_symptom_check_creation_and_str(self):
        """Test creating a SymptomCheck record and checking string representation."""
        check = SymptomCheck.objects.create(
            symptoms="Fever, Cough, Headache",
            result="Flu (Influenza) (Match Score: 57.1%)"
        )
        self.assertIsNotNone(check.pk)
        self.assertIn("Check #", str(check))
        self.assertIn("Flu", str(check))

    def test_model_ordering(self):
        """Model should order latest checks first."""
        check1 = SymptomCheck.objects.create(symptoms="Fever", result="Check 1")
        check2 = SymptomCheck.objects.create(symptoms="Cough", result="Check 2")
        checks = list(SymptomCheck.objects.all())
        self.assertEqual(checks[0].pk, check2.pk)


class AssistantViewsTests(TestCase):
    """
    Test suite for views, URL routing, forms, and template rendering.
    """

    def setUp(self):
        self.client = Client()

    def test_homepage_view(self):
        """Homepage returns 200 OK and contains brand elements."""
        response = self.client.get(reverse('assistant:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SmartHealth")
        self.assertContains(response, "Understand Your Symptoms Better")
        self.assertContains(response, "Check Symptoms")

    def test_about_page_view(self):
        """About page returns 200 OK and contains tech stack details."""
        response = self.client.get(reverse('assistant:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About SmartHealth Assistant")
        self.assertContains(response, "MCA Academic Project")
        self.assertContains(response, "Django")
        self.assertContains(response, "SQLite")

    def test_valid_symptom_submission(self):
        """Submitting valid symptoms creates DB record and redirects to result page."""
        initial_count = SymptomCheck.objects.count()
        response = self.client.post(reverse('assistant:checker'), {
            'selected_symptoms': ['Fever', 'Cough', 'Body ache'],
            'custom_symptoms': 'Fatigue',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('assistant:result'))
        self.assertEqual(SymptomCheck.objects.count(), initial_count + 1)

        # Check result page rendering
        result_response = self.client.get(reverse('assistant:result'))
        self.assertEqual(result_response.status_code, 200)
        self.assertContains(result_response, "Analysis Results")
        self.assertContains(result_response, "Symptom Match Score")
        self.assertContains(result_response, "Important Medical Disclaimer")

    def test_empty_symptom_submission_handled(self):
        """Submitting empty symptoms triggers form validation error and does not create DB record."""
        initial_count = SymptomCheck.objects.count()
        response = self.client.post(reverse('assistant:checker'), {
            'selected_symptoms': [],
            'custom_symptoms': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SymptomCheck.objects.count(), initial_count)
        self.assertContains(response, "Please select at least one symptom")

    def test_emergency_symptom_submission(self):
        """Emergency symptom submission renders emergency warning and disclaimer."""
        response = self.client.post(reverse('assistant:checker'), {
            'custom_symptoms': 'Severe chest pain, Difficulty breathing',
        })
        self.assertEqual(response.status_code, 302)
        
        result_response = self.client.get(reverse('assistant:result'))
        self.assertEqual(result_response.status_code, 200)
        self.assertContains(result_response, "Seek Emergency Medical Care")
        self.assertContains(result_response, "Some symptoms may require immediate medical attention")

    def test_history_page_view(self):
        """History page lists past checks."""
        SymptomCheck.objects.create(
            symptoms="Headache, Dizziness",
            result="Migraine (Match Score: 50.0%)"
        )
        response = self.client.get(reverse('assistant:history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Symptom Check History")
        self.assertContains(response, "Headache, Dizziness")
        self.assertContains(response, "Migraine")

    def test_history_detail_view(self):
        """Accessing a historical check by ID shows the detail analysis."""
        check = SymptomCheck.objects.create(
            symptoms="Headache, Fatigue",
            result="Tension Headache"
        )
        response = self.client.get(reverse('assistant:history_detail', args=[check.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Analysis Results")
        self.assertContains(response, "Historical check conducted on")

    def test_contact_form_submission(self):
        """Contact form validates and returns friendly academic success message."""
        response = self.client.post(reverse('assistant:index'), {
            'contact_submit': '1',
            'name': 'MCA Student',
            'email': 'student@example.edu',
            'message': 'Testing the academic contact form feedback mechanism.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('assistant:index'))

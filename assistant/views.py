from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SymptomForm, ContactForm
from .models import SymptomCheck
from .symptom_data import PREDEFINED_SYMPTOMS, analyze_symptoms


def index_view(request):
    """
    Renders the homepage containing the hero section, quick overview,
    features, and the academic contact section.
    """
    contact_form = ContactForm()
    if request.method == 'POST' and 'contact_submit' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            messages.success(
                request,
                f"Thank you, {name}! Your message has been received. "
                "(Academic demonstration: Message successfully recorded.)"
            )
            return redirect('assistant:index')
        else:
            messages.error(request, "Please correct the errors in the contact form.")

    return render(request, 'assistant/index.html', {
        'contact_form': contact_form,
        'symptoms_list': PREDEFINED_SYMPTOMS,
    })


def checker_view(request):
    """
    Renders and processes the symptom checker page.
    Accepts checkbox selections and custom text input.
    """
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            all_symptoms = form.cleaned_data['all_symptoms']
            
            # Perform rule-based analysis
            analysis = analyze_symptoms(all_symptoms)

            # Build result summary for database persistence
            if analysis['is_emergency']:
                result_summary = f"EMERGENCY ALERT: {', '.join(analysis['emergency_symptoms'])}"
            elif analysis['results']:
                top_match = analysis['results'][0]
                result_summary = f"{top_match['condition']} (Match Score: {top_match['match_score']}%)"
            else:
                result_summary = "No matching condition found in knowledge base"

            # Save check to SQLite database
            symptom_record = SymptomCheck.objects.create(
                symptoms=", ".join(all_symptoms),
                result=result_summary
            )

            # Store the current analysis result in session for the result page
            request.session['current_analysis'] = analysis
            request.session['current_check_id'] = symptom_record.id

            return redirect('assistant:result')
        else:
            messages.error(
                request,
                "Please select at least one symptom or type symptoms separated by commas."
            )
    else:
        form = SymptomForm()

    return render(request, 'assistant/index.html', {
        'form': form,
        'contact_form': ContactForm(),
        'symptoms_list': PREDEFINED_SYMPTOMS,
        'scroll_to_checker': True if request.method == 'POST' else False,
    })


def result_view(request):
    """
    Displays the analysis outcome: emergency alerts or matched conditions,
    percentages labeled strictly as 'Symptom Match Score', precautions,
    next steps, and mandatory medical disclaimers.
    """
    analysis = request.session.get('current_analysis')
    check_id = request.session.get('current_check_id')

    if not analysis:
        messages.warning(request, "No analysis found. Please enter your symptoms to run a check.")
        return redirect('assistant:index')

    return render(request, 'assistant/result.html', {
        'analysis': analysis,
        'check_id': check_id,
    })


def history_view(request):
    """
    Displays the chronological log of previous symptom checks retrieved from SQLite.
    """
    checks = SymptomCheck.objects.all().order_by('-created_at')
    return render(request, 'assistant/history.html', {
        'checks': checks,
    })


def history_detail_view(request, check_id):
    """
    Allows user to inspect or re-run a previous symptom check from history.
    """
    record = get_object_or_404(SymptomCheck, pk=check_id)
    # Parse symptoms back into list and re-run analysis
    symptoms_list = [s.strip() for s in record.symptoms.split(',') if s.strip()]
    analysis = analyze_symptoms(symptoms_list)

    return render(request, 'assistant/result.html', {
        'analysis': analysis,
        'check_id': record.id,
        'is_historical': True,
        'recorded_at': record.created_at,
    })


def about_view(request):
    """
    Renders the academic About page detailing project scope, technologies,
    and rule-based architecture.
    """
    return render(request, 'assistant/about.html')

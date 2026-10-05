/**
 * SmartHealth Assistant - Interactive UI and Validation Script
 * MCA Academic Project
 */

document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const symptomForm = document.getElementById('symptomForm');
    const customSymptomsInput = document.getElementById('custom_symptoms_input');
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    const countBadge = document.getElementById('selectedCountBadge');
    const clearBtn = document.getElementById('clearSymptomsBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeSpinner = document.getElementById('analyzeSpinner');
    const analyzeIcon = document.getElementById('analyzeIcon');

    // 1. Update selection count and toggle visual highlights
    function updateSelectionState() {
        let selectedCount = 0;

        checkboxes.forEach(function (cb) {
            const card = cb.closest('.symptom-checkbox-card');
            if (cb.checked) {
                selectedCount++;
                if (card) card.classList.add('is-selected');
            } else {
                if (card) card.classList.remove('is-selected');
            }
        });

        // Check typed symptoms count
        if (customSymptomsInput) {
            const typed = customSymptomsInput.value.trim();
            if (typed.length > 0) {
                const typedItems = typed.split(',').filter(function (s) {
                    return s.trim().length > 0;
                });
                selectedCount += typedItems.length;
            }
        }

        if (countBadge) {
            countBadge.textContent = selectedCount + ' symptom' + (selectedCount === 1 ? '' : 's') + ' selected';
            if (selectedCount > 0) {
                countBadge.classList.remove('bg-secondary');
                countBadge.classList.add('bg-primary');
            } else {
                countBadge.classList.remove('bg-primary');
                countBadge.classList.add('bg-secondary');
            }
        }
    }

    // Attach change event listeners to checkboxes
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', updateSelectionState);

        // Also allow clicking anywhere on the card to toggle
        const card = checkbox.closest('.symptom-checkbox-card');
        if (card) {
            card.addEventListener('click', function (e) {
                if (e.target !== checkbox && e.target.tagName !== 'LABEL') {
                    checkbox.checked = !checkbox.checked;
                    updateSelectionState();
                }
            });
        }
    });

    // Attach input event to custom symptoms textbox
    if (customSymptomsInput) {
        customSymptomsInput.addEventListener('input', updateSelectionState);
    }

    // Initial check on load
    updateSelectionState();

    // 2. Clear Symptoms Button with confirmation
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            let hasAny = false;
            checkboxes.forEach(function (cb) {
                if (cb.checked) hasAny = true;
            });
            if (customSymptomsInput && customSymptomsInput.value.trim().length > 0) {
                hasAny = true;
            }

            if (!hasAny) {
                alert('No symptoms are currently selected or entered.');
                return;
            }

            const confirmed = window.confirm('Are you sure you want to clear all selected and typed symptoms?');
            if (confirmed) {
                checkboxes.forEach(function (cb) {
                    cb.checked = false;
                });
                if (customSymptomsInput) {
                    customSymptomsInput.value = '';
                }
                updateSelectionState();
            }
        });
    }

    // 3. Form Validation and Loading Indicator during Analysis
    if (symptomForm) {
        symptomForm.addEventListener('submit', function (e) {
            let hasSelectedCheckbox = false;
            checkboxes.forEach(function (cb) {
                if (cb.checked) hasSelectedCheckbox = true;
            });

            let hasTypedSymptoms = false;
            if (customSymptomsInput && customSymptomsInput.value.trim().length > 0) {
                hasTypedSymptoms = true;
            }

            // Ensure at least one symptom is provided
            if (!hasSelectedCheckbox && !hasTypedSymptoms) {
                e.preventDefault();
                alert('Please select at least one symptom from the list or type your symptoms into the search box before analyzing.');
                if (customSymptomsInput) {
                    customSymptomsInput.focus();
                }
                return false;
            }

            // Display loading indicator
            if (analyzeBtn) {
                analyzeBtn.disabled = true;
                if (analyzeSpinner) analyzeSpinner.classList.remove('d-none');
                if (analyzeIcon) analyzeIcon.classList.add('d-none');
                analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing Symptoms...';
            }

            // Allow natural form submission to proceed
            return true;
        });
    }

    // Smooth scroll for hash links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId.length > 1) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

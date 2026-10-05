# SmartHealthAssistant

**MCA Academic Web Application Project**  
*Intelligent Companion for Preliminary Health Information*

---

## 1. Project Overview

**SmartHealthAssistant** is a complete, full-stack web application designed for an MCA-level (Master of Computer Applications) academic curriculum. The platform allows users to input their observed symptoms—via intuitive checkboxes and free-text inputs—and receive preliminary health condition matches, comprehensive explanations, precautionary advice, and suggested clinical next steps.

The system incorporates a transparent **rule-based inference engine** with a dedicated **emergency symptom detection mechanism** to safeguard users against critical conditions.

> [!IMPORTANT]
> **Mandatory Medical Disclaimer:**  
> This system is strictly an educational and informational tool. It is **NOT** a certified medical diagnosis system, medical device, or doctor replacement. Users must always seek professional medical evaluation from a qualified healthcare practitioner.

---

## 2. Key Features

- **Responsive Healthcare UI:** Built with Bootstrap 5 and clean CSS3, fully responsive across mobile phones, tablets, and desktop workstations.
- **Dual Symptom Entry Mode:**
  - *Method 1:* Free-text input with comma-separated parsing.
  - *Method 2:* Multi-select interactive checkboxes with live counter badges.
- **Rule-Based Inference Engine:**
  - Evaluates symptom overlap against verified condition profiles (Common Cold, Flu, Migraine, Tension Headache, Food Poisoning, Gastroenteritis, Dehydration, Allergic Rhinitis).
  - Calculates a precise **Symptom Match Score (%)**, explicitly labeled to avoid confusing match scores with disease probabilities.
- **Emergency Warning System:**
  - Detects red-flag symptoms such as severe chest pain, difficulty breathing, severe bleeding, stroke symptoms, or loss of consciousness.
  - Instantly bypasses standard condition matching to display high-priority emergency alerts and local hotline guidance.
- **Persistent Evaluation History:**
  - Persists all symptom checks in an SQLite database using Django's ORM.
  - Provides a chronological history view allowing users to inspect past evaluation records.
- **Django Administration Suite:**
  - Pre-configured `admin.py` with custom list displays, search filtering, and read-only timestamps.
- **Contact & Feedback Module:**
  - Academic feedback form with client and server-side validation.
- **Automated Test Suite:**
  - Comprehensive unit and integration tests verifying views, models, emergency filters, and scoring logic.

---

## 3. Technology Stack

| Layer | Technology | Details |
|---|---|---|
| **Backend Framework** | Django 5.x / 6.x | Python web framework (MTV architecture) |
| **Programming Language** | Python 3.10+ | Core language for rule-based engine and views |
| **Database** | SQLite 3 | Zero-configuration relational database |
| **Frontend Framework** | Bootstrap 5.3.3 | Responsive grid, cards, badges, and modals |
| **Icons** | Bootstrap Icons 1.11 | High-definition healthcare icons |
| **Styling** | Custom CSS3 | Modern healthcare palette, cards, and animations |
| **Client Scripting** | Vanilla JavaScript | Dynamic counters, loading states, and validation |
| **Testing** | Django Test Framework | `django.test.TestCase` covering all layers |

---

## 4. Project Directory Structure

```text
SmartHealthAssistant/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── smarthealth/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── assistant/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── forms.py
    ├── symptom_data.py
    ├── tests.py
    │
    ├── templates/
    │   └── assistant/
    │       ├── base.html
    │       ├── index.html
    │       ├── result.html
    │       ├── about.html
    │       └── history.html
    │
    └── static/
        └── assistant/
            ├── css/
            │   └── style.css
            └── js/
                └── script.js
```

---

## 5. Development & VS Code Setup (Windows)

Follow these exact steps in your Visual Studio Code terminal (PowerShell):

### Step 1: Open the Project in VS Code
Open VS Code, navigate to `File` > `Open Folder...`, and select the `SmartHealthAssistant` directory.

### Step 2: Create a Python Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(If PowerShell displays a script execution policy restriction, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then run the command above).*

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Apply Database Migrations
Create the SQLite database schema:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create an Administrator Account
Create a superuser to access the Django Admin portal:
```powershell
python manage.py createsuperuser
```
Follow the interactive prompts to set an admin username, email, and password.

### Step 7: Run the Development Server
```powershell
python manage.py runserver
```

Once running, access the application in your browser:
- **Application URL:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin Portal:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 6. Running the Test Suite

Execute the automated test suite with the following command:

```powershell
python manage.py test
```

Expected result: All tests pass with `OK`.

---

## 7. Knowledge Base & Symptom Matching Logic

The knowledge base in [`assistant/symptom_data.py`](assistant/symptom_data.py) implements rule-based reasoning:

### 1. Emergency Detection
Input symptoms are sanitized and compared against critical life-safety conditions:
- *Severe chest pain*
- *Difficulty breathing*
- *Severe bleeding*
- *Loss of consciousness*
- *Stroke-like symptoms*
- *Severe allergic reaction*

If an emergency indicator is matched, standard condition scoring is bypassed immediately to prevent any false reassurance.

### 2. Symptom Match Score Formula
For regular evaluations, each condition profile $C$ in the knowledge base has a set of defining symptoms $S_C$. If the user enters symptoms $U$, the matching subset is:

$$M = S_C \cap U$$

The **Symptom Match Score** is calculated as:

$$\text{Match Score (\%)} = \left(\frac{|M|}{|S_C|}\right) \times 100$$

- Conditions with at least one matching symptom are ranked in descending order of their match score.
- The user is shown:
  - Condition name
  - Symptom match score percentage
  - Verified matching symptoms ($\checkmark$)
  - General clinical overview
  - Recommended precautions
  - Suggested next steps

---

## 8. Security & Production Deployment Considerations

- **DEBUG Mode:** In [`smarthealth/settings.py`](smarthealth/settings.py), `DEBUG = True` is set for development. For any production deployment, `DEBUG` must be set to `False` and `ALLOWED_HOSTS` configured with your domain.
- **CSRF Protection:** All forms include Django's `{% csrf_token %}` tag to protect against Cross-Site Request Forgery.
- **ORM & Injection Defense:** No raw SQL queries are used. All database transactions use the Django ORM to protect against SQL injection.
- **Input Sanitization:** User text input is stripped, normalized, and validated both client-side (JavaScript) and server-side (Django Forms).

---

## 9. Academic Limitations & Ethics

1. **Heuristic Limitation:** Symptom matching does not replace laboratory diagnostics, clinical imaging, or patient physical examination.
2. **Non-Diagnostic:** Scores signify textual alignment with condition profiles, not statistical epidemiology.
3. **Emergency Priority:** Critical symptoms require rapid physical triage beyond the scope of any digital assistant.

---

## 10. License & Credits

Developed as an MCA Academic Project demonstrating web engineering, software architecture, and preliminary health information systems using Python, Django, SQLite, and Bootstrap 5.

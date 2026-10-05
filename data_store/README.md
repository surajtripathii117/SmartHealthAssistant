# SmartHealthAssistant - Data Store Directory

This folder (`data_store/`) contains all persistent data, knowledge base specifications, sample fixtures, and data export tools for the project.

---

## Files in this Directory

| File | Description | Format |
|---|---|---|
| `conditions_knowledge_base.json` | Complete knowledge base of all 8 health conditions, symptom mappings, precautions, and next steps | JSON |
| `emergency_symptoms.json` | High-priority red-flag symptoms catalog, clinical risk factors, and emergency hotlines | JSON |
| `sample_patient_checks.json` | Django fixture with realistic sample symptom evaluation records | JSON |
| `export_data.py` | Standalone Python utility to export live SQLite records to JSON & CSV | Python Script |
| `exported_symptom_checks.json` | Live export of all evaluations recorded in SQLite | JSON |
| `exported_symptom_checks.csv` | Tabular export of all evaluations for Excel / analysis | CSV |

---

## How to Load Sample Data into SQLite Database

To populate your database with sample evaluation history, run:

```powershell
python manage.py loaddata data_store/sample_patient_checks.json
```

---

## How to Export Live Database Records

Whenever you conduct symptom checks through the web application, you can export all saved records into this folder by running:

```powershell
python data_store/export_data.py
```

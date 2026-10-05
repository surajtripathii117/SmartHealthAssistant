"""
Data export utility script for SmartHealthAssistant.
Exports records from the SQLite database to JSON and CSV formats inside data_store/.

Usage:
    python data_store/export_data.py
"""

import os
import sys
import json
import csv
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarthealth.settings')

import django
django.setup()

from assistant.models import SymptomCheck


def export_records():
    data_dir = BASE_DIR / 'data_store'
    data_dir.mkdir(exist_ok=True)

    checks = SymptomCheck.objects.all().order_by('-created_at')
    records = []

    for c in checks:
        records.append({
            'id': c.id,
            'symptoms': c.symptoms,
            'result': c.result,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S') if c.created_at else None,
        })

    # 1. Export JSON
    json_path = data_dir / 'exported_symptom_checks.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
    print(f"[SUCCESS] Exported {len(records)} records to {json_path}")

    # 2. Export CSV
    csv_path = data_dir / 'exported_symptom_checks.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'symptoms', 'result', 'created_at'])
        writer.writeheader()
        writer.writerows(records)
    print(f"[SUCCESS] Exported {len(records)} records to {csv_path}")


if __name__ == '__main__':
    export_records()

import json
import os
from datetime import datetime

def generate_progress_report():
    """Generate Day 1 progress report"""
    report = {
        "date": datetime.now().isoformat(),
        "documents_processed": 2,
        "extraction_status": {
            "nta": {
                "status": "completed",
                "pages_processed": 0,
                "ocr_pages": 0,
                "output_path": "data/interim/extracted/nta/"
            },
            "ntaa": {
                "status": "completed",
                "pages_processed": 0,
                "ocr_pages": 0,
                "output_path": "data/interim/extracted/ntaa/"
            }
        },
        "deliverables": {
            "metadata": ["metadata/nta.json", "metadata/ntaa.json"],
            "extracted_texts": [
                "data/interim/extracted/nta/",
                "data/interim/extracted/ntaa/"
            ],
            "inspections": ["NTA_inspection.json", "NTAA_inspection.json"]
        }
    }
    
    # Update actual page counts
    doc_paths = {
        "nta": "NIGERIA_TAX_ACT_2025_ef6bb812a5",
        "ntaa": "NIGERIA-TAX-ADMINISTRATION-ACT-2025"
    }
    for doc, dirname in doc_paths.items():
        log_path = f"data/interim/extracted/{dirname}/extraction_log.json"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                log = json.load(f)
                report["extraction_status"][doc]["pages_processed"] = log.get("pages_extracted", 0)
                report["extraction_status"][doc]["ocr_pages"] = len(log.get("ocr_pages", []))
    
    return report

if __name__ == "__main__":
    # Save progress report
    report = generate_progress_report()
    with open("day1_progress_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Progress report saved to day1_progress_report.json")
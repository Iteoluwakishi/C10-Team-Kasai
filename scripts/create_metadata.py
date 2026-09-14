import os
import json
from datetime import datetime
from pathlib import Path

def create_metadata(pdf_path, extracted_text, inspection_data):
    """Create comprehensive metadata for the document"""
    
    # Detect extraction methods used
    extraction_methods = {}
    for page_num, data in extracted_text.items():
        method = data.get("method", "unknown")
        extraction_methods[page_num] = method
    
    # Determine extraction types
    methods_used = list(set(extraction_methods.values()))
    
    metadata = {
        "document_id": Path(pdf_path).stem.lower().replace(" ", "_"),
        "title": Path(pdf_path).stem.replace("_", " "),
        "document_type": "Act" if "Act" in Path(pdf_path).stem else "Regulation",
        "status": "active",
        "effective_date": "2024-01-01",  # Adjust based on actual date
        "source": str(pdf_path),
        "page_count": len(extracted_text),
        "extraction_method": methods_used,
        "extraction_date": datetime.now().isoformat(),
        "metadata_version": "1.0",
        "ocr_required": "ocr" in methods_used,
        "ocr_pages": [p for p, m in extraction_methods.items() if m == "ocr"],
        "page_extraction_summary": {
            "total_pages": len(extracted_text),
            "pymupdf_pages": len([p for p, m in extraction_methods.items() if m == "pymupdf"]),
            "pdfplumber_pages": len([p for p, m in extraction_methods.items() if m == "pdfplumber"]),
            "ocr_pages": len([p for p, m in extraction_methods.items() if m == "ocr"])
        },
        "inspection_reference": inspection_data.get("inspection_date", ""),
        "processing_notes": "Extracted using automated pipeline with fallback to pdfplumber and OCR"
    }
    
    # Add legal structure placeholders
    metadata["legal_structure"] = {
        "chapters": [],  # To be populated during content analysis
        "sections": [],  # To be populated during content analysis
        "schedules": []  # To be populated during content analysis
    }
    
    return metadata

if __name__ == "__main__":
    # Example usage:
    # # Generate metadata for NTA
    # nta_metadata = create_metadata(
    #     "path/to/Nigeria_Tax_Act.pdf",
    #     extracted_text, # Needs to be defined or loaded
    #     nta_inspection  # Needs to be defined or loaded
    # )
    #
    # os.makedirs("metadata", exist_ok=True)
    # with open("metadata/nta.json", "w") as f:
    #     json.dump(nta_metadata, f, indent=2)
    pass
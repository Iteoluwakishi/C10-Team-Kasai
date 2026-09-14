import fitz  # PyMuPDF
import json
from datetime import datetime
from pathlib import Path

def inspect_pdf(pdf_path):
    """Inspect PDF file and return detailed metadata"""
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        
        inspection = {
            "file_name": Path(pdf_path).name,
            "file_path": str(pdf_path),
            "page_count": len(doc),
            "text_selectable": True,
            "scanned_pages": [],
            "tables_detected": [],
            "headers": [],
            "footers": [],
            "page_numbering": None,
            "ocr_required": False,
            "inspection_date": datetime.now().isoformat(),
            "issues": []
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Check if text is selectable
            text = page.get_text()
            if not text.strip():
                inspection["text_selectable"] = False
                inspection["scanned_pages"].append(page_num + 1)
                inspection["ocr_required"] = True
                continue
            
            # Detect tables (heuristic: look for repeated patterns or many tabs/spaces)
            if "\t" in text or "|" in text or text.count("  ") > 10:
                inspection["tables_detected"].append(page_num + 1)
            
            # Detect headers/footers (common patterns)
            lines = text.split('\n')
            if len(lines) > 3:
                # Check for potential headers (short text at top of page)
                if len(lines[0].strip()) < 100 and any(legal_term in lines[0].lower() for legal_term in ['act', 'law', 'chapter', 'section']):
                    inspection["headers"].append({"page": page_num + 1, "text": lines[0].strip()})
                
                # Check for potential footers (short text at bottom)
                if len(lines[-1].strip()) < 100:
                    inspection["footers"].append({"page": page_num + 1, "text": lines[-1].strip()})
            
            # Detect page numbering
            for line in lines:
                if any(str(num) in line for num in range(1, len(doc) + 1)) and len(line.strip()) < 10:
                    inspection["page_numbering"] = {"page": page_num + 1, "text": line.strip()}
                    break
        
        doc.close()
        return inspection
        
    except Exception as e:
        return {
            "error": str(e),
            "file_name": Path(pdf_path).name,
            "inspection_date": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import os
    # Default to known sources if run directly
    project_root = Path(__file__).parent.parent
    nta_path = project_root / "Sources" / "NIGERIA_TAX_ACT_2025_ef6bb812a5.pdf"
    ntaa_path = project_root / "Sources" / "NIGERIA-TAX-ADMINISTRATION-ACT-2025.pdf"
    
    if nta_path.exists():
        nta_inspection = inspect_pdf(str(nta_path))
        with open("NTA_inspection.json", "w") as f:
            json.dump(nta_inspection, f, indent=2)
            print(f"Saved NTA_inspection.json")
    
    if ntaa_path.exists():
        ntaa_inspection = inspect_pdf(str(ntaa_path))
        with open("NTAA_inspection.json", "w") as f:
            json.dump(ntaa_inspection, f, indent=2)
            print(f"Saved NTAA_inspection.json")
import os
from pathlib import Path
from extract import LegalDocumentExtractor

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        "data/interim/extracted/nta",
        "data/interim/extracted/ntaa",
        "metadata",
        "data/interim/ocr_outputs"  # For storing OCR intermediate files
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("Directory structure created successfully!")

# Main execution script
def main():
    """Complete Day 1 pipeline"""
    
    # Create directories
    create_directory_structure()
    
    project_root = Path(__file__).parent.parent
    
    # Process NTA
    nta_path = project_root / "Sources" / "NIGERIA_TAX_ACT_2025_ef6bb812a5.pdf"
    print("Processing Nigeria Tax Act...")
    if nta_path.exists():
        nta_extractor = LegalDocumentExtractor(str(nta_path))
        nta_text = nta_extractor.extract_all()
        nta_extractor.save_extracted_text(nta_text)
    else:
        print(f"File not found: {nta_path}")
    
    # Process NTAA
    ntaa_path = project_root / "Sources" / "NIGERIA-TAX-ADMINISTRATION-ACT-2025.pdf"
    print("Processing Nigeria Tax Administration Act...")
    if ntaa_path.exists():
        ntaa_extractor = LegalDocumentExtractor(str(ntaa_path))
        ntaa_text = ntaa_extractor.extract_all()
        ntaa_extractor.save_extracted_text(ntaa_text)
    else:
        print(f"File not found: {ntaa_path}")
    
    print("Day 1 tasks completed successfully!")

if __name__ == "__main__":
    main()
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import io
import json
from pathlib import Path
import os
from datetime import datetime

class LegalDocumentExtractor:
    def __init__(self, pdf_path, output_dir="data/interim/extracted"):
        self.pdf_path = pdf_path
        self.doc_name = Path(pdf_path).stem
        self.output_dir = Path(output_dir) / self.doc_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_pages = {}
        self.ocr_pages = []
        
    def extract_with_pymupdf(self):
        """Extract text using PyMuPDF"""
        doc = fitz.open(self.pdf_path)
        extracted_text = {}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            if text.strip():
                extracted_text[page_num + 1] = {
                    "text": text,
                    "method": "pymupdf",
                    "status": "success"
                }
            else:
                extracted_text[page_num + 1] = {
                    "text": "",
                    "method": "pymupdf",
                    "status": "failed"
                }
        
        doc.close()
        return extracted_text
    
    def extract_with_pdfplumber(self, pages_with_issues):
        """Extract text using pdfplumber for pages that failed with PyMuPDF"""
        extracted_text = {}
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num in pages_with_issues:
                if page_num <= len(pdf.pages):
                    page = pdf.pages[page_num - 1]
                    text = page.extract_text()
                    
                    if text and text.strip():
                        extracted_text[page_num] = {
                            "text": text,
                            "method": "pdfplumber",
                            "status": "success"
                        }
                    else:
                        extracted_text[page_num] = {
                            "text": "",
                            "method": "pdfplumber",
                            "status": "failed"
                        }
        
        return extracted_text
    
    def perform_ocr(self, pages_to_ocr):
        """Perform OCR on pages that failed text extraction"""
        doc = fitz.open(self.pdf_path)
        ocr_results = {}
        
        for page_num in pages_to_ocr:
            try:
                page = doc[page_num - 1]
                
                # Convert PDF page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                
                # Perform OCR
                ocr_text = pytesseract.image_to_string(image)
                
                if ocr_text.strip():
                    ocr_results[page_num] = {
                        "text": ocr_text,
                        "method": "ocr",
                        "status": "success",
                        "ocr_confidence": "estimated"  # Tesseract doesn't provide confidence easily
                    }
                    self.ocr_pages.append(page_num)
                else:
                    ocr_results[page_num] = {
                        "text": "",
                        "method": "ocr",
                        "status": "failed"
                    }
                    
            except Exception as e:
                ocr_results[page_num] = {
                    "text": "",
                    "method": "ocr",
                    "status": "failed",
                    "error": str(e)
                }
        
        doc.close()
        return ocr_results
    
    def extract_all(self):
        """Complete extraction pipeline"""
        # Step 1: Try PyMuPDF
        print(f"Extracting from {self.pdf_path} using PyMuPDF...")
        extracted = self.extract_with_pymupdf()
        
        # Identify pages that need alternative extraction
        failed_pages = [p for p, data in extracted.items() if data["status"] == "failed"]
        
        if failed_pages:
            # Step 2: Try pdfplumber on failed pages
            print(f"Trying pdfplumber for pages: {failed_pages}")
            pdfplumber_results = self.extract_with_pdfplumber(failed_pages)
            
            # Update extracted with pdfplumber results
            for page_num, data in pdfplumber_results.items():
                extracted[page_num] = data
            
            # Identify pages that still failed
            still_failed = [p for p, data in extracted.items() if data["status"] == "failed"]
            
            if still_failed:
                # Step 3: Perform OCR on remaining failed pages
                print(f"Performing OCR for pages: {still_failed}")
                ocr_results = self.perform_ocr(still_failed)
                
                # Update extracted with OCR results
                for page_num, data in ocr_results.items():
                    extracted[page_num] = data
        
        return extracted
    
    def save_extracted_text(self, extracted_text):
        """Save extracted text in the required format"""
        for page_num, data in extracted_text.items():
            output_file = self.output_dir / f"page_{page_num:04d}.txt"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"[PAGE {page_num}]\n\n")
                f.write(data["text"])
        
        # Also save the complete extracted text
        complete_text = ""
        for page_num in sorted(extracted_text.keys()):
            complete_text += f"[PAGE {page_num}]\n\n"
            complete_text += extracted_text[page_num]["text"]
            complete_text += "\n\n"
        
        with open(self.output_dir / "complete_text.txt", "w", encoding="utf-8") as f:
            f.write(complete_text)
        
        # Save extraction log
        log_data = {
            "file": str(self.pdf_path),
            "extraction_date": datetime.now().isoformat(),
            "pages_extracted": len(extracted_text),
            "ocr_pages": self.ocr_pages,
            "extraction_methods": {
                "pymupdf": len([p for p, d in extracted_text.items() if d["method"] == "pymupdf"]),
                "pdfplumber": len([p for p, d in extracted_text.items() if d["method"] == "pdfplumber"]),
                "ocr": len([p for p, d in extracted_text.items() if d["method"] == "ocr"])
            }
        }
        
        with open(self.output_dir / "extraction_log.json", "w") as f:
            json.dump(log_data, f, indent=2)

# Usage example
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if os.path.exists(pdf_path):
            print(f"Processing {pdf_path}...")
            extractor = LegalDocumentExtractor(pdf_path)
            extracted_text = extractor.extract_all()
            extractor.save_extracted_text(extracted_text)
            print("Done.")
        else:
            print(f"File not found: {pdf_path}")
    else:
        print("Usage: python extract.py <path_to_pdf>")
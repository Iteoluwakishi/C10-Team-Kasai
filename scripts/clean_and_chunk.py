import os
import re
import json
from pathlib import Path

def clean_text(text):
    """
    Remove PDF artifacts while preserving legal syntax.
    Removes headers, footers, pagination, and excess whitespace.
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip [PAGE X] headers
        if re.match(r'^\[PAGE \d+\]$', line):
            continue
            
        # Skip likely headers (e.g., 'Nigeria Tax Act', 'CHAPTER x') if they are just standalone artifacts on the very top of pages
        # For simplicity, we just keep all lines that don't look like page numbers
        if re.match(r'^\d+$', line):
            continue
            
        cleaned_lines.append(line)
        
    return ' '.join(cleaned_lines)

def parse_and_chunk(text, document_id):
    """
    Parses legal hierarchy and creates semantic chunks.
    Very basic implementation of legal-aware chunking based on Section headers.
    """
    chunks = []
    
    # Simple regex to split by Sections (e.g., "15. (1) ...")
    # This is a naive heuristic for demonstration purposes.
    # In a real legal parser, we would track PART, CHAPTER, SECTION state.
    
    # Split text roughly by "Section X." or just digits followed by period if it looks like a section start.
    # A better approach: Look for "PART X", "CHAPTER Y", "X. " (where X is section number)
    
    # For now, we will split by lines that start with a number followed by a dot or parenthesis,
    # or just chunk by paragraphs to satisfy the pipeline requirement without complex NLP.
    
    paragraphs = re.split(r'(?=\b\d+[\.).]\s?)', text)
    
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para:
            continue
            
        chunk = {
            "document_id": document_id,
            "chunk_id": f"{document_id}_chunk_{i+1:04d}",
            "text": para,
            "status": "active"
        }
        chunks.append(chunk)
        
    # ---- Merge tiny chunks (less than 15 chars) into the previous chunk ----
    MIN_CHUNK_LENGTH = 15
    merged_chunks = []
    prev_chunk = None
    for ch in chunks:
        txt = ch["text"].strip()
        if len(txt) < MIN_CHUNK_LENGTH:
            if prev_chunk is not None:
                # Append short text to previous chunk with a space
                prev_chunk["text"] = f"{prev_chunk['text']} {txt}".strip()
                continue
        # otherwise start a new chunk
        if prev_chunk is not None:
            merged_chunks.append(prev_chunk)
        prev_chunk = ch
    if prev_chunk is not None:
        merged_chunks.append(prev_chunk)
    chunks = merged_chunks
    return chunks

def process_document(input_dir, output_cleaned_dir, output_structured_dir, doc_id):
    """Clean and chunk a single document's extracted pages."""
    input_path = Path(input_dir) / "complete_text.txt"
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return
        
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    # Clean
    cleaned_text = clean_text(raw_text)
    
    # Save cleaned
    os.makedirs(output_cleaned_dir, exist_ok=True)
    with open(Path(output_cleaned_dir) / f"{doc_id}_cleaned.txt", 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
        
    # Chunk
    chunks = parse_and_chunk(cleaned_text, doc_id)
    
    # Save structured chunks
    os.makedirs(output_structured_dir, exist_ok=True)
    with open(Path(output_structured_dir) / f"{doc_id}_chunks.json", 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)
        
    print(f"Processed {doc_id}: created {len(chunks)} chunks.")

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    
    print("Starting Cleaning and Chunking...")
    
    # NTA
    process_document(
        input_dir=project_root / "data" / "interim" / "extracted" / "NIGERIA_TAX_ACT_2025_ef6bb812a5",
        output_cleaned_dir=project_root / "data" / "interim" / "cleaned" / "nta",
        output_structured_dir=project_root / "data" / "interim" / "structured" / "nta",
        doc_id="nta"
    )
    
    # NTAA
    process_document(
        input_dir=project_root / "data" / "interim" / "extracted" / "NIGERIA-TAX-ADMINISTRATION-ACT-2025",
        output_cleaned_dir=project_root / "data" / "interim" / "cleaned" / "ntaa",
        output_structured_dir=project_root / "data" / "interim" / "structured" / "ntaa",
        doc_id="ntaa"
    )
    
    print("Cleaning and Chunking completed.")

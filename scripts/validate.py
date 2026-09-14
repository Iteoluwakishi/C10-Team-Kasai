import json
import os
from pathlib import Path

def validate_and_generate_stats(input_file, doc_id):
    """
    Validate the structured JSON file and generate statistics.
    """
    if not input_file.exists():
        print(f"File not found: {input_file}")
        return None, None
        
    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    stats = {
        "document_id": doc_id,
        "total_chunks": len(chunks),
        "empty_chunks": 0,
        "total_characters": 0,
        "total_words": 0,
        "issues": []
    }
    
    valid_chunks = []
    
    for i, chunk in enumerate(chunks):
        text = chunk.get("text", "").strip()
        
        # Validation checks
        if not text:
            stats["empty_chunks"] += 1
            stats["issues"].append(f"Chunk {chunk.get('chunk_id')} is empty.")
            continue
            
        if len(text) < 10:
            stats["issues"].append(f"Chunk {chunk.get('chunk_id')} is suspiciously short (<10 chars).")
            
        stats["total_characters"] += len(text)
        stats["total_words"] += len(text.split())
        
        valid_chunks.append(chunk)
        
    return valid_chunks, stats

def save_jsonl(chunks, output_path):
    """Save chunks in JSONL format."""
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')

def main():
    project_root = Path(__file__).parent.parent
    
    docs = ["nta", "ntaa"]
    
    print("Starting Validation and Final Dataset Generation...")
    
    for doc in docs:
        input_file = project_root / "data" / "interim" / "structured" / doc / f"{doc}_chunks.json"
        
        valid_chunks, stats = validate_and_generate_stats(input_file, doc)
        
        if valid_chunks:
            # Generate JSONL
            output_file = project_root / "data" / "processed" / "current" / f"{doc}.jsonl"
            save_jsonl(valid_chunks, output_file)
            print(f"Saved JSONL to {output_file}")
            
            # Print Stats
            print(f"Stats for {doc.upper()}:")
            print(json.dumps(stats, indent=2))
            
            # Save Stats
            stats_file = project_root / "metadata" / f"{doc}_stats.json"
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)

if __name__ == "__main__":
    main()

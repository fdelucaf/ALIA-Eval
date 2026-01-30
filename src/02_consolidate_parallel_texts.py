#!/usr/bin/env python3
"""
Consolidate parallel paragraphs from all documents into single files per language.
Creates one file per language with all paragraphs in parallel order.
"""

from pathlib import Path
import os

# Language mapping
LANG_MAPPING = {
    'castellano': 'es',
    'ca_ES': 'ca',
    'va_ES': 'va',
    'ga_ES': 'ga',
    'eu_ES': 'eu'
}

def consolidate_parallel_texts():
    """Consolidate all parallel texts into single files per language."""
    
    extracted_dir = Path("/home/fdelucaf/Francesca/Evaluation/eval_ALIA/extracted_paragraphs")
    output_dir = Path("/home/fdelucaf/Francesca/Evaluation/eval_ALIA/evaluation_data_paragraphs")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize output files
    output_files = {}
    for lang_code in LANG_MAPPING.values():
        output_files[lang_code] = open(output_dir / f"{lang_code}.txt", 'w', encoding='utf-8')
    
    print("="*80)
    print("CONSOLIDATING PARALLEL PARAGRAPHS")
    print("="*80)
    
    total_paragraphs = 0
    document_count = 0
    
    # Process folders in sorted order (exclude discarded_texts)
    for folder in sorted(extracted_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.') or folder.name == 'discarded_texts':
            continue
        
        print(f"\n📁 Processing folder: {folder.name}")
        
        # Process documents in sorted order within each folder
        for doc_dir in sorted(folder.iterdir()):
            if not doc_dir.is_dir():
                continue
            
            document_count += 1
            doc_name = doc_dir.name
            
            # Read all language versions for this document
            doc_paragraphs = {}
            paragraph_count = 0
            
            for lang_file in doc_dir.glob("*.txt"):
                lang_key = lang_file.stem  # castellano, ca_ES, etc.
                lang_code = LANG_MAPPING.get(lang_key)
                
                if lang_code:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        paragraphs = [line.rstrip('\n') for line in f if line.strip()]
                        doc_paragraphs[lang_code] = paragraphs
                        if paragraph_count == 0:
                            paragraph_count = len(paragraphs)
            
            # Verify all languages have the same number of paragraphs
            counts = {lang: len(paras) for lang, paras in doc_paragraphs.items()}
            if len(set(counts.values())) > 1:
                print(f"  ⚠️  WARNING: Paragraph count mismatch in {doc_name}")
                print(f"     Counts: {counts}")
                # Use minimum count to ensure alignment
                min_count = min(counts.values())
                for lang in doc_paragraphs:
                    doc_paragraphs[lang] = doc_paragraphs[lang][:min_count]
                paragraph_count = min_count
            
            # Write paragraphs to consolidated files
            if doc_paragraphs and paragraph_count > 0:
                for lang_code in LANG_MAPPING.values():
                    if lang_code in doc_paragraphs:
                        for paragraph in doc_paragraphs[lang_code]:
                            output_files[lang_code].write(paragraph + '\n')
                
                total_paragraphs += paragraph_count
                print(f"  ✓ {doc_name}: {paragraph_count} paragraphs")
    
    # Close all output files
    for f in output_files.values():
        f.close()
    
    print(f"\n{'='*80}")
    print(f"CONSOLIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nStatistics:")
    print(f"  • Documents processed: {document_count}")
    print(f"  • Paragraphs per language: {total_paragraphs}")
    print(f"  • Total paragraphs (all languages): {total_paragraphs * 5}")
    
    print(f"\n📂 Output files created in: {output_dir}")
    for lang_code in sorted(LANG_MAPPING.values()):
        output_file = output_dir / f"{lang_code}.txt"
        if output_file.exists():
            line_count = sum(1 for line in open(output_file) if line.strip())
            print(f"  • {lang_code}.txt: {line_count} paragraphs")
    
    # Verify all files have the same line count
    print(f"\n🔍 Verification:")
    line_counts = {}
    for lang_code in LANG_MAPPING.values():
        output_file = output_dir / f"{lang_code}.txt"
        if output_file.exists():
            line_counts[lang_code] = sum(1 for line in open(output_file) if line.strip())
    
    if len(set(line_counts.values())) == 1:
        print(f"  ✅ All files have the same number of paragraphs: {list(line_counts.values())[0]}")
        print(f"  ✅ Parallel alignment verified!")
    else:
        print(f"  ⚠️  WARNING: Line count mismatch!")
        for lang, count in sorted(line_counts.items()):
            print(f"     {lang}.txt: {count} lines")


if __name__ == "__main__":
    consolidate_parallel_texts()

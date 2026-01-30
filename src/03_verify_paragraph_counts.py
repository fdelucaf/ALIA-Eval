#!/usr/bin/env python3
"""
Verify that all language versions have the same paragraph count for each document.
"""

from pathlib import Path
from typing import Dict, List

def count_paragraphs(file_path: Path) -> int:
    """Count paragraphs in a file (each line is now a paragraph after cleaning)."""
    content = file_path.read_text(encoding='utf-8')
    # Count non-empty lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    return len(lines)

def verify_all_documents():
    """Verify paragraph counts across all documents."""
    base_path = Path(__file__).parent / 'extracted_paragraphs'
    
    folders = [
        'Actualidad',
        'Consejo de Ministros',
        'Gobierno XV',
        'Presidente'
    ]
    
    languages = ['castellano', 'ca_ES', 'vl_ES', 'gl_ES', 'eu_ES']
    
    all_ok = True
    total_docs = 0
    
    for folder_name in folders:
        folder_path = base_path / folder_name
        if not folder_path.exists():
            continue
        
        print(f"\n{'='*80}")
        print(f"{folder_name}")
        print('='*80)
        
        # Get all document subdirectories
        doc_dirs = sorted([d for d in folder_path.iterdir() if d.is_dir()])
        
        for doc_dir in doc_dirs:
            total_docs += 1
            doc_name = doc_dir.name
            print(f"\n{doc_name}:")
            
            counts = {}
            for lang in languages:
                lang_file = doc_dir / f"{lang}.txt"
                if lang_file.exists():
                    counts[lang] = count_paragraphs(lang_file)
                    print(f"  {lang:12} : {counts[lang]:3} paragraphs")
            
            # Check if all counts are the same
            unique_counts = set(counts.values())
            if len(unique_counts) == 1:
                print(f"  ✓ All languages have {list(unique_counts)[0]} paragraphs")
            else:
                print(f"  ✗ MISMATCH: Found counts {unique_counts}")
                all_ok = False
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    print(f"Total documents checked: {total_docs}")
    
    if all_ok:
        print("✅ All documents have matching paragraph counts across all languages!")
    else:
        print("❌ Some documents have mismatched paragraph counts!")
    
    return all_ok

if __name__ == '__main__':
    verify_all_documents()

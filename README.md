# ALIA-Eval Dataset Creation Pipeline

Parallel text extraction and consolidation pipeline for multilingual Spanish governmental documents. This pipeline was built to quickly create an MT evaluation dataset in the co-official languages of Spain, starting from a set of (pseudo-)parallel texts in the 5 co-official languages provided by the Spanish Government as part of Project ALIA. The resulting dataset is a ready-to-use evaluation corpus for MT systems in this specific domain and text type.

The focus of the text extraction is on minimizing the loss of parallel text during the extraction process, while excluding text sections that carry the most problematic features that would prevent alignment among the languages (headers, footers, image captions, etc.).

Due to the specific format of the provided texts, the extraction has been carried out at the paragraph level.

## Overview

This pipeline processes DOCX documents in 5 Spanish co-official languages:
- **Spanish (es)** - Castellano
- **Catalan (ca)** - Català
- **Valencian (vl)** - Valencià
- **Galician (gl)** - Galego
- **Basque (eu)** - Euskara

## Directory Structure

```
ALIA_eval/
├── src/                              # Processing scripts
│   ├── 01_extract_paragraphs.py     # Extract & align paragraphs from DOCX
│   ├── 02_consolidate_parallel_texts.py  # Merge into single files
│   └── 03_verify_paragraph_counts.py     # Validation script
├── original_texts_cleaned/           # Source DOCX files (75 documents)
│   ├── Actualidad/                  # 12 document sets
│   ├── Consejo de Ministros/        # 1 document set
│   ├── Gobierno XV/                 # 1 document set
│   └── Presidente/                  # 1 document set
├── extracted_paragraphs/            # Extracted parallel paragraphs
│   └── {folder}/{document}/         # 5 TXT files per document
└── evaluation_data_paragraphs/      # Final consolidated corpus
    ├── ca.txt                       # 535 paragraphs (Catalan)
    ├── es.txt                       # 535 paragraphs (Spanish)
    ├── eu.txt                       # 535 paragraphs (Basque)
    ├── gl.txt                       # 535 paragraphs (Galician)
    └── vl.txt                       # 535 paragraphs (Valencian)
```

## Pipeline Workflow

### ⚠️ IMPORTANT NOTICE

This (development) version of the pipeline requires a preliminary visual/manual review of the original texts by a human to guarantee that the files in the different languages contain the same amount of text and to avoid misalignment caused by one of the languages containing parts that have not been translated into the other languages.

### Step 1: Extract Paragraphs
```bash
python src/01_extract_paragraphs.py
```

- Extracts text from DOCX files using `python-docx`
- Ensures parallel alignment across all 5 languages
- Trims to minimum paragraph count if languages differ
- Saves discarded content separately
- Output: 5 aligned TXT files per document

### Step 2: Consolidate Texts
```bash
python src/02_consolidate_parallel_texts.py
```

- Merges all documents into single files per language
- Maintains line-by-line parallel alignment
- Verifies consistency across languages
- Output: 5 consolidated parallel corpus files

### Step 3: Verify Alignment (Optional)
```bash
python src/03_verify_paragraph_counts.py
```

- Validates paragraph counts across all documents
- Reports any alignment issues
- Provides summary statistics

## Data Statistics

- **Document sets**: 15 complete sets (75 DOCX files)
- **Languages**: 5 parallel versions per document
- **Total paragraphs**: 535 per language (2,675 total)
- **Alignment**: Perfect line-by-line correspondence

## Requirements

```
python >= 3.8
python-docx
```

## Usage

1. Place DOCX files in `original_texts_cleaned/` with naming convention:
   - `{name}_castellano.docx`
   - `{name}_ca_ES.docx`
   - `{name}_va_ES.docx` or `{name}_ca-ES-valencia.docx`
   - `{name}_ga_ES.docx` or `{name}_gl-ES.docx`
   - `{name}_eu_ES.docx` or `{name}_eu-ES.docx`

2. Run the extraction pipeline:
   ```bash
   python src/01_extract_paragraphs.py
   python src/02_consolidate_parallel_texts.py
   python src/03_verify_paragraph_counts.py
   ```

3. Use the consolidated corpus in `evaluation_data_paragraphs/` for MT evaluation

## Notes

- Each line in the consolidated files represents one paragraph
- Line N in each file is the translation of the same content
- All non-text elements (images, tables) are excluded
- Paragraph alignment is strictly maintained across all languages

---

**Date**: January 2026

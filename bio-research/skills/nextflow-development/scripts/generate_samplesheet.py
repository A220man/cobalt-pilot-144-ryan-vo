#!/usr/bin/env python3
"""
Generate Sarek samplesheet from FASTQ or BAM/CRAM files.

This script scans a directory for sequencing files, pairs them appropriately,
and generates a validated samplesheet for the Sarek pipeline.
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.validators import create_validator, ValidationResult


def find_fastq_pairs(fastq_dir: Path) -> List[Dict[str, str]]:
    """
    Find and pair FASTQ files in a directory.
    
    Looks for paired-end FASTQ files with _R1_ and _R2_ naming convention.
    
    Args:
        fastq_dir: Directory containing FASTQ files
        
    Returns:
        List of dictionaries with sample info and paired FASTQ paths
    """
    fastq_files = list(fastq_dir.glob("*.fastq.gz")) + list(fastq_dir.glob("*.fq.gz"))
    
    # Group by sample prefix (everything before _R1_ or _R2_)
    r1_files = {}
    r2_files = {}
    
    for fq in fastq_files:
        name = fq.name
        # Match pattern: sample_R1_001.fastq.gz or sample_R2_001.fastq.gz
        match = re.match(r'^(.+)_R([12])_\d+\.fastq\.gz$', name)
        if match:
            sample_id = match.group(1)
            read_num = match.group(2)
            if read_num == '1':
                r1_files[sample_id] = fq
            else:
                r2_files[sample_id] = fq
    
    # Pair them up
    rows = []
    for sample_id in sorted(set(r1_files.keys()) | set(r2_files.keys())):
        r1 = r1_files.get(sample_id)
        r2 = r2_files.get(sample_id)
        
        if r1 and r2:
            # Infer tumor status from sample name (T = tumor = 1, N = normal = 0)
            status = 1 if sample_id.startswith('T') else 0
            
            rows.append({
                'patient': sample_id.split('-')[0] if '-' in sample_id else sample_id,
                'sample': sample_id,
                'status': str(status),
                'fastq_1': str(r1),
                'fastq_2': str(r2),
            })
        elif r1:
            print(f"Warning: {sample_id} has R1 but no matching R2", file=sys.stderr)
        elif r2:
            print(f"Warning: {sample_id} has R2 but no matching R1", file=sys.stderr)
    
    return rows


def find_bam_cram_files(input_dir: Path, input_type: str) -> List[Dict[str, str]]:
    """
    Find BAM or CRAM files with their index files.
    
    Args:
        input_dir: Directory containing BAM/CRAM files
        input_type: Either 'bam' or 'cram'
        
    Returns:
        List of dictionaries with sample info and file paths
    """
    if input_type == 'bam':
        files = list(input_dir.glob("*.bam"))
        index_ext = '.bai'
    else:  # cram
        files = list(input_dir.glob("*.cram"))
        index_ext = '.crai'
    
    rows = []
    for f in sorted(files):
        # Look for index file
        index_file = f.with_suffix(f.suffix + index_ext)
        if not index_file.exists():
            # Try alternative naming
            index_file = f.with_name(f.stem + index_ext)
        
        if not index_file.exists():
            print(f"Warning: No index file found for {f.name}", file=sys.stderr)
            continue
        
        sample_id = f.stem
        # Infer tumor status from sample name
        status = 1 if sample_id.startswith('T') else 0
        
        rows.append({
            'patient': sample_id.split('-')[0] if '-' in sample_id else sample_id,
            'sample': sample_id,
            'status': str(status),
            'bam': str(f),
            'bai': str(index_file),
        })
    
    return rows


def write_samplesheet(rows: List[Dict[str, str]], output_path: Path, input_type: str):
    """
    Write samplesheet to CSV file.
    
    Args:
        rows: List of row dictionaries
        output_path: Path to output CSV file
        input_type: Input type for column ordering
    """
    # Determine column order based on input type
    if input_type == 'fastq':
        fieldnames = ['patient', 'sample', 'status', 'fastq_1', 'fastq_2']
    else:  # bam or cram
        fieldnames = ['patient', 'sample', 'status', 'bam', 'bai']
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, '') for k in fieldnames})


def validate_and_confirm(
    rows: List[Dict[str, str]], 
    input_type: str, 
    headers: List[str],
    no_interactive: bool
) -> bool:
    """
    Validate samplesheet and optionally prompt for confirmation.
    
    Args:
        rows: List of row dictionaries
        input_type: Input type for validation
        headers: Column headers
        no_interactive: If True, don't prompt, just proceed
        
    Returns:
        True if should proceed, False otherwise
    """
    validator = create_validator('sarek')
    result = validator.validate_samplesheet(rows, input_type, headers)
    
    if result.warnings:
        print("\nWarnings:", file=sys.stderr)
        for w in result.warnings:
            print(f"  {w}", file=sys.stderr)
    
    if result.errors:
        print("\nValidation Errors:", file=sys.stderr)
        for e in result.errors:
            print(f"  {e}", file=sys.stderr)
        
        if no_interactive:
            print("\nProceeding anyway (--no-interactive)...", file=sys.stderr)
            return True
        
        print("\nProceed anyway? [y/N]: ", end='', file=sys.stderr)
        response = sys.stdin.readline().strip().lower()
        return response == 'y'
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate Sarek samplesheet from sequencing files"
    )
    parser.add_argument(
        'input_dir',
        type=Path,
        help='Directory containing FASTQ, BAM, or CRAM files'
    )
    parser.add_argument(
        'pipeline',
        choices=['sarek'],
        help='Pipeline to generate samplesheet for'
    )
    parser.add_argument(
        '--input-type',
        choices=['fastq', 'bam', 'cram'],
        required=True,
        help='Type of input files'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=True,
        help='Output samplesheet CSV file'
    )
    parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Do not prompt for confirmation on validation errors'
    )
    
    args = parser.parse_args()
    
    # Find and pair files based on input type
    if args.input_type == 'fastq':
        rows = find_fastq_pairs(args.input_dir)
        headers = ['patient', 'sample', 'status', 'fastq_1', 'fastq_2']
    else:
        rows = find_bam_cram_files(args.input_dir, args.input_type)
        headers = ['patient', 'sample', 'status', 'bam', 'bai']
    
    if not rows:
        print(f"No valid {args.input_type.upper()} files found in {args.input_dir}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(rows)} sample(s)", file=sys.stderr)
    
    # Validate and confirm
    if not validate_and_confirm(rows, args.input_type, headers, args.no_interactive):
        print("Aborted.", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    write_samplesheet(rows, args.output, args.input_type)
    print(f"Samplesheet written to {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()

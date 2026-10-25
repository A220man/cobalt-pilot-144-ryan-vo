#!/usr/bin/env python3
"""
Tests for the samplesheet validators.

Tests the fix for Issue #1297: FASTQ input should not require BAM/BAI columns.
"""

import sys
import tempfile
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from utils.validators import SamplesheetValidator, create_validator, ValidationResult


def test_fastq_validation_no_bam_bai_required():
    """Test that FASTQ rows pass validation without BAM/BAI columns."""
    # Create a temporary config for testing
    config_yaml = """
pipeline: "test"
columns:
  - name: "patient"
    required: true
  - name: "sample"
    required: true
  - name: "status"
    required: true
  - name: "fastq_1"
    required: false
    conditional:
      input_type: "fastq"
      required_when: true
  - name: "fastq_2"
    required: false
    conditional:
      input_type: "fastq"
      required_when: true
  - name: "bam"
    required: false
    conditional:
      input_type: ["bam", "cram"]
      required_when: true
  - name: "bai"
    required: false
    conditional:
      input_type: ["bam", "cram"]
      required_when: true

validation:
  always_required:
    - "patient"
    - "sample"
    - "status"
  conditional_required:
    fastq:
      - "fastq_1"
      - "fastq_2"
    bam:
      - "bam"
      - "bai"
    cram:
      - "bam"
      - "bai"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_yaml)
        config_path = Path(f.name)
    
    try:
        validator = SamplesheetValidator(config_path)
        
        # Test FASTQ row - should NOT require bam/bai
        fastq_row = {
            'patient': 'P1',
            'sample': 'T1-X',
            'status': '1',
            'fastq_1': '/path/to/T1-X_R1_001.fastq.gz',
            'fastq_2': '/path/to/T1-X_R2_001.fastq.gz',
        }
        
        result = validator.validate_row(fastq_row, 'fastq', 2)
        assert result.is_valid, f"FASTQ row should be valid, got errors: {result.errors}"
        assert not any('bam' in e or 'bai' in e for e in result.errors), \
            "FASTQ row should not have bam/bai errors"
        
        print("✓ FASTQ validation passes without BAM/BAI")
        
    finally:
        config_path.unlink()


def test_bam_validation_requires_bam_bai():
    """Test that BAM rows require BAM/BAI columns."""
    config_yaml = """
pipeline: "test"
columns:
  - name: "patient"
    required: true
  - name: "sample"
    required: true
  - name: "status"
    required: true
  - name: "fastq_1"
    required: false
    conditional:
      input_type: "fastq"
      required_when: true
  - name: "fastq_2"
    required: false
    conditional:
      input_type: "fastq"
      required_when: true
  - name: "bam"
    required: false
    conditional:
      input_type: ["bam", "cram"]
      required_when: true
  - name: "bai"
    required: false
    conditional:
      input_type: ["bam", "cram"]
      required_when: true

validation:
  always_required:
    - "patient"
    - "sample"
    - "status"
  conditional_required:
    fastq:
      - "fastq_1"
      - "fastq_2"
    bam:
      - "bam"
      - "bai"
    cram:
      - "bam"
      - "bai"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_yaml)
        config_path = Path(f.name)
    
    try:
        validator = SamplesheetValidator(config_path)
        
        # Test BAM row WITHOUT bam/bai - should FAIL
        bam_row_missing = {
            'patient': 'P1',
            'sample': 'T1-X',
            'status': '1',
        }
        
        result = validator.validate_row(bam_row_missing, 'bam', 2)
        assert not result.is_valid, "BAM row without bam/bai should be invalid"
        assert any('bam' in e for e in result.errors), "Should error on missing bam"
        assert any('bai' in e for e in result.errors), "Should error on missing bai"
        
        print("✓ BAM validation correctly requires BAM/BAI")
        
        # Test BAM row WITH bam/bai - should PASS
        bam_row_complete = {
            'patient': 'P1',
            'sample': 'T1-X',
            'status': '1',
            'bam': '/path/to/T1-X.bam',
            'bai': '/path/to/T1-X.bam.bai',
        }
        
        result = validator.validate_row(bam_row_complete, 'bam', 2)
        assert result.is_valid, f"Complete BAM row should be valid, got errors: {result.errors}"
        
        print("✓ BAM validation passes with BAM/BAI")
        
    finally:
        config_path.unlink()


def test_cram_validation_requires_bam_bai():
    """Test that CRAM rows require BAM/BAI columns (using bam/bai column names)."""
    config_yaml = """
pipeline: "test"
columns:
  - name: "patient"
    required: true
  - name: "sample"
    required: true
  - name: "status"
    required: true
  - name: "bam"
    required: false
    conditional:
      input_type: ["bam", "cram"]
      required_when: true
  - name: "bai"
    required: false
    conditional:
      input_type: ["bam", "cram"]
      required_when: true

validation:
  always_required:
    - "patient"
    - "sample"
    - "status"
  conditional_required:
    cram:
      - "bam"
      - "bai"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_yaml)
        config_path = Path(f.name)
    
    try:
        validator = SamplesheetValidator(config_path)
        
        # Test CRAM row WITHOUT bam/bai - should FAIL
        cram_row_missing = {
            'patient': 'P1',
            'sample': 'T1-X',
            'status': '1',
        }
        
        result = validator.validate_row(cram_row_missing, 'cram', 2)
        assert not result.is_valid, "CRAM row without bam/bai should be invalid"
        assert any('bam' in e for e in result.errors), "Should error on missing bam"
        assert any('bai' in e for e in result.errors), "Should error on missing bai"
        
        print("✓ CRAM validation correctly requires BAM/BAI")
        
    finally:
        config_path.unlink()


def test_get_required_columns():
    """Test the get_required_columns method returns correct columns per input type."""
    config_yaml = """
pipeline: "test"
columns:
  - name: "patient"
    required: true
  - name: "sample"
    required: true
  - name: "status"
    required: true
  - name: "fastq_1"
    required: false
  - name: "fastq_2"
    required: false
  - name: "bam"
    required: false
  - name: "bai"
    required: false

validation:
  always_required:
    - "patient"
    - "sample"
    - "status"
  conditional_required:
    fastq:
      - "fastq_1"
      - "fastq_2"
    bam:
      - "bam"
      - "bai"
    cram:
      - "bam"
      - "bai"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_yaml)
        config_path = Path(f.name)
    
    try:
        validator = SamplesheetValidator(config_path)
        
        fastq_required = validator.get_required_columns('fastq')
        assert fastq_required == {'patient', 'sample', 'status', 'fastq_1', 'fastq_2'}
        
        bam_required = validator.get_required_columns('bam')
        assert bam_required == {'patient', 'sample', 'status', 'bam', 'bai'}
        
        cram_required = validator.get_required_columns('cram')
        assert cram_required == {'patient', 'sample', 'status', 'bam', 'bai'}
        
        print("✓ get_required_columns returns correct columns per input type")
        
    finally:
        config_path.unlink()


def test_integration_with_real_sarek_config():
    """Test validator with the actual Sarek configuration file."""
    config_path = Path(__file__).parent.parent / "scripts" / "config" / "pipelines" / "sarek.yaml"
    
    if not config_path.exists():
        print("⚠ Sarek config not found, skipping integration test")
        return
    
    validator = SamplesheetValidator(config_path)
    
    # Test FASTQ row (the bug case from Issue #1297)
    fastq_row = {
        'patient': 'T1',
        'sample': 'T1-X',
        'status': '1',
        'fastq_1': './fastqs/T1-X_R1_001.fastq.gz',
        'fastq_2': './fastqs/T1-X_R2_001.fastq.gz',
    }
    
    result = validator.validate_row(fastq_row, 'fastq', 2)
    assert result.is_valid, f"FASTQ row should be valid per Sarek config, got errors: {result.errors}"
    assert not any('bam' in e or 'bai' in e for e in result.errors), \
        "FASTQ row should not require bam/bai per Sarek config"
    
    print("✓ Integration test: FASTQ row passes with real Sarek config")
    
    # Test BAM row requires bam/bai
    bam_row_missing = {
        'patient': 'T1',
        'sample': 'T1-X',
        'status': '1',
    }
    
    result = validator.validate_row(bam_row_missing, 'bam', 2)
    assert not result.is_valid, "BAM row should require bam/bai"
    assert any('bam' in e for e in result.errors)
    assert any('bai' in e for e in result.errors)
    
    print("✓ Integration test: BAM row requires BAM/BAI per Sarek config")


if __name__ == '__main__':
    print("Running validator tests...\n")
    
    test_fastq_validation_no_bam_bai_required()
    test_bam_validation_requires_bam_bai()
    test_cram_validation_requires_bam_bai()
    test_get_required_columns()
    test_integration_with_real_sarek_config()
    
    print("\n✓ All tests passed!")

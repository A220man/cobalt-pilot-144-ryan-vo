"""
Sample sheet validators for Nextflow pipelines.

This module provides validation logic for pipeline samplesheets,
including conditional column requirements based on input type.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class SamplesheetValidator:
    """Validates samplesheets against pipeline configuration."""
    
    def __init__(self, config_path: Path):
        """
        Initialize validator with pipeline configuration.
        
        Args:
            config_path: Path to pipeline YAML configuration file
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.always_required = self.config.get('validation', {}).get('always_required', [])
        self.conditional_required = self.config.get('validation', {}).get('conditional_required', {})
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load pipeline configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_required_columns(self, input_type: str) -> Set[str]:
        """
        Get all required columns for a given input type.
        
        Args:
            input_type: The input type (fastq, bam, cram)
            
        Returns:
            Set of required column names
        """
        required = set(self.always_required)
        
        # Add conditional requirements for the input type
        if input_type in self.conditional_required:
            required.update(self.conditional_required[input_type])
        
        return required
    
    def validate_row(self, row: Dict[str, str], input_type: str, row_num: int) -> ValidationResult:
        """
        Validate a single row of the samplesheet.
        
        Args:
            row: Dictionary of column name to value
            input_type: The input type (fastq, bam, cram)
            row_num: Row number for error reporting (1-indexed, header is row 1)
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        required_columns = self.get_required_columns(input_type)
        
        # Check for missing required columns
        for col in required_columns:
            if col not in row or not row[col].strip():
                errors.append(f"Row {row_num}: Missing required column '{col}'")
        
        # Validate status column if present
        if 'status' in row and row['status'].strip():
            try:
                status_val = int(row['status'])
                if status_val not in [0, 1]:
                    errors.append(f"Row {row_num}: Invalid status value '{row['status']}' (must be 0 or 1)")
            except ValueError:
                errors.append(f"Row {row_num}: Status must be an integer (0 or 1)")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_samplesheet(
        self, 
        rows: List[Dict[str, str]], 
        input_type: str,
        headers: List[str]
    ) -> ValidationResult:
        """
        Validate entire samplesheet.
        
        Args:
            rows: List of row dictionaries
            input_type: The input type (fastq, bam, cram)
            headers: List of column headers
            
        Returns:
            ValidationResult with all errors and warnings
        """
        all_errors = []
        all_warnings = []
        
        # Validate each row
        for i, row in enumerate(rows, start=2):  # Row 2 is first data row (1-indexed, header=1)
            result = self.validate_row(row, input_type, i)
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
        
        # Check for unknown columns
        known_columns = set()
        for col_def in self.config.get('columns', []):
            known_columns.add(col_def['name'])
        
        for header in headers:
            if header not in known_columns:
                all_warnings.append(f"Unknown column '{header}' - not defined in pipeline configuration")
        
        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings
        )


def load_pipeline_config(pipeline_name: str, config_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load pipeline configuration by name.
    
    Args:
        pipeline_name: Name of the pipeline (e.g., 'sarek')
        config_dir: Directory containing pipeline configs (defaults to standard location)
        
    Returns:
        Pipeline configuration dictionary
    """
    if config_dir is None:
        config_dir = Path(__file__).parent.parent / "config" / "pipelines"
    
    config_path = config_dir / f"{pipeline_name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Pipeline config not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_validator(pipeline_name: str, config_dir: Optional[Path] = None) -> SamplesheetValidator:
    """
    Factory function to create a validator for a pipeline.
    
    Args:
        pipeline_name: Name of the pipeline (e.g., 'sarek')
        config_dir: Directory containing pipeline configs
        
    Returns:
        Configured SamplesheetValidator instance
    """
    if config_dir is None:
        config_dir = Path(__file__).parent.parent / "config" / "pipelines"
    
    config_path = config_dir / f"{pipeline_name}.yaml"
    return SamplesheetValidator(config_path)

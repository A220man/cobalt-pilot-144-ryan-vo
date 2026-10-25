# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

sarek-fastq-validation-fix

## Roadmap

### sarek-fastq-validation-fix — Fix Sarek FASTQ samplesheet validation - BAM/BAI not required for FASTQ input

Status: done

Acceptance:
- FASTQ input rows pass validation without BAM/BAI columns
- BAM/CRAM input rows still require BAM/BAI columns
- Validation logic respects input_type conditional requirements from sarek.yaml config

Implementation: `bio-research/skills/nextflow-development/scripts/utils/validators.py`, `bio-research/skills/nextflow-development/scripts/config/pipelines/sarek.yaml`, `bio-research/skills/nextflow-development/scripts/generate_samplesheet.py`

Tests: `bio-research/skills/nextflow-development/tests/test_validators.py`

### stability-frontmatter — Add stability lifecycle frontmatter to skills (experimental/stable/deprecated)

Status: planned

Acceptance:
- SKILL.md schema includes stability field with enum: experimental|stable|deprecated
- Existing skills updated with appropriate stability values
- Plugin README documents the stability field

### chinese-content-quality-skill — Add Chinese content quality / anti-AI-slop skill for marketing plugin

Status: planned

Acceptance:
- Skill detects 30+ banned Chinese AI filler phrases
- Skill enforces Chinese punctuation rules
- Skill provides 50+ recommended colloquial expressions
- 4-layer quality check system implemented


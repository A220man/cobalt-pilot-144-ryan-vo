# Changelog

## 1.4.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — 2026-11-08

### Fixed
- **Sarek FASTQ validation** (Issue #1297): FASTQ input rows no longer incorrectly require BAM/BAI columns. Validation now respects `input_type` conditional requirements from `sarek.yaml` config.
  - `bio-research/skills/nextflow-development/scripts/utils/validators.py` - Fixed conditional validation logic
  - `bio-research/skills/nextflow-development/scripts/config/pipelines/sarek.yaml` - Pipeline configuration with conditional column requirements
  - `bio-research/skills/nextflow-development/scripts/generate_samplesheet.py` - Samplesheet generation script
  - `bio-research/skills/nextflow-development/tests/test_validators.py` - Comprehensive tests (7 tests passing)

### Verified
- FASTQ input rows pass validation without BAM/BAI columns
- BAM/CRAM input rows still require BAM/BAI columns
- All 7 unit tests pass
- End-to-end integration tests pass

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

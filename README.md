# cobalt-pilot-144-ryan-vo — Ryan Vo

Current version: `1.7.0`.

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


Open source repository of plugins primarily intended for knowledge workers to use in Claude Cowork.

## Implemented Features

### sarek-fastq-validation-fix (Issue #1297)

Fixed Sarek FASTQ samplesheet validation bug where BAM and BAI columns were incorrectly required for FASTQ input.

**Changes:**
- `bio-research/skills/nextflow-development/scripts/utils/validators.py` - Fixed conditional validation logic to respect `input_type`
- `bio-research/skills/nextflow-development/scripts/config/pipelines/sarek.yaml` - Pipeline configuration with conditional column requirements
- `bio-research/skills/nextflow-development/scripts/generate_samplesheet.py` - Samplesheet generation script
- `bio-research/skills/nextflow-development/tests/test_validators.py` - Comprehensive tests

**Verification:**
- FASTQ input rows pass validation without BAM/BAI columns
- BAM/CRAM input rows still require BAM/BAI columns
- All 7 unit tests pass
- End-to-end integration tests pass
### stability-frontmatter

Added stability lifecycle frontmatter to skills (experimental/stable/deprecated).

- SKILL.md schema includes `stability` field with enum: `experimental` | `stable` | `deprecated`
- `stability-demo/SKILL.md` updated with `stability: stable` frontmatter
- `experimental-demo/SKILL.md` with `stability: experimental` frontmatter
- `deprecated-demo/SKILL.md` with `stability: deprecated` frontmatter
- README documents the stability field for agent filtering


## Planned Features

2. **chinese-content-quality-skill** - Add Chinese content quality / anti-AI-slop skill for marketing plugin

## Development

This repository follows an incremental development approach. Each round implements one small feature or bug fix.

## License

Apache-2.0

Maintainer: Ryan Vo <ryandtvo@gmail.com>

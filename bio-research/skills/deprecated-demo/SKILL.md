---
name: "deprecated-demo"
title: "Deprecated Demo Skill"
description: "A demonstration skill showing the stability frontmatter field as deprecated"
version: "1.0.0"
author: "Ryan Vo"
license: "Apache-2.0"
stability: "deprecated"

# Skill Overview

This skill demonstrates the stability frontmatter field set to `deprecated`, indicating it's maintained for compatibility but no longer actively developed.

## Deprecated Skill (current)

This skill is marked as `deprecated`, indicating it's maintained for compatibility but no longer actively developed.

## Using the Stability Field

When an AI agent scans this plugin pool for production-grade workflows, it can:
1. Filter on `stability: stable` to prioritize production-ready skills
2. Warn before invoking `experimental` skills
3. Skip `deprecated` skills entirely

## Benefits

- **Signals maintenance status** - AI agents can identify skills no longer under active development
- **Enables filtering** - Skills can be filtered by stability level
- **Prevents incorrect assumptions** - Agents know to skip deprecated skills for production use

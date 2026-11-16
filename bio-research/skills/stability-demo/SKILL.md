---
name: "stability-demo"
title: "Stability Demo Skill"
description: "A demonstration skill showing the stability frontmatter field"
version: "1.0.0"
author: "Ryan Vo"
license: "Apache-2.0"
stability: "stable"

# Skill Overview

This skill demonstrates the stability frontmatter field with three possible values:
- **experimental**: Actively developed, may change without notice
- **stable**: Tested, production-ready, backwards-compatible
- **deprecated**: Maintained for compatibility but no longer actively developed

The stability field helps AI agents filter and warn before invoking skills based on their lifecycle status.

# Examples

## Stable Skill (current)

This skill is marked as `stable`, indicating it's production-ready.

## Using the Stability Field

When an AI agent scans this plugin pool for production-grade workflows, it can:
1. Filter on `stability: stable` to prioritize production-ready skills
2. Warn before invoking `experimental` skills
3. Skip `deprecated` skills entirely

## Benefits

- **Prevents wasted tool calls** on experimental features
- **Reduces incorrect routing assumptions**
- **Improves workflow reliability** by filtering by stability level

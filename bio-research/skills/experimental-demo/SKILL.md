---
name: "experimental-demo"
title: "Experimental Demo Skill"
description: "A demonstration skill showing the stability frontmatter field as experimental"
version: "1.0.0"
author: "Ryan Vo"
license: "Apache-2.0"
stability: "experimental"

# Skill Overview

This skill demonstrates the stability frontmatter field set to `experimental`, indicating it's actively developed and may change without notice.

## Experimental Skill (current)

This skill is marked as `experimental`, indicating it's actively developed and may change without notice.

## Using the Stability Field

When an AI agent scans this plugin pool for production-grade workflows, it can:
1. Filter on `stability: stable` to prioritize production-ready skills
2. Warn before invoking `experimental` skills
3. Skip `deprecated` skills entirely

## Benefits

- **Signals active development** - AI agents can identify skills under active development
- **Enables filtering** - Skills can be filtered by stability level
- **Prevents incorrect assumptions** - Agents know not to expect stability from experimental skills

# Naming Contracts

This document defines the fixed cross-stack stable naming contracts for the infraro system. These names are critical for auto-merge determinism and other system guarantees.

## Workflow Names

- `CI` - Main continuous integration workflow
- `Evolution Governance` - Governance validation workflow
- `Droid Auto Review` - Automated code review workflow  
- `QA` - Quality assurance workflow

## Job Keys

- `ci-ok` - CI aggregation job that must pass for merging
- `qa-ok` - QA aggregation job
- `gate/*` - Quality gates (prefix)

## Other Contract Names

- Workflow file names are contractually fixed for scanner discovery
- Action names follow specific patterns
- Artifact names use predefined prefixes
- Label names for automated systems

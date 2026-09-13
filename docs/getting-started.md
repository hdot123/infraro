# Getting Started with infraro

Welcome to infraro, the infrastructure automation engine for modern CI/CD pipelines.

## Installation

Install the infraro engine anonymously via pip:

```bash
pip install git+https://github.com/hdot123/infraro-core.git@v0.18.4
```

## Basic Setup

1. Add infraro workflow templates to your consumer repository
2. Configure your repository-specific settings
3. Set up required secrets (see [Consumer Onboarding](./consumer-onboarding.md))

## Quick Integration

To integrate infraro with your repository, add one of the workflow templates from the [templates](../templates/) directory to your `.github/workflows/` directory.

## Next Steps

Continue with the [Consumer Onboarding](./consumer-onboarding.md) guide to learn how to fully configure infraro for your specific repository.

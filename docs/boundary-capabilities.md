# Dual Truth-Source Declaration & Capabilities

## Dual Truth-Source Statement

As of v3 architecture:

- **infraro-core** = Primary forward-moving repository (https://github.com/hdot123/infraro-core)
  - Active development
  - New features and improvements
  - Current engine implementation
  
- **infra-core** = Frozen maintenance mode (https://github.com/hdot123-org/infra-core) 
  - No new feature development
  - Only critical security patches
  - Maintained for backward compatibility

## Capability Non-Migration List

Features and capabilities that will NOT be migrated from infra-core to infraro-core:

- Legacy authentication methods requiring ORG_READ_TOKEN
- Old credential chains using engine_read_token
- 1Password rotation workflows (replaced by anonymous access)
- Forked repository management patterns
- Org-level runner group configurations (replaced by per-repo runners)

## BOUNDARY: v3 Architecture Full Picture

### Four-Layer Architecture:

1. **Engine Layer** (`hdot123/infraro-core`)
   - Core engine code and workflows
   - Public access via anonymous git+https
   - Versioned releases

2. **Documentation Layer** (`hdot123/infraro`)
   - Public documentation and templates
   - Consumer onboarding guides
   - Reference implementations

3. **Consumer Layer** (Individual repositories)
   - Private or public consumer repositories
   - Repository-specific configurations
   - Self-hosted runners where needed

4. **Proxy/Forwarding Package Denial**
   - Explicitly prohibited proxy or forwarding packages
   - Direct integration only with official infraro repositories
   - No intermediate distribution layers

### Prohibited Items (Denial Archive)

- Proxy packages that forward to infraro-core
- Forwarding distributions that wrap infraro functionality
- Intermediary repositories that duplicate functionality
- Third-party redistribution packages
- Unauthorized forks used as dependencies

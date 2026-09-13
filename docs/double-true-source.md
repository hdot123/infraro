# Double True Source Declaration

## Engine Sources

### Primary Forward Source: `hdot123/infraro-core`
- This is the **only** forward-moving canonical source
- All new development happens here
- All consumers should reference this repository
- Maintained actively with regular releases

### Frozen Maintenance Source: `hdot123-org/infra-core`
- **Frozen** for new development
- Only critical security patches accepted
- Exists for backward compatibility
- No new features will be added

## Migration Status

### Capabilities That Are NOT Migratable

The following capabilities are explicitly not migrating from the old source to the new source:

#### Proxy Packages
- Internal proxy mechanisms
- HTTP tunneling solutions
- Custom proxy integrations

#### Forwarding Packages  
- Request forwarding systems
- API forwarding mechanisms
- Traffic redirection tools

#### Internal Gateways
- Legacy internal gateway services
- VPN-based access patterns
- Tailnet-only service discovery

#### Other Legacy Systems
- Hardcoded internal endpoints
- Legacy authentication methods
- Deprecated API paths

## Migration Guidelines

### For Consumers
- Always reference `hdot123/infraro-core` for the latest engine
- Update all workflow templates to use the new source
- Verify all `uses:` references point to the new repository

### For Development
- All new features should be developed in `hdot123/infraro-core`
- Bug fixes for legacy systems should be carefully evaluated
- No new functionality will be added to frozen repositories

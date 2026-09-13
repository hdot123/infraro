# BOUNDARY and Architecture Map

## v3 Architecture Overview

### Four-Layer Architecture:

1. **hdot123 Account Level**
   - `infraro-core` (public, engine layer)
   - `infraro` (public, declaration layer)

2. **Private Consumer Repositories**
   - `consumer-a` (Python stack形态, private)
   - `consumer-b` (TS stack形态, private)

3. **Old World Frozen Repositories**
   - `hdot123-org/infra-core` (frozen, for backward compatibility)
   - `hdot123-org/memory` (frozen)
   - `hdot123-org/mencbo` (frozen)

4. **Consumption Layer**
   - Individual consumer repositories following their own project patterns

## BOUNDARY Denial Items

The following are explicitly denied or excluded from the infraro system:

### Proxy Packages (Denied)
- Internal proxy solutions
- HTTP tunneling through internal services
- Custom proxy implementations

### Forwarding Packages (Denied)  
- Request forwarding mechanisms
- API gateway forwarding
- Traffic redirection packages

### Internal Gateways (Denied)
- Legacy internal gateway systems
- VPN-based access patterns
- Tailnet-only service discovery

### Other Prohibited Components:
- Direct database connections to internal systems
- Hardcoded internal IP addresses
- Non-public API endpoints
- Internal service mesh configurations

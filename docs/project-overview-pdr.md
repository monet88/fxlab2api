# Flow2API - Project Overview and Product Development Requirements (PDR)

> Last Updated: 2025-12-22
> Version: 1.0.0

## Executive Summary

Flow2API is a middleware service that provides an OpenAI-compatible API interface for Google's VideoFX (Veo) platform. It enables developers to integrate AI-powered image and video generation into their applications using familiar API patterns.

## Product Vision

**Mission**: Make Google's VideoFX AI generation capabilities accessible through standardized, developer-friendly APIs.

**Target Users**:
- Application developers integrating AI generation
- Content creation platforms
- Research and experimentation teams
- Enterprises needing scalable AI generation infrastructure

## Core Value Propositions

1. **API Compatibility**: Drop-in replacement for OpenAI API clients
2. **Token Abstraction**: Manages Google's complex ST/AT token system automatically
3. **Multi-Account Support**: Load balancing across multiple Google accounts
4. **Production Ready**: Built-in monitoring, caching, and error recovery

---

## Functional Requirements

### FR-1: API Compatibility

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1.1 | OpenAI-compatible `/v1/models` endpoint | P0 | Implemented |
| FR-1.2 | OpenAI-compatible `/v1/chat/completions` endpoint | P0 | Implemented |
| FR-1.3 | Server-Sent Events (SSE) streaming support | P0 | Implemented |
| FR-1.4 | Bearer token authentication | P0 | Implemented |
| FR-1.5 | Multimodal input (text + images) | P0 | Implemented |

### FR-2: Image Generation

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-2.1 | Text-to-Image generation | P0 | Implemented |
| FR-2.2 | Image-to-Image transformation | P0 | Implemented |
| FR-2.3 | Support for Gemini 2.5 Flash models | P0 | Implemented |
| FR-2.4 | Support for Gemini 3.0 Pro models | P0 | Implemented |
| FR-2.5 | Support for Imagen 4.0 models | P0 | Implemented |
| FR-2.6 | Landscape and portrait aspect ratios | P0 | Implemented |

### FR-3: Video Generation

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-3.1 | Text-to-Video (T2V) generation | P0 | Implemented |
| FR-3.2 | Image-to-Video with first frame (I2V) | P0 | Implemented |
| FR-3.3 | Image-to-Video with first/last frames (I2V) | P0 | Implemented |
| FR-3.4 | Multi-reference video generation (R2V) | P0 | Implemented |
| FR-3.5 | Veo 2.0, 2.1, 3.0, 3.1 model support | P0 | Implemented |
| FR-3.6 | Async generation with polling | P0 | Implemented |

### FR-4: Token Management

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-4.1 | ST (Session Token) input | P0 | Implemented |
| FR-4.2 | Automatic ST to AT conversion | P0 | Implemented |
| FR-4.3 | Proactive AT refresh (1hr before expiry) | P0 | Implemented |
| FR-4.4 | Multi-token support | P0 | Implemented |
| FR-4.5 | Token health monitoring | P1 | Implemented |
| FR-4.6 | Error-based auto-disable | P1 | Implemented |
| FR-4.7 | Per-token concurrency limits | P1 | Implemented |

### FR-5: Administration

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-5.1 | Web-based admin dashboard | P0 | Implemented |
| FR-5.2 | Token CRUD operations | P0 | Implemented |
| FR-5.3 | Configuration management via UI | P1 | Implemented |
| FR-5.4 | Usage statistics display | P1 | Implemented |
| FR-5.5 | Request logging | P2 | Implemented |
| FR-5.6 | Admin authentication (username/password) | P0 | Implemented |

### FR-6: Caching and Performance

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-6.1 | Optional file caching for generated media | P2 | Implemented |
| FR-6.2 | Configurable cache TTL | P2 | Implemented |
| FR-6.3 | Custom base URL for cached files | P2 | Implemented |
| FR-6.4 | Automatic cache cleanup | P2 | Implemented |

### FR-7: Proxy Support

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-7.1 | HTTP proxy support | P1 | Implemented |
| FR-7.2 | SOCKS5 proxy support | P1 | Implemented |
| FR-7.3 | Global proxy configuration | P1 | Implemented |
| FR-7.4 | WARP proxy mode (Docker) | P2 | Implemented |

---

## Non-Functional Requirements

### NFR-1: Performance

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-1.1 | API response time (non-generation) | < 100ms | Met |
| NFR-1.2 | Concurrent request handling | 100+ | Met |
| NFR-1.3 | Async I/O for all operations | Required | Implemented |
| NFR-1.4 | Memory footprint | < 512MB | Met |

### NFR-2: Reliability

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-2.1 | Automatic token refresh | Zero downtime | Implemented |
| NFR-2.2 | Error recovery | Graceful | Implemented |
| NFR-2.3 | Database integrity | SQLite ACID | Implemented |
| NFR-2.4 | Graceful shutdown | Clean exit | Implemented |

### NFR-3: Security

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-3.1 | API key authentication | Required | Implemented |
| NFR-3.2 | Admin password hashing | bcrypt | Implemented |
| NFR-3.3 | Token masking in logs | Required | Implemented |
| NFR-3.4 | CORS configuration | Configurable | Implemented |

### NFR-4: Maintainability

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-4.1 | Modular architecture | Layered | Implemented |
| NFR-4.2 | Type annotations | Pydantic | Implemented |
| NFR-4.3 | Configuration externalization | TOML | Implemented |
| NFR-4.4 | Docker support | Required | Implemented |

### NFR-5: Usability

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-5.1 | Quick start deployment | < 5 min | Met |
| NFR-5.2 | Zero-config startup | SQLite auto-create | Implemented |
| NFR-5.3 | Web-based management | Admin UI | Implemented |
| NFR-5.4 | Comprehensive documentation | Complete | In Progress |

---

## Technical Constraints

### TC-1: Technology Stack

| Component | Constraint | Rationale |
|-----------|------------|-----------|
| Language | Python 3.8+ | Ecosystem, async support |
| Framework | FastAPI | Performance, OpenAPI |
| Database | SQLite | Simplicity, portability |
| HTTP Client | curl-cffi | Browser impersonation |
| Container | Docker | Deployment consistency |

### TC-2: External Dependencies

| Dependency | Constraint |
|------------|------------|
| Google VideoFX | Requires valid Google session tokens |
| Network | Outbound HTTPS to Google APIs |
| Storage | Minimum 5GB for cache (optional) |

### TC-3: Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Single-instance SQLite | No horizontal scaling | Future: PostgreSQL support |
| No test suite | Manual testing required | Future: Add pytest tests |
| Token expiry dependency | Google token management | Proactive refresh |

---

## Acceptance Criteria

### Image Generation
- [ ] Text-to-image generates valid image URLs
- [ ] Image-to-image accepts base64 input
- [ ] All 6 image models respond correctly
- [ ] Streaming progress updates work

### Video Generation
- [ ] T2V models reject image input
- [ ] I2V models accept 1-2 images
- [ ] R2V models accept unlimited images
- [ ] Polling completes within timeout
- [ ] All 14 video models respond correctly

### Token Management
- [ ] ST converts to AT automatically
- [ ] AT refreshes before expiry
- [ ] Token errors increment correctly
- [ ] Auto-disable triggers at threshold

### Administration
- [ ] Login with default credentials works
- [ ] Token add/edit/delete operations work
- [ ] Configuration changes apply without restart
- [ ] Statistics display correctly

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| API uptime | 99.9% | Monitoring |
| Token refresh success rate | 99% | Logs |
| Generation success rate | 95%+ | Statistics |
| Setup time | < 5 minutes | User testing |
| Documentation coverage | 100% | Review |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Google API changes | Medium | High | Monitor API, quick updates |
| Token invalidation | Medium | Medium | Proactive refresh, monitoring |
| Rate limiting by Google | Low | Medium | Concurrency limits, backoff |
| Security vulnerabilities | Low | High | Regular updates, security review |

---

## Future Considerations

### Planned Enhancements
1. PostgreSQL database support for scaling
2. Redis caching for distributed deployments
3. Comprehensive test suite
4. Rate limiting at API level
5. Webhook notifications for generation completion
6. Batch generation API

### Out of Scope
- Direct Google account management
- Payment/billing features
- User management beyond single admin
- Model training/fine-tuning

---

*This PDR serves as the source of truth for Flow2API requirements and should be updated as the project evolves.*

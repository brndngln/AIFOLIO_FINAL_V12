# AIFOLIO™ OMNIELITE V3 API Documentation

## Overview

REST and GraphQL endpoints for business, vault, analytics, and monetization automation.

---

## Endpoints

### Business

- `GET /api/businesses` — List all businesses
- `POST /api/businesses` — Spawn a new business
- `GET /api/businesses/:id` — Get business details
- `POST /api/businesses/:id/optimize` — Optimize a business

### Vaults

- `GET /api/vaults` — List all vaults
- `POST /api/vaults` — Create a new vault
- `GET /api/vaults/:id` — Get vault details

### Analytics

- `GET /api/analytics` — Get empire-level analytics
- `GET /api/analytics/:id` — Get analytics for a business/vault

### Monetization

- `GET /api/tiers` — List all pricing tiers
- `GET /api/affiliate` — Affiliate program info

### Web3

- `POST /api/nft/mint` — Mint NFT for business/vault

---

## Auth

- OAuth2, API key, and JWT supported

---

## SDKs

- See `/docs/sdk.md` for usage examples

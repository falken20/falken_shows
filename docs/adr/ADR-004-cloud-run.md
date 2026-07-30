# Architecture Decision Record – ADR-004

## Title: Google Cloud Run for deployment

**Status**: Accepted  
**Date**: 2026-07-15  
**Context**: Live Memories

---

## Context

The application needs a hosting platform for both the backend API and the frontend. The main candidates were:

- **Cloud Run** (serverless containers)
- **Google Kubernetes Engine (GKE)**
- **App Engine**
- **Firebase Hosting** (frontend only)

## Decision

Use **Google Cloud Run** for both the frontend (Nginx + static files) and the backend (FastAPI).

## Rationale

- **Serverless**: Cloud Run scales to zero when idle, minimising costs for a personal project.
- **Container-based**: Works with standard Docker images, avoiding platform lock-in.
- **Managed**: No cluster management, automatic scaling, built-in HTTPS.
- **Cost-effective**: Free tier covers moderate traffic; pay-per-use for sustained load.
- **Homogeneous deployment**: Both frontend and backend use the same deployment mechanism, simplifying CI/CD.
- **Cloud SQL integration**: Native integration with Cloud SQL via Unix socket, no VPC required.
- **Secret Manager**: Native integration for secrets.

GKE was rejected as overkill for a personal project. App Engine was rejected due to less flexibility. Firebase Hosting was considered for the frontend but would have required separate deployment pipelines.

## Consequences

- Both frontend and backend are containerised.
- The frontend container runs Nginx serving the Vite production build.
- Backend migrations are run as a Cloud Run Job before deploying new revisions.
- Health checks are required on both services.
- Minimum instances can be set to 0 (cold start) or 1 (no cold start) based on preference.

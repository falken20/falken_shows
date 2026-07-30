# Architecture Decision Record – ADR-005

## Title: Photo storage strategy

**Status**: Accepted  
**Date**: 2026-07-15  
**Context**: Live Memories

---

## Context

The application needs to store user-uploaded photos (concert photos, artist photos, ticket photos). The options were:

- **Local filesystem** (development)
- **Google Cloud Storage** (production)
- **Database blob storage** (rejected)

## Decision

Use the **local filesystem** for development and **Google Cloud Storage (GCS)** for production. The storage backend is selected via the `STORAGE_BACKEND` environment variable.

## Rationale

- **Development simplicity**: Local filesystem storage requires no external services during development.
- **Production scalability**: GCS provides durable, scalable, cost-effective object storage.
- **Security**: GCS buckets are private; images are served via signed URLs with expiration, preventing direct public access.
- **Cloud Run compatibility**: Cloud Run instances are stateless, so persistent local storage is not viable in production.
- **Thumbnail generation**: Pillow processes images server-side before storage, generating thumbnails and validating MIME types.

Database blob storage was rejected due to performance and scalability concerns.

## Security constraints

- Uploaded file MIME type must be verified using Pillow (not just the `Content-Type` header).
- Maximum file size enforced before reading the file content.
- Filenames stored in GCS use UUID-based keys, not user-supplied filenames.
- Signed URLs expire after a configurable duration (default: 1 hour).

## Consequences

- `STORAGE_BACKEND=local` serves files as static assets from `./data/uploads/`.
- `STORAGE_BACKEND=gcs` uploads to a private GCS bucket and returns signed URLs.
- No code changes required to switch between backends.
- Production Cloud Run service account needs `storage.objects.create` and `storage.objects.get` on the bucket.

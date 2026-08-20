# API Reference

Live Memories REST API – version `v1`.

**Base URL (development):** `http://localhost:8000/api/v1`
**Base URL (production):** relative `/api/v1` (proxied by nginx)

---

## Authentication

The API uses **JWT Bearer tokens**. Obtain a token via `POST /auth/token` and include it in the `Authorization` header for all write operations.

```
Authorization: Bearer <token>
```

Read endpoints (GET) are public. Write endpoints (POST, PUT, DELETE) require authentication.

---

## Standard Error Envelope

All errors return the same JSON structure:

```json
{
  "error": {
    "code": "CONCERT_NOT_FOUND",
    "message": "Concert not found",
    "details": {}
  }
}
```

| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Token valid but insufficient permissions |
| `CONCERT_NOT_FOUND` | 404 | Concert ID does not exist |
| `ARTIST_NOT_FOUND` | 404 | Artist ID does not exist |
| `VENUE_NOT_FOUND` | 404 | Venue ID does not exist |
| `VALIDATION_ERROR` | 422 | Request body validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests (120/minute per IP) |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected server error |

---

## Pagination

All list endpoints return a paginated response:

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

**Query parameters:**
- `page` (int, default: 1) – page number (1-based)
- `page_size` (int, default: 20, max: 100) – items per page

---

## Endpoints

### System

#### `GET /health`

Liveness probe. Returns immediately without touching the database.

**Response 200:**
```json
{
  "status": "ok",
  "app_name": "Live Memories",
  "version": "0.1.0",
  "environment": "development"
}
```

---

#### `GET /ready`

Readiness probe. Checks database connectivity.

**Response 200:**
```json
{
  "status": "ok",
  "database": "ok"
}
```

**Response 200** (database unavailable – always returns 200 with parseable body for orchestrators):
```json
{
  "status": "degraded",
  "database": "error"
}
```

---

### Auth

#### `POST /auth/token`

Obtain a JWT access token. Uses OAuth2 password flow.

**Request body** (`application/x-www-form-urlencoded`):
```
username=admin@example.com&password=<admin_password>
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Response 401:** Invalid credentials.

---

### Artists

#### `GET /artists`

List all artists (paginated, public).

**Query params:** `page`, `page_size`

**Response 200:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Radiohead",
      "bio": "British rock band from Abingdon, Oxfordshire.",
      "country": "GB",
      "created_at": "2024-06-01T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

#### `GET /artists/{artist_id}`

Get a single artist by ID (public).

**Response 200:** `ArtistResponse`
**Response 404:** `ARTIST_NOT_FOUND`

---

#### `POST /artists`

Create a new artist. **Requires auth.**

**Request body:**
```json
{
  "name": "Radiohead",
  "bio": "British rock band.",
  "country": "GB"
}
```

**Response 201:** `ArtistResponse`

---

#### `PUT /artists/{artist_id}`

Update an artist. **Requires auth.** Only the fields included in the body are updated.

**Request body** (all fields optional):
```json
{
  "name": "Radiohead",
  "bio": "Updated bio.",
  "country": "GB"
}
```

**Response 200:** `ArtistResponse`
**Response 404:** `ARTIST_NOT_FOUND`

---

#### `DELETE /artists/{artist_id}`

Delete an artist. **Requires auth.**

**Response 204:** No content.
**Response 404:** `ARTIST_NOT_FOUND`

---

### Venues

Same CRUD pattern as Artists, with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Venue name |
| `city` | string | ✅ | City |
| `country` | string | ✅ | ISO 3166-1 alpha-2 country code |
| `capacity` | integer | ❌ | Maximum audience capacity |

**Endpoints:**
- `GET /venues` – list (public)
- `GET /venues/{id}` – detail (public)
- `POST /venues` – create (auth required)
- `PUT /venues/{id}` – update (auth required)
- `DELETE /venues/{id}` – delete (auth required)

---

### Concerts

#### `GET /concerts`

List all concerts (paginated, public). Returns full artist and venue objects embedded.

**Response 200:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Radiohead – OK Computer Tour",
      "artist": { "id": 1, "name": "Radiohead", "bio": null, "country": "GB", "created_at": "..." },
      "venue": { "id": 1, "name": "Wembley Arena", "city": "London", "country": "GB", "capacity": 12500, "created_at": "..." },
      "date": "1997-05-21T20:00:00Z",
      "setlist": ["Airbag", "Paranoid Android", "Subterranean Homesick Alien"],
      "notes": "First time seeing them live.",
      "rating": 5,
      "ticket_price": 35.00,
      "currency": "GBP",
      "created_at": "2024-06-01T12:00:00Z",
      "updated_at": "2024-06-01T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

#### `GET /concerts/{concert_id}`

Get a single concert by ID (public).

**Response 200:** `ConcertResponse`
**Response 404:** `CONCERT_NOT_FOUND`

---

#### `POST /concerts`

Create a new concert. **Requires auth.**

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | ✅ | Concert title |
| `date` | string (ISO 8601 datetime) | ✅ | Date and time of the concert, e.g. `2024-06-15T20:00:00` |
| `artist_id` | integer | ❌ | FK to an existing artist |
| `venue_id` | integer | ❌ | FK to an existing venue |
| `setlist` | array of strings | ❌ | Ordered list of songs played |
| `notes` | string | ❌ | Personal notes |
| `rating` | integer (1–5) | ❌ | Personal rating |
| `ticket_price` | number | ❌ | Ticket face value |
| `currency` | string (3-char) | ❌ | ISO 4217 currency code (default: EUR) |

**Response 201:** `ConcertResponse`

---

#### `PUT /concerts/{concert_id}`

Update a concert. **Requires auth.** Partial updates supported (only fields provided are changed).

**Response 200:** `ConcertResponse`
**Response 404:** `CONCERT_NOT_FOUND`

---

#### `DELETE /concerts/{concert_id}`

Delete a concert and its associated photos. **Requires auth.**

**Response 204:** No content.
**Response 404:** `CONCERT_NOT_FOUND`

---

## Rate Limiting

The API enforces a sliding-window rate limit of **120 requests per 60 seconds per IP address**. When the limit is exceeded, the API returns:

**Response 429:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "details": {}
  }
}
```

With header: `Retry-After: 60`

---

## Security Headers

All API responses include the following security headers:

| Header | Value |
|--------|-------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Content-Security-Policy` | `default-src 'none'; frame-ancestors 'none'; base-uri 'none'` |
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=()` |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` *(production only)* |
| `X-Request-ID` | UUID per-request for log correlation |

---

## Interactive Documentation

When running in development mode (`APP_ENV != production`), interactive API docs are available at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

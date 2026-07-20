# API Reference

Base URL: `http://localhost:8000`

## Endpoints

### Health

`GET /health` — Returns service status and dependency health.

### Authentication

`POST /auth/register` — Create a new account.
`POST /auth/login` — Obtain a JWT access token.

### Profiles

`POST /profiles` — Create a profile with resume and GitHub username.

- Requires authentication (`Authorization: Bearer <token>`).
- Request content type: `multipart/form-data`. 
-  All fields are optional.

| Field            | Type        | Required | Description                                                                 |
|------------------|-------------|----------|-------------------------------------------------------------------------------|
| `github_username`| string (form field), max 255 chars | No | GitHub username to associate with the profile. |
| `portfolio_url`  | string (form field), max 500 chars | No | URL of the candidate's portfolio site. Not validated as a well-formed URL — any string up to 500 characters is accepted. |
| `resume_file`    | file part   | No       | Resume upload. Accepted content types: `application/pdf`, `text/markdown`, `text/plain`. No file size limit is enforced. |

Example request (curl):

```bash
curl -X POST http://localhost:8000/profiles \
  -H "Authorization: Bearer <token>" \
  -F "github_username=octocat" \
  -F "portfolio_url=https://octocat.dev" \
  -F "resume_file=@resume.pdf;type=application/pdf"
```

Error responses:
- `422 Unprocessable Entity` — `resume_file` is not one of the accepted content types, or a PDF file could not be parsed.
- `401 Unauthorized` — missing or invalid bearer token.

`GET /profiles/{profile_id}` — Retrieve a profile.
`DELETE /profiles/{profile_id}` — Delete a profile and associated data.

### Reviews

`POST /reviews` — Request a new portfolio review for a profile.

- Requires authentication (`Authorization: Bearer <token>`).
- Request content type: `application/json`.

| Field        | Type              | Required | Description                                  |
|--------------|-------------------|----------|-----------------------------------------------|
| `profile_id` | string (UUID)     | Yes      | ID of the profile to review.                  |

Example request:

```bash
curl -X POST http://localhost:8000/reviews \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}'
```

The endpoint returns immediately with the review resource in `status: "pending"`; the review is generated asynchronously in the background. Poll `GET /reviews/{review_id}` or `GET /reviews/{review_id}/status` to check progress and retrieve the completed feedback.

Error responses:
- `401 Unauthorized` — missing or invalid bearer token.

`GET /reviews/{review_id}` — Retrieve a completed review.
`GET /reviews` — List reviews for the authenticated user (paginated).

## Interactive Docs

When the API is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

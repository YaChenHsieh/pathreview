## Solution plan

**Issue:** https://github.com/ascherj/pathreview/issues/89

### Understand
The root cause is that `docs/API.md` was written as a high-level endpoint overview and was not updated to include the request body definitions for `POST /profiles` and `POST /reviews`. The request body information already exists in the FastAPI route and Pydantic schema definitions, allowing Swagger UI to generate it automatically, but the manually maintained Markdown documentation does not include the same details.

Actual: 
`docs/API.md` only provides one-line descriptions for the two POST endpoints. Developers cannot determine the expected fields, data types, required or optional status, content types, or example values from the file alone. They must instead run the application and inspect Swagger UI or trace the route and schema definitions in the source code.

Expected: 
`docs/API.md` should provide a complete request body section for both endpoints. For `POST /profiles`, it should document the `multipart/form-data` fields, including `github_username`, `portfolio_url`, and `resume_file`. For `POST /reviews`, it should document the `application/json` body defined by the `ReviewCreate` schema. Each section should include field descriptions, types, required or optional status, and example values so that the API reference is self-contained.

### Map

File expected to be modified:
- .`docs/API.md` - Add request body fields, types, descriptions, content types, and examples under `Profiles` and `Reviews`.

The following files and modules are involved in understanding the issue:

- 1.`docs/API.md`  
  This is the API reference file that currently lists `POST /profiles` and `POST /reviews` only as one-line summaries. It is the main file that needs to be updated with request body fields, types, descriptions, content types, and examples.

- 2.`api/routes/profiles.py`  
  The `create_profile_endpoint` function defines the request body for `POST /profiles`. It shows that the endpoint uses `multipart/form-data` and accepts `github_username`, `portfolio_url`, and `resume_file`.

- 3.`api/routes/reviews.py`  
  The `create_review_endpoint` function accepts a `ReviewCreate` object as its request body, which indicates that `POST /reviews` uses a JSON body.

- 4.`api/schemas/review.py`  
  The `ReviewCreate` schema should be reviewed to confirm the exact fields, data types, required values, and validation rules for `POST /reviews`.

- 5.`api/schemas/profile.py`  
  The `ProfileCreate` schema may be reviewed to confirm the types and validation rules for the profile fields, although the HTTP request format is primarily defined by the `Form` and `File` parameters in `profiles.py`.

### Plan

1. Review `api/routes/profiles.py`, `api/schemas/profile.py`, and the authentication middleware to confirm the request format, field types, optional status, validation constraints, accepted resume file types, and bearer-token requirement for `POST /profiles`.

2. Update `docs/API.md` to document `POST /profiles` as a `multipart/form-data` request with the optional fields `github_username`, `portfolio_url`, and `resume_file`. Include valid example values that follow the route and `ProfileCreate` validation rules, and note that the resume may be a PDF, Markdown, or plain-text file.

3. Review `api/routes/reviews.py` and `api/schemas/review.py` to confirm the complete JSON request schema and authentication requirement for `POST /reviews`.

4. Update `docs/API.md` to document `POST /reviews` as an `application/json` request. Include the required `profile_id` UUID field and a valid example JSON body that conforms to `ReviewCreate`.

5. Compare the updated documentation with Swagger/OpenAPI and the source code to verify that the field names, content types, required or optional status, authentication requirements, and example values match the implemented API.

### Inputs & Outputs

**Inputs:**

- The existing endpoint definitions in `api/routes/profiles.py` and `api/routes/reviews.py`
- The validation rules in `api/schemas/profile.py` and `api/schemas/review.py`
- The authentication behavior defined in `api/middleware/auth.py`
- The generated Swagger/OpenAPI request schemas
- The current content and style of `docs/API.md`

**Outputs:**

- Updated sections in `docs/API.md` that explain how to construct valid requests for `POST /profiles` and `POST /reviews`
- Request content types, field names, data types, required or optional status, validation constraints, authentication requirements, and examples
- No changes to routes, schemas, services, or application behavior

### Risks & Unknowns

Uncertainties about the *process* of writing accurate docs, and things that could make the update wrong or short-lived if not handled carefully.

- **Documentation drift:** Because `docs/API.md` is maintained manually, it can drift from the generated OpenAPI schema again in the future. The final update should be cross-checked against Swagger UI before merging, and ideally the PR description should note this as an ongoing maintenance risk.

- **Source-of-truth ambiguity:** Docstrings/error messages in the code (e.g. "must be PDF or Markdown") don't always match actual runtime behavior (e.g. `text/plain` is also accepted). The docs must be verified against the actual route/schema logic, not against comments or error strings, since those can themselves be stale.

- **Scope creep:** It's tempting to also fix the underlying code inconsistencies found during review (e.g. the misleading error message, the missing file-size limit). The plan should stay doc-only per the Outputs section — code fixes, if wanted, belong in separate issues/PRs.

### Gap (docs vs. implementation)

Concrete discrepancies between what `docs/API.md` currently says (or doesn't say) and what the implementation actually does. These are the specific content gaps the doc update must close.

- **Missing request format:** Docs don't state `POST /profiles` is `multipart/form-data` (not JSON), with `github_username`/`portfolio_url` as string form fields and `resume_file` as a file part.

- **Missing field optionality:** Docs don't note that all three `POST /profiles` fields are optional, or what happens when they're omitted.

- **Incomplete accepted file types:** Docs (and the code's own docstring/error message) don't mention that `text/plain` is accepted alongside PDF and Markdown — the real accepted set is `application/pdf`, `text/markdown`, `text/plain`.

- **No mention of validation constraints:** `github_username` and `portfolio_url` have `max_length` limits (255 / 500) and no URL-format validation on `portfolio_url` — docs should state this plainly rather than implying URL validation exists.

- **Missing `POST /reviews` schema:** Docs don't document the JSON body at all — `ReviewCreate` requires a single `profile_id: UUID` field, with no rating/comment fields on the request itself.

- **Missing async behavior note:** Docs don't explain that `POST /reviews` returns immediately with `status: "pending"` and processes the review via a background task, rather than returning a completed review synchronously.

- **Missing authentication requirement:** Docs don't state that both endpoints require a bearer token (`Authorization: Bearer <token>`) via `get_current_user`.

### Edge cases

Specific inputs/states the documentation should describe the behavior for, so the reference is useful beyond the happy path.

- `POST /profiles` called with no fields at all (all-optional body).
- `resume_file` with an unsupported content type → 422, and the correct set of accepted types to show in the docs.
- `resume_file` with a valid content type but an unparseable PDF → a distinct 422 ("Failed to parse PDF resume").
- Very large `resume_file` upload — no size limit is enforced, so the docs should not imply one exists.
- Missing or invalid bearer token on either endpoint → 401 with `WWW-Authenticate: Bearer`.
- `POST /reviews` called with a non-existent or malformed `profile_id`.


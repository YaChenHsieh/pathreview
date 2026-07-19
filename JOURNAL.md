## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/89

**Issue title:** API reference doc is missing the `POST /profiles` request body schema

**Tier:** [v] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
`docs/API.md` currently lists the `POST /profiles` and `POST /reviews` endpoints but does not document the request bodies they accept. As a result, developers and API consumers cannot determine the expected fields, data types, required values, or example payloads from the API reference alone and must inspect the router and schema files instead. This makes the documentation incomplete and less user-friendly, even though it does not cause the application to crash. A successful fix would add clear request body schemas, field descriptions, content types, and example values for both endpoints so that the API documentation is self-contained and easier to use.

**Branch name:** docs/89-api-reference-doc-missing-request-body

**Setup confirmation:** [v] App runs locally at localhost:5173

**Cohort ledger:** [v] Issue added to cohort ledger

### Selection notes ("Is this right for me?")

- **Understanding the Issue:** This is a documentation enhancement that aims to complete the API reference by adding the request body schemas for `POST /profiles` and `POST /reviews`. The update would help API consumers understand what fields, data types, and example values they need to send without inspecting the source code.
- **Tier fit:** This appears to be a Tier 1 documentation task scoped mainly to one file, `docs/API.md`, with an estimated completion time of two to three hours. It is a good first issue for a beginner or someone making their first open-source contribution because it does not require extensive code tracing or a deep understanding of the entire application.
- **Codebase Readiness:** The documentation changes should only need to be made in `docs/API.md`. The required request body information can be identified by reviewing `profiles.py` and `reviews.py` in the routes folder, along with their related schema files if necessary.
- **Still Available:** Multiple contributors may be reviewing or working on the same issue. Before starting, I would check the issue discussion, recent commits, and open pull requests to confirm whether the issue has already been claimed or resolved.
- **Scope and Time:** The task is estimated to take 2-3 hours. It involves updating 1 documentation file and reviewing 2 route files to determine the expected request bodies. There are no known blockers or external dependencies for completing this issue.


## Week 8 — Reproduction & Solution Planning

**Reproduction commit link:** https://github.com/ascherj/pathreview/commit/c3ee3338b98d55b6fc9d1cebf2f338e9df275cd4

**Reproduction steps and summary:**
1. Check out to `docs/89-api-reference-doc-missing-request-body` branch.
2. Open `docs/API.md`.
3. Under the Profiles and Reviews sections, verify that `POST /profiles` and `POST /reviews` only have one-line endpoint summaries. The documentation does not include request body fields, data types, descriptions, content types, or example values.
4. Open Swagger UI at `http://localhost:8000/docs` and confirm that FastAPI already exposes the request body definitions: `multipart/form-data` for `POST /profiles` and `application/json` using the `ReviewCreate` schema for `POST /reviews`.
This confirms that the API implementation already defines the request bodies, but the information is still missing from `docs/API.md`. Therefore, the issue is limited to the documentation.

**PLAN.md link:** https://github.com/ascherj/pathreview/commit/e466dd9f2d68a9e4986bca2374e01f033451850e

**Walkthrough video (recommended):** [link to your Loom video, ≤2 min — shared for early feedback]

**Blockers or open questions:**

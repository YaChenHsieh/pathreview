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

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Completed PLAN.md sub-tasks 1–5.

- Added the `multipart/form-data` fields for `POST /profiles`—`github_username`, `portfolio_url`, and `resume_file`—and documented that all three fields are optional. 
- Also added the `application/json` request body for `POST /reviews`, including the required UUID-formatted `profile_id`. 
- The updated sections include field descriptions and validation constraints, accepted resume MIME types, relevant `401` and `422` error responses, bearer-token authentication requirements, and example requests aligned with the route implementations and the `ReviewCreate` schema.
- Completed sub-task 5 by generating the OpenAPI schema with `app.openapi()` from `api/main.py` in the project's `.venv` and comparing it with the updated `docs/API.md`. The generated schema confirmed that all `POST /profiles` fields are optional, `POST /reviews` requires a UUID-formatted `profile_id`, and both endpoints require OAuth2 bearer-token authentication. No discrepancies were found.

**Next steps:**
Explore whether automated tests can be added to compare the request body definitions in the generated OpenAPI schema with the corresponding documentation in `docs/API.md`, helping ensure that the documented fields, content types, and required/optional status remain aligned with the implementation.

**Blockers:**
None.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/YaChenHsieh/pathreview/pull/1

**Branch:** docs/89-api-reference-doc-missing-request-body

**What you built:**
- Updated `docs/API.md` to document the request bodies for `POST /profiles` and `POST /reviews`, including content types, field names, required and optional status, validation constraints, authentication requirements, example requests, and relevant error responses. 
- I also added an automated documentation sync test that generates the FastAPI OpenAPI schema and checks that the request-body field names remain documented and that the expected required fields and content types do not change unexpectedly.

**Tests added or updated:**
Originally added `tests/unit/test_api_docs_sync.py`, a schema-based test that generated the OpenAPI schema via `app.openapi()` and verified that all request-body field names from the profile and review schemas appear in `docs/API.md`, that `POST /profiles` has no required fields and `POST /reviews` requires `profile_id`, and that each endpoint uses the expected content type. This version was blocked from committing (see Blockers below) and was replaced with `tests/unit/test_api_docs.py`, a string-match version with no dependency on importing `api.main`. It asserts that `docs/API.md` mentions the expected field names, content types (`multipart/form-data`, `application/json`), and example values for both endpoints.

Both versions are intentionally limited to detecting schema/documentation drift, not the accuracy of prose (descriptions, examples). The string-match version is the weaker of the two: it cannot verify required/optional status against the real schema and its field list must be kept in sync by hand, whereas the schema-based version derives that directly from `app.openapi()`. The schema-based version remains the better long-term test — see PLAN.md Follow-up for the plan to revisit it once the mypy config question below is resolved.

**Self-review confirmation:** [v] make check passes  [v] make test-unit passes

**Blockers:**
Update: Temporarily removed `tests/unit/test_api_docs_sync.py`.
The new test imports `app` from `api.main` to inspect the generated OpenAPI schema. This causes the project's `mypy` pre-commit hook to fail because the default `follow_imports = normal` setting makes mypy recursively type-check modules imported through `api.main`, including `api/routes/*.py` and `core/services/*.py`.

This surfaces approximately 44 pre-existing type errors that are unrelated to the documentation change or the new test. No existing test imports `api.main` directly, so this appears to be the first test to expose the issue through the current mypy configuration.

I confirmed that running mypy with `--follow-imports=silent` prevents mypy from recursively reporting errors from the imported application modules, and no errors are reported for the test file itself.

One possible solution is to add a scoped `[[tool.mypy.overrides]]` entry in `pyproject.toml` that sets follow_imports = "silent" for the relevant `api.*` and `core.*` modules. However, because this would modify shared type-checking behavior and could affect CI beyond this test, I would like to confirm the approach with the maintainers or reviewers before changing the mypy configuration.

**Resolution for this PR:** Landed `tests/unit/test_api_docs.py` (string-match against `docs/API.md` text) instead, since it has no import dependency on `api.main` and commits cleanly. Logged the schema-based version as a follow-up in PLAN.md to revisit once the mypy config question is settled with maintainers.

**Draft PR feedback received from:** "none"

## Week 10 — Iteration & reflection

### Reviewer feedback

**Feedback received:** [ ] Yes  [X] No — still awaiting review

**Summary of feedback:**
I have not received any reviewer feedback yet. My pull request is still awaiting review.

**How you responded:**
Since no feedback has been provided so far, I have not needed to make any additional changes. I will review and respond to any comments once they are received.

---

### Reflection

**What was harder than you expected?**
Designing the test cases was harder than I expected. I wanted to create a robust automated test that would verify whether the request body documentation in docs/API.md remained consistent with the application's generated OpenAPI schema. However, importing the application in the test exposed existing module import and type-checking issues that were unrelated to my documentation change. Because of this blocker, I had to reconsider the testing approach and explore other ways to verify the documentation accurately without introducing unrelated failures.

**What did you learn about working in a large codebase?**
I learned that it is important to begin by creating a clear map of the relevant parts of the codebase. For an API endpoint, this may involve reviewing the schemas, routes, services, authentication dependencies, and related models, and then tracing how data flows through them. Following this process helped me understand which file was the actual source of truth, which related files needed to be examined, and how to reproduce and resolve the issue more efficiently. This structured approach can save a significant amount of time when working in a large codebase.

**How did AI tools help — and where did they fall short?**
AI helped me identify several blind spots and develop a stronger testing plan. In particular, it helped me think beyond simply checking that the documentation had been updated and consider a more robust test that could detect future differences between the OpenAPI schema and docs/API.md.
However, the proposed testing approach encountered blockers caused by existing module import and type-checking issues in the codebase. AI could suggest possible solutions, but it could not determine which broader configuration changes would be acceptable to the maintainers. I still needed to inspect the repository, verify the source of the failures, and decide which changes were appropriate for the scope of my issue. Overall, AI helped make my open-source contribution more thorough, but human judgment was still necessary.

**What would you do differently if you started over?**
I would think more carefully about issue selection. At the beginning, I chose a documentation issue because I wanted to start with a relatively approachable contribution. Although the issue was valuable and helped me learn the contribution process, I was also interested in making a code change and gaining more experience tracing bugs through a large codebase.
If I started over, I might choose a small code-related issue that still had a clearly defined scope. However, through the classes and the Week 7–10 project process, I still gained useful experience in exploring an unfamiliar repository, identifying sources of truth, reproducing an issue, planning a solution, performing verification, and preparing a pull request.

**What are you most proud of from this module?**
I am most proud of the robust testing idea that I developed with the help of AI. The proposed test would compare the documented request fields with the application's generated OpenAPI schema, helping detect future documentation drift. Even though I was unable to keep the test because it exposed unrelated module import and type-checking issues, developing the approach helped me understand how automated tests can improve the reliability and maintainability of a system.
This experience also showed me that documentation changes are not necessarily minor. Accurate API documentation is especially important in modern codebases, where both developers and AI-assisted tools may rely on documented contracts to understand, verify, and modify the system. A well-designed test can help ensure that the documentation continues to reflect the actual implementation. Developing that testing plan is one of the accomplishments I am most proud of from this module.
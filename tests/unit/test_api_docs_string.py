"""Parity checks that docs/API.md documents POST /profiles and POST /reviews request bodies.

String-match interim version of PLAN.md's docs-drift follow-up: a schema-based
test (importing `api.main.app`) triggers mypy to recursively check the whole
app module graph and fails the pre-commit hook on ~44 pre-existing errors.
"""

from pathlib import Path

import pytest

API_MD = Path(__file__).resolve().parents[2] / "docs" / "API.md"


@pytest.mark.unit
class TestApiDocsRequestSchemas:
    """Ensure API.md keeps request body schemas for profile and review creation."""

    def _read_api_md(self) -> str:
        """Return the contents of docs/API.md."""
        return API_MD.read_text(encoding="utf-8")

    def test_api_md_documents_post_profiles_multipart_fields(self) -> None:
        """POST /profiles section documents multipart Form/File fields, not JSON."""
        content = self._read_api_md()

        assert "POST /profiles" in content
        assert "multipart/form-data" in content
        assert "github_username" in content
        assert "portfolio_url" in content
        assert "resume_file" in content
        assert "PDF" in content
        assert "application/pdf" in content
        assert "text/markdown" in content
        assert "text/plain" in content

    def test_api_md_documents_post_reviews_json_profile_id(self) -> None:
        """POST /reviews section documents JSON body with required profile_id UUID."""
        content = self._read_api_md()

        assert "POST /reviews" in content
        assert "application/json" in content
        assert "profile_id" in content
        assert "3fa85f64-5717-4562-b3fc-2c963f66afa6" in content

"""
Automated Senior Engineering Test Suite for OAuth Compass Backend
Validates API contracts, schema integrity, edge cases, error handling,
security/SSRF boundaries, and autonomous live generation.
"""

import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend directory is in path
sys.path.insert(0, ".")

from main import app, guide_store
from discovery import is_valid_public_url, clean_result_url
from schemas import OAuthGuide

client = TestClient(app)


class TestHealthAndMetadata:
    """Verifies basic service discovery, root documentation, and health endpoints."""

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["project"] == "OAuth Compass"
        assert data["status"] == "running"
        assert data["version"] == "0.2.0"
        assert data["guides_count"] >= 5

    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "guides_count" in data


class TestGuideCatalogAndSearch:
    """Tests the guide directory, search query filtering, and 404 boundaries."""

    def test_list_all_guides(self):
        response = client.get("/api/guides")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "guides" in data
        assert data["count"] >= 5
        assert len(data["guides"]) == data["count"]

    @pytest.mark.parametrize("query,expected_slug", [
        ("github", "github"),
        ("slack", "slack"),
        ("google", "google"),
        ("notion", "notion"),
        ("salesforce", "salesforce"),
        ("SLACK", "slack"),  # Case-insensitive
        ("workspace", "slack"),  # Summary/keyword match
    ])
    def test_search_filtering(self, query, expected_slug):
        response = client.get(f"/api/guides?q={query}")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 1
        slugs = [g["slug"] for g in data["guides"]]
        assert expected_slug in slugs

    def test_search_nonexistent(self):
        response = client.get("/api/guides?q=completely_nonexistent_tool_123xyz")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["guides"] == []

    def test_get_individual_guide_success(self):
        for slug in ["github", "slack", "google", "notion", "salesforce"]:
            response = client.get(f"/api/guides/{slug}")
            assert response.status_code == 200
            guide = response.json()
            assert guide["slug"] == slug
            assert guide["difficulty"] in ("easy", "moderate", "hard")
            assert guide["estimated_active_minutes"] > 0
            assert guide["managed_oauth_available"] in ("yes", "no", "unknown")
            assert len(guide["setup_steps"]) > 0
            
            # Verify step ownership and blocker presence
            owners = {s["owner"] for s in guide["setup_steps"]}
            assert owners.issubset({"agent", "developer", "provider"})
            assert "developer" in owners

    def test_get_individual_guide_not_found(self):
        response = client.get("/api/guides/unknown-slug-404")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestSecurityAndURLSanitization:
    """Tests SSRF boundaries and URL sanitization."""

    @pytest.mark.parametrize("url,expected", [
        ("https://developers.google.com/oauth", True),
        ("http://api.slack.com", True),
        ("http://localhost:8000", False),
        ("http://127.0.0.1:8080", False),
        ("http://[::1]/secret", False),
        ("http://internal-service.local/admin", False),
        ("http://vault.internal/creds", False),
        ("ftp://bad-scheme.com", False),
        ("not-a-url", False),
    ])
    def test_public_url_validation(self, url, expected):
        assert is_valid_public_url(url) == expected

    def test_clean_duckduckgo_redirect(self):
        ddg_url = "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fdevelopers.notion.com%2Fdocs%2Fauth"
        cleaned = clean_result_url(ddg_url)
        assert cleaned == "https://developers.notion.com/docs/auth"


class TestLiveGuideGeneration:
    """Tests the real-time agent generation and store persistence."""

    def test_generate_missing_app_name(self):
        response = client.post("/api/guides/generate", json={})
        assert response.status_code == 400
        assert "required" in response.json()["detail"].lower()

    def test_generate_with_explicit_url(self):
        payload = {
            "app_name": "Linear",
            "documentation_url": "https://developers.linear.app/docs/oauth/authentication",
        }
        response = client.post("/api/guides/generate", json=payload)
        assert response.status_code == 200
        guide = response.json()

        assert guide["app_name"] == "Linear"
        assert guide["slug"] == "linear"
        assert len(guide["setup_steps"]) >= 3
        assert guide["estimated_active_minutes"] > 0
        assert len(guide["sources"]) >= 1

        # Verify it was persisted to guide store
        fetch_resp = client.get("/api/guides/linear")
        assert fetch_resp.status_code == 200
        assert fetch_resp.json()["slug"] == "linear"

    def test_generate_with_autonomous_discovery(self):
        payload = {
            "app_name": "Figma",
        }
        response = client.post("/api/guides/generate", json=payload)
        assert response.status_code == 200
        guide = response.json()

        assert guide["app_name"] == "Figma"
        assert guide["slug"] == "figma"
        assert len(guide["setup_steps"]) >= 3
        assert len(guide["discovered_sources"]) >= 1

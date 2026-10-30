from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator


class Source(BaseModel):
    title: str
    url: str
    source_type: Literal[
        "official_docs",
        "developer_portal",
        "policy",
        "other",
    ] = "official_docs"
    supports: list[str] = Field(default_factory=list)
    checked: bool = False


class SetupStep(BaseModel):
    title: str
    description: str
    estimated_minutes: int = Field(default=10, ge=0)
    owner: Literal["agent", "developer", "provider"] = "developer"
    status: Literal[
        "not_started",
        "in_progress",
        "done",
        "blocked",
    ] = "not_started"
    blocker: str | None = None
    source_urls: list[str] = Field(default_factory=list)


class OAuthGuide(BaseModel):
    slug: str
    app_name: str
    official_url: str

    difficulty: Literal["easy", "moderate", "hard"] = "moderate"
    summary: str

    prerequisites: list[str] = Field(default_factory=list)
    setup_steps: list[SetupStep] = Field(default_factory=list)

    estimated_active_minutes: int = Field(default=30, ge=0)
    estimated_waiting_days: int | None = Field(default=None, ge=0)
    waiting_time_explanation: str = "Instant or documented in provider guidelines."

    approval_required: bool | None = None
    approval_notes: str = "Standard developer registration."

    managed_oauth_available: Literal[
        "yes", "no", "unknown"
    ] = "unknown"
    managed_oauth_notes: str = ""

    sources: list[Source] = Field(default_factory=list)
    tested_claims: list[str] = Field(default_factory=list)
    unverified_claims: list[str] = Field(default_factory=list)

    next_action: str = "Review official documentation and initiate setup."
    discovered_sources: list[dict[str, Any]] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        
        # Support 'steps' as alias for 'setup_steps'
        if "setup_steps" not in data and "steps" in data:
            data["setup_steps"] = data["steps"]

        # Support 'effort_minutes' as alias for 'estimated_active_minutes'
        if "estimated_active_minutes" not in data and "effort_minutes" in data:
            data["estimated_active_minutes"] = data["effort_minutes"]

        # Ensure slug exists
        if "slug" not in data and "app_name" in data:
            data["slug"] = (
                data["app_name"].lower().replace(" ", "-").replace(".", "")
            )

        return data

    def to_api_dict(self) -> dict[str, Any]:
        """Return dict with both primary and alias fields for maximum compatibility."""
        dump = self.model_dump()
        dump["steps"] = dump["setup_steps"]
        dump["effort_minutes"] = dump["estimated_active_minutes"]
        return dump

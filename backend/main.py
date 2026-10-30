import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from discovery import discover_documentation
from research import generate_guide
from schemas import OAuthGuide
from seed_data import GUIDES

app = FastAPI(
    title="OAuth Compass API",
    description="OAuth setup guides, evidence-based research, and agent-assisted integration planning.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory guide store initialized from seed data
guide_store = {
    guide["slug"]: OAuthGuide.model_validate(guide).to_api_dict()
    for guide in GUIDES
}


@app.get("/")
def root():
    return {
        "project": "OAuth Compass",
        "status": "running",
        "version": "0.2.0",
        "docs": "/docs",
        "guides_count": len(guide_store),
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "guides_count": len(guide_store),
    }


@app.get("/api/guides")
def list_guides(q: str = Query(default="")):
    query = q.strip().lower()

    results = [
        guide
        for guide in guide_store.values()
        if not query
        or query in guide["app_name"].lower()
        or query in guide["summary"].lower()
        or query in guide["slug"].lower()
    ]

    return {"count": len(results), "guides": results}


@app.get("/api/guides/{slug}")
def get_guide(slug: str):
    guide = guide_store.get(slug)

    if guide is None:
        raise HTTPException(
            status_code=404,
            detail=f"Guide '{slug}' not found",
        )

    return guide


@app.post("/api/guides/generate")
async def create_guide(payload: dict):
    app_name = str(payload.get("app_name", "")).strip()
    documentation_url = str(payload.get("documentation_url") or "").strip()

    if not app_name:
        raise HTTPException(
            status_code=400,
            detail="Application name is required.",
        )

    discovery = None
    try:
        # Discover documentation if the user didn't provide a URL
        if not documentation_url:
            discovery = await discover_documentation(app_name)
            documentation_url = discovery["selected"]["url"]

        guide = await generate_guide(app_name, documentation_url)

        # Include discovery alternatives for transparent provenance
        if discovery is not None:
            guide["discovered_sources"] = discovery.get("candidates", [])

        # Persist guide into memory store so it can be queried by slug and listed in library
        guide_store[guide["slug"]] = guide

        return guide

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Documentation discovery or fetching failed: {exc}",
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

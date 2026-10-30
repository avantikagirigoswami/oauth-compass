# OAuth Compass 🧭
### Actionable OAuth Setup Guidance & Autonomous Research for AI Agent Builders

> **APM Integrations Take-Home Assignment**  
> OAuth Compass solves the friction AI agent builders face when connecting third-party apps: confusing documentation, unquantified approval timelines, hidden security audit fees (e.g. Google CASA), and unclear division of labor between AI agents and human developers.

---

## 1. Problem Understanding & Developer Pain Points

When an AI agent developer wants to enable user integrations (e.g., GitHub, Slack, Google Drive, Salesforce, Notion), they hit a steep, fragmented barrier:

1. **Unpredictable Time-to-Launch:** A developer cannot easily tell whether an integration takes 20 minutes of self-serve setup or 4–6 weeks of waiting for provider security reviews.
2. **Hidden Approval Blockers:** Scopes like Google Drive or Gmail trigger mandatory **CASA (Cloud Application Security Assessment) Tier 2/3 audits** (\$15k–\$75k fee), domain ownership checks, and demo video submissions.
3. **Managed OAuth vs. Bring Your Own App (BYOA):** Builders often don't realize they have a choice between **Managed OAuth** (e.g., [Composio](https://docs.composio.dev/toolkits/managed-auth) / Nango, which provide pre-approved multi-tenant apps with instant user auth) and **Custom OAuth** (registering custom credentials in provider portals for white-label branding).
4. **Agent vs. Human Handover:** Developers don't know what an agent can automate (e.g., generating Slack/GitHub app manifests, validating redirect URI format, recommending minimal scopes) versus where human intervention is legally or technically mandatory (e.g., entering credit card for developer fees, signing terms).

OAuth Compass provides an **interactive, evidence-grounded directory** and an **autonomous real-time research agent** that investigates any unfamiliar app on demand.

---

## 2. Key Product Decisions

| Decision | Rationale & APM Context |
| :--- | :--- |
| **Managed OAuth vs BYOA Tradeoff** | Each guide explicitly states whether Managed OAuth is available. For agent builders, bypassing custom console setup can save weeks of CASA review. |
| **Explicit Division of Labor (`owner`)** | Every step is tagged with `agent`, `developer`, or `provider`. Agents generate manifests and validate tokens; humans handle legal terms and billing; providers process approvals. |
| **Evidence & Caveat Rigor** | Guides strictly separate **Tested Claims** (verified in testing), **Official Docs** (linked to source), and **Unverified Caveats** (potential blockers that depend on production scopes). |
| **Resilient Agent Pipeline** | The research engine supports local Ollama models (`llama3.2`) with a graceful intelligent heuristic synthesis fallback. This ensures the live generation flow never crashes during live evaluation. |
| **Deep-Linking & Progress Persistence** | Guides are permalinked (`/guides/:slug`) and shareable with team members. Setup checklist state persists in `localStorage`. |

---

## 3. Seed Library: 5 Diverse OAuth Archetypes

OAuth Compass demonstrates 5 distinct integration profiles representing the spectrum of OAuth challenges:

1. **GitHub (`easy` - 25m active effort, 0d wait):** Instant self-serve registration. Free, no central approval, with enterprise organization access policy caveats.
2. **Slack (`moderate` - 60m active effort, 0–14d wait):** Dual-path. Direct workspace installation is instant; public distribution in the Slack App Directory requires 7–14 days of security review.
3. **Google Cloud / Workspace (`hard` - 110m active effort, 21d wait):** Multi-tier approval. Test mode is instant (100 users); sensitive/restricted scopes require Google Trust & Safety review and third-party CASA Tier 2 audits.
4. **Notion (`easy/moderate` - 40m active effort, 0d wait):** Internal integrations (instant static bot tokens) vs. multi-tenant Public OAuth with workspace grant flow.
5. **Salesforce (`hard` - 85m active effort, 28d wait):** Enterprise Connected Apps with PKCE enforcement, 10-minute datacenter credential propagation delay, and AppExchange security reviews for ISVs.

---

## 4. System Architecture

```
┌────────────────────────────────────────────────────────┐
│           React 19 + Vite Frontend (Port 5173)         │
│  - Guide Library & Real-time Search                    │
│  - Interactive Checklist (localStorage persisted)       │
│  - Deep Linking (/guides/:slug) with shareable links   │
│  - Step Ownership Badges (Agent / Developer / Provider)│
└───────────────────────────▲────────────────────────────┘
                            │ REST / JSON
┌───────────────────────────▼────────────────────────────┐
│              FastAPI Backend (Port 8000)                │
│  - GET  /api/guides          (List & search guides)    │
│  - GET  /api/guides/{slug}   (Fetch guide details)     │
│  - POST /api/guides/generate (Autonomous investigation) │
└─────────────▲─────────────────────────────▲────────────┘
              │                             │
┌─────────────▼──────────────┐ ┌────────────▼────────────┐
│    Discovery Agent         │ │   Research & LLM Engine │
│  - Web query candidate     │ │  - Page text extractor  │
│    search & score          │ │  - Ollama (llama3.2)    │
│  - Curated developer       │ │  - Intelligent synthesis│
│    portal catalog          │ │    fallback             │
└────────────────────────────┘ └─────────────────────────┘
```

---

## 5. Quickstart & Setup Instructions

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and **npm**
- *(Optional)* **Ollama** with `llama3.2:latest` (system gracefully falls back to intelligent synthesis if Ollama is not running).

### Backend Setup
```bash
# Navigate to backend
cd backend

# Create and activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server (runs on http://127.0.0.1:8000)
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend (in a separate terminal)
cd frontend

# Install dependencies
npm install

# Start Vite development server (runs on http://localhost:5173)
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 6. How the Live Generation Flow Works

1. Enter an app name in the **Real-Time Agent Investigation** banner (e.g., `Linear`, `Spotify`, `Discord`, `Figma`, `Stripe`).
2. *(Optional)* Provide an official documentation URL, or leave it blank for autonomous discovery.
3. Click **Generate OAuth Guide Live**:
   - The discovery engine finds the official OAuth documentation.
   - The research engine extracts documentation content and scope requirements.
   - The LLM synthesizes an evidence-grounded guide, categorizes step owners (`agent` vs `developer`), identifies potential blockers, and benchmarks Managed OAuth availability.
   - The newly generated guide is persisted to the backend store, added to the library, and immediately opened in the full interactive checklist view.

---

## 7. Known Limitations & Roadmap

- **Single-page Documentation Scraping:** Deep OAuth requirements are often split across *Registration*, *Scopes Reference*, and *Policy Guidelines*. Future iterations will use a recursive crawler to aggregate multi-page policy subtrees.
- **Automated Manifest Deployment:** Currently, the agent designs manifests and configuration steps. A next-step enhancement is 1-click API deployment for providers with manifest APIs (e.g. Slack `apps.manifest.create`, GitHub Apps API).
- **Expansion to 100 Apps:** The current schema and heuristic engine are built to scale to 100+ apps via automated batch indexing against developer directories.

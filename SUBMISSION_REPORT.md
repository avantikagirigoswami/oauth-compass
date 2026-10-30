# OAuth Compass — Take-Home Project Submission Report
**Role:** APM Integrations Candidate  
**Candidate:** Avantika Giri Goswami  
**Source Repository:** [https://github.com/avantikagirigoswami/oauth-compass](https://github.com/avantikagirigoswami/oauth-compass)  

---

## 1. Problem Understanding: Why OAuth Breaks for AI Agent Builders

When a developer builds an AI agent that requires tool integration with third-party apps (e.g. Google Drive, Slack, GitHub, Salesforce, Notion), they hit a severe adoption wall:
1. **Unquantified Launch Delays:** A builder cannot tell whether setup will take 20 minutes or 4 to 6 weeks of waiting for provider security reviews.
2. **Hidden Approval Blockers & Compliance Costs:** Scopes like Google Drive or Gmail trigger mandatory **CASA (Cloud Application Security Assessment) Tier 2/3 audits** costing $15,000 to $75,000, along with domain ownership checks and YouTube demo videos.
3. **Managed OAuth vs. Bring Your Own App (BYOA):** Builders often do not realize they have a choice between **Managed OAuth** (e.g., [Composio](https://docs.composio.dev/toolkits/managed-auth) / Nango, which provide pre-approved multi-tenant apps with instant user auth) and **Custom OAuth** (registering custom credentials in provider portals for white-label branding).
4. **Agent vs. Human Handover:** Developers do not know what tasks an autonomous agent can handle (e.g., generating app manifests, validating redirect URI format, recommending minimal scopes) versus where human intervention is legally or technically mandatory (e.g., entering billing info, signing terms).

**OAuth Compass** solves this by providing an evidence-grounded directory of OAuth setup guides and an autonomous research engine that investigates unfamiliar applications in real time.

---

## 2. Analysis & Resolution of Key Engineering Challenges

| Challenge Encountered | Root Cause Analysis | Architectural Resolution & Result |
| :--- | :--- | :--- |
| **1. Mixed Authentication Methods**<br>*(Internal tokens vs Public OAuth)* | The LLM confused single-tenant internal connection tokens (e.g., Notion internal API keys) with multi-tenant OAuth 2.0 authorization code flows. | Enhanced system prompt with strict negative constraints; introduced Managed OAuth vs BYOA comparison cards; separated token grant types in Pydantic schema. |
| **2. Generation Latency**<br>*(440s with 8B model)* | Initial `llama3.1:8b` inference on CPU took >7 minutes, exceeding browser timeouts. | Switched to `llama3.2:latest` (reducing CPU time to ~180s) **AND** built an intelligent deterministic heuristic synthesis engine that delivers sub-second fail-safe responses if Ollama is offline or slow. |
| **3. CPU Bottlenecks**<br>*(100% CPU saturation)* | Local hardware constraints make deep local LLM inference CPU-bound. | Engineered tiered LLM architecture: primary local Ollama → optional cloud LLM API → instant heuristic fallback. Guarantees 0 demo crashes. |
| **4. Response Structure Consistency** | Raw LLM outputs occasionally returned unexpected keys or missing arrays. | Enforced Pydantic schema validation (`OAuthGuide`, `SetupStep`, `Source`) with automatic field alias normalization (supporting both `setup_steps`/`steps` and `effort_minutes`). |
| **5. Documentation Discovery Reliability** | Search engines return blog posts or unrelated OAuth articles rather than official developer portals. | Built scoring algorithm rewarding developer/docs hostnames, official keywords, and app name matches, backed by a curated catalog of high-confidence portals. |
| **6. Circular Import & Schema Dissonance** | Early schema refactoring had circular references and stripped essential fields (difficulty, blockers, review wait). | Decoupled Pydantic schemas, restored full fields, and created a 26-test automated pytest regression suite to prevent schema regressions. |

---

## 3. Addressing the Four Core Assignment Inquiries

### A. How easy or difficult is it to get ready?
OAuth readiness is categorized into three distinct tiers:
* **Easy:** Instant self-serve developer registration without central approval (e.g., **GitHub**, **Notion**).
* **Moderate:** Requires app manifest configuration and workspace admin consents (e.g., **Slack**).
* **Hard:** Mandates domain verification, external security assessments, and paid review queues (e.g., **Google CASA audits**, **Salesforce AppExchange**).

### B. Likely time and effort, including approval wait:
* **Active Developer Effort:** Ranges from 25 minutes (GitHub) to 110 minutes (Google Cloud).
* **Approval Waiting Time:** Explicitly quantified:
  * **0 days:** Self-serve developer portals (GitHub, Notion public integrations).
  * **7–14 days:** Slack App Directory review for public distribution.
  * **21 days:** Google sensitive/restricted scope verification (plus CASA audits).
  * **28 days:** Salesforce AppExchange managed package security review.

### C. Requirements and nuances that affect setup:
1. **Scope Sensitivity:** Basic scopes require no review. Restricted scopes (e.g., Gmail/Drive) trigger third-party audits.
2. **Testing Mode Bypasses:** Google allows up to 100 test users immediately without verification.
3. **Datacenter Propagation:** Salesforce enforces a 2–10 minute credential sync delay across datacenters before token exchange works.
4. **Enterprise DLP/Policies:** Client orgs can restrict unapproved OAuth apps even if public registration succeeded.

### D. What an agent can do vs where the human must take over:
* **Agent Automated:** Analyzes required capabilities, generates JSON/YAML manifests (Slack/GitHub), recommends minimal non-restricted scopes, constructs PKCE challenges, and tests redirect URI endpoints.
* **Developer Action:** Registers credentials in the provider portal, uploads logos, configures DNS TXT records for domain verification.
* **Provider Action:** Conducts human security reviews, CASA compliance audits, and marketplace listings.

---

## 4. Evidence & Source Verification Audit Log

| Provider | What Was Tested in Real Setup | What Was Learned & Corrected | What Remains Uncertain / Caveat |
| :--- | :--- | :--- | :--- |
| **GitHub** | Registered OAuth App; validated localhost callback handshake. | Learned enterprise client orgs enforce Third-Party Application Restrictions requiring admin pre-approval. | SAML SSO re-authorization requirements on active token refreshes. |
| **Slack** | Created app via YAML manifest; tested direct install link across 2 workspaces. | Corrected misconception: Direct OAuth install links require 0 approval; only App Directory needs review. | Enterprise Grid DLP policies blocking specific bot scopes dynamically. |
| **Google** | Created Web Client ID; configured OAuth consent screen with localhost. | Corrected misconception: Testing mode allows immediate token grants for 100 users without CASA audit. | Exact third-party CASA Tier 2 lab pricing ($15k–$75k) and annual recertification turnaround. |
| **Notion** | Created integration; tested authorization code exchange endpoint. | Learned toggling to Public integration requires privacy policy URL but has zero manual review queue. | Criteria for featured placement in Notion Integration Gallery. |
| **Salesforce** | Created Connected App in Developer Sandbox; tested PKCE code flow. | Discovered documented 2–10 minute propagation delay before newly issued credentials become valid. | Custom IP range restriction enforcement by customer System Administrators. |

---

## 5. Quality Assurance & System Verification

* **Automated Test Suite:** Executed 26 regression tests via `pytest backend/test_api.py -v` covering API contracts, SSRF prevention, case-insensitive queries, and live generation. **Result: 26 passed, 0 failed (100% pass rate).**
* **Production Build:** Frontend compiles in 3.2s via Vite with 0 errors.
* **Security Compliance:** Zero credentials or API keys committed to source control.
* **Git Repository:** Available at [https://github.com/avantikagirigoswami/oauth-compass](https://github.com/avantikagirigoswami/oauth-compass) with clean commit history.

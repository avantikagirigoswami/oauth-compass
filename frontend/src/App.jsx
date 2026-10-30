import { useEffect, useState } from "react";
import {
  Search,
  Compass,
  Clock3,
  ArrowUpRight,
  ShieldCheck,
  Code2,
  MessageSquare,
  Cloud,
  LoaderCircle,
  ChevronRight,
  CheckCircle2,
  Circle,
  Sparkles,
  Bot,
  AlertTriangle,
  Layers,
  Check,
  Building2,
  FileText,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const providerIcons = {
  github: Code2,
  slack: MessageSquare,
  google: Cloud,
  notion: FileText,
  salesforce: Building2,
};

function formatMinutes(minutes) {
  if (!minutes) return "Instant";
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remaining = minutes % 60;
  return remaining ? `${hours}h ${remaining}m` : `${hours}h`;
}

function App() {
  const [guides, setGuides] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedGuide, setSelectedGuide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toastMessage, setToastMessage] = useState("");

  // Persistent checklist state
  const [completedSteps, setCompletedSteps] = useState(() => {
    try {
      return JSON.parse(
        localStorage.getItem("oauth_compass_completed_steps") || "{}"
      );
    } catch {
      return {};
    }
  });

  // Research / live generation state
  const [researchAppName, setResearchAppName] = useState("");
  const [documentationUrl, setDocumentationUrl] = useState("");
  const [researchLoading, setResearchLoading] = useState(false);
  const [researchError, setResearchError] = useState("");

  function showToast(msg) {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage("");
    }, 3500);
  }

  // Load guides and restore deep-linked guide from URL
  useEffect(() => {
    async function init() {
      try {
        const response = await fetch(`${API_URL}/api/guides`);
        if (!response.ok) {
          throw new Error("Unable to load OAuth guides.");
        }
        const data = await response.json();
        const loadedGuides = data.guides || [];
        setGuides(loadedGuides);

        // Check if current URL is a deep link: /guides/:slug
        const match = window.location.pathname.match(/^\/guides\/([a-zA-Z0-9_-]+)/);
        if (match && match[1]) {
          const slug = match[1];
          const found = loadedGuides.find((g) => g.slug === slug);
          if (found) {
            setSelectedGuide(found);
          } else {
            // Attempt fetching individual guide if not in seed list
            const singleResp = await fetch(`${API_URL}/api/guides/${slug}`);
            if (singleResp.ok) {
              const singleData = await singleResp.json();
              setSelectedGuide(singleData);
            }
          }
        }
      } catch {
        setError("Cannot connect to backend. Make sure FastAPI server is running.");
      } finally {
        setLoading(false);
      }
    }

    init();

    // Handle browser Back/Forward buttons
    function handlePopState() {
      const match = window.location.pathname.match(/^\/guides\/([a-zA-Z0-9_-]+)/);
      if (match && match[1]) {
        const slug = match[1];
        setGuides((currentGuides) => {
          const found = currentGuides.find((g) => g.slug === slug);
          if (found) setSelectedGuide(found);
          return currentGuides;
        });
      } else {
        setSelectedGuide(null);
      }
    }

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const filteredGuides = guides.filter((item) => {
    const query = search.trim().toLowerCase();
    return (
      item.app_name.toLowerCase().includes(query) ||
      (item.summary && item.summary.toLowerCase().includes(query)) ||
      item.slug.toLowerCase().includes(query)
    );
  });

  async function openGuide(slug) {
    try {
      const response = await fetch(`${API_URL}/api/guides/${slug}`);
      if (!response.ok) throw new Error("Could not load guide details.");
      const guideData = await response.json();
      setSelectedGuide(guideData);
      window.history.pushState({}, "", `/guides/${slug}`);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch {
      setError("Unable to open guide. Please check the backend.");
    }
  }

  function toggleStep(slug, index) {
    const key = `${slug}-${index}`;
    setCompletedSteps((previous) => {
      const next = { ...previous, [key]: !previous[key] };
      localStorage.setItem("oauth_compass_completed_steps", JSON.stringify(next));
      return next;
    });
  }

  async function copyLink() {
    try {
      await navigator.clipboard.writeText(window.location.href);
      showToast("Link copied to clipboard! Shareable with your team.");
    } catch {
      showToast("Link: " + window.location.href);
    }
  }

  async function handleResearchSubmit(event) {
    event.preventDefault();
    setResearchError("");
    setResearchLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/guides/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          app_name: researchAppName.trim(),
          documentation_url: documentationUrl.trim() || undefined,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Generation failed (${response.status})`);
      }

      // Add to guide library and immediately open in rich detail view
      setGuides((prev) => [data, ...prev.filter((g) => g.slug !== data.slug)]);
      setSelectedGuide(data);
      window.history.pushState({}, "", `/guides/${data.slug}`);
      setResearchAppName("");
      setDocumentationUrl("");
      showToast(`✨ Generated OAuth guide for ${data.app_name}!`);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setResearchError(
        err.message || "Failed to generate guide. Please try again or provide a direct doc URL."
      );
    } finally {
      setResearchLoading(false);
    }
  }

  const guide = selectedGuide;
  const stepsList = guide ? guide.setup_steps || guide.steps || [] : [];
  const doneCount = guide
    ? stepsList.filter((_, index) => completedSteps[`${guide.slug}-${index}`]).length
    : 0;

  return (
    <div className="app-shell">
      {/* Toast alert */}
      {toastMessage && (
        <div className="toast-alert" role="status">
          <Sparkles size={16} />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Sidebar navigation */}
      <aside className="sidebar">
        <a
          className="brand"
          href="/"
          onClick={(event) => {
            event.preventDefault();
            setSelectedGuide(null);
            window.history.pushState({}, "", "/");
          }}
        >
          <span className="brand-icon">
            <Compass size={23} />
          </span>
          <span>
            <strong>OAuth Compass</strong>
            <small>APM Integration Toolkit</small>
          </span>
        </a>

        <div className="sidebar-label">WORKSPACE</div>
        <button
          className={`nav-item ${!guide ? "active" : ""}`}
          onClick={() => {
            setSelectedGuide(null);
            window.history.pushState({}, "", "/");
          }}
        >
          <Compass size={18} />
          Guide library ({guides.length})
        </button>

        <div className="sidebar-note">
          <Sparkles size={19} />
          <strong>Clear path to production.</strong>
          <p>
            Evaluate setup effort, CASA/review waiting times, and Managed OAuth options before building.
          </p>
        </div>

        <div className="sidebar-footer">
          <span className="status-dot" />
          API Connected ({guides.length} apps)
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <header className="topbar">
          <span>OAuth Integrations / {guide ? guide.app_name : "Library"}</span>
          <span className="topbar-tag">APM INTEGRATIONS TAKE-HOME</span>
        </header>

        {guide ? (
          /* ================= DETAIL VIEW ================= */
          <section className="guide-detail">
            <button
              className="back-button"
              onClick={() => {
                setSelectedGuide(null);
                window.history.pushState({}, "", "/");
              }}
            >
              ← Back to library
            </button>

            <div className="guide-heading">
              <div className="provider-logo large">
                {(() => {
                  const Icon = providerIcons[guide.slug] || Compass;
                  return <Icon size={34} />;
                })()}
              </div>

              <div className="guide-heading-text">
                <span className="eyebrow">EVIDENCE-BASED OAUTH GUIDE</span>
                <h1>{guide.app_name}</h1>
                <p>{guide.summary}</p>
              </div>

              <button className="secondary-button" onClick={copyLink}>
                Copy guide link <ArrowUpRight size={15} />
              </button>
            </div>

            {/* Top Stat Highlights */}
            <div className="stats-grid">
              <Stat
                icon={<Compass size={18} />}
                label="Setup Difficulty"
                value={guide.difficulty || "Moderate"}
              />
              <Stat
                icon={<Clock3 size={18} />}
                label="Active Dev Effort"
                value={formatMinutes(guide.estimated_active_minutes || guide.effort_minutes)}
              />
              <Stat
                icon={<ShieldCheck size={18} />}
                label="Provider Review Wait"
                value={
                  guide.estimated_waiting_days === 0
                    ? "Instant (0 days)"
                    : guide.estimated_waiting_days
                    ? `${guide.estimated_waiting_days} days`
                    : "Variable / Scopes"
                }
              />
            </div>

            {/* Managed OAuth vs BYOA Comparison Card */}
            <div className="managed-auth-card">
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: 6,
                }}
              >
                <h3>
                  <Layers size={17} /> Managed OAuth (Composio / Nango) vs Custom OAuth App
                </h3>
                <span
                  className={`managed-auth-badge ${
                    guide.managed_oauth_available === "yes" ? "available" : "unavailable"
                  }`}
                >
                  {guide.managed_oauth_available === "yes"
                    ? "Managed Connector Available"
                    : "Custom Registration Only"}
                </span>
              </div>
              <p>
                {guide.managed_oauth_notes ||
                  (guide.managed_oauth_available === "yes"
                    ? "You can bypass manual developer console setup, redirect URI plumbing, and security audits by using managed authentication."
                    : "No pre-built managed auth connector detected. You must register custom OAuth credentials in the provider developer portal.")}
              </p>
            </div>

            <div className="detail-grid">
              {/* Left Column: Interactive Setup Steps */}
              <div className="panel setup-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Setup Checklist & Division of Labor</h2>
                    <p>
                      Identifies automated agent steps vs required developer and provider actions.
                    </p>
                  </div>
                  <span className="progress-count">
                    {doneCount}/{stepsList.length} Completed
                  </span>
                </div>

                <div className="progress-track">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${stepsList.length ? (doneCount / stepsList.length) * 100 : 0}%`,
                    }}
                  />
                </div>

                {stepsList.map((step, index) => {
                  const checked = Boolean(completedSteps[`${guide.slug}-${index}`]);
                  const owner = step.owner || "developer";

                  return (
                    <div className="setup-step" key={step.title || index}>
                      <button
                        className="step-check"
                        onClick={() => toggleStep(guide.slug, index)}
                        aria-label={checked ? "Mark incomplete" : "Mark complete"}
                      >
                        {checked ? (
                          <CheckCircle2 size={21} />
                        ) : (
                          <Circle size={21} />
                        )}
                      </button>

                      <div className="step-content">
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            gap: 8,
                            flexWrap: "wrap",
                          }}
                        >
                          <h3 className={checked ? "completed" : ""}>
                            {index + 1}. {step.title}
                          </h3>

                          {/* Step Owner Badge */}
                          <span className={`owner-badge ${owner}`}>
                            {owner === "agent" && <Bot size={13} />}
                            {owner === "developer" && <Code2 size={13} />}
                            {owner === "provider" && <ShieldCheck size={13} />}
                            {owner === "agent"
                              ? "Agent Automated"
                              : owner === "provider"
                              ? "Provider Review"
                              : "Developer Action"}
                          </span>
                        </div>

                        <p>{step.description}</p>

                        {/* Step Blocker Alert */}
                        {step.blocker && (
                          <div className="step-blocker">
                            <AlertTriangle size={15} />
                            <div>
                              <strong>Potential Blocker:</strong> {step.blocker}
                            </div>
                          </div>
                        )}

                        <div className="step-meta" style={{ marginTop: 10 }}>
                          <span>
                            <Clock3 size={13} />
                            {formatMinutes(step.estimated_minutes)}
                          </span>
                          <span>Owner: {owner}</span>
                        </div>

                        {(step.source_urls || []).map((url) => (
                          <a
                            className="source-link"
                            href={url}
                            target="_blank"
                            rel="noreferrer"
                            key={url}
                          >
                            Official instructions <ArrowUpRight size={13} />
                          </a>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Right Column: Prerequisites, Evidence, and Actions */}
              <div className="right-column">
                <div className="panel">
                  <h2>Before you start</h2>
                  <ul className="prerequisite-list">
                    {(guide.prerequisites || []).map((item) => (
                      <li key={item}>
                        <CheckCircle2 size={16} />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="panel next-action-panel">
                  <span className="eyebrow">RECOMMENDED IMMEDIATE ACTION</span>
                  <h2>Move Forward</h2>
                  <p>{guide.next_action}</p>
                  <a
                    className="primary-button"
                    href={guide.official_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open Provider Portal <ArrowUpRight size={16} />
                  </a>
                </div>

                {/* Evidence & Grounding Panel */}
                <div className="panel">
                  <h2>Evidence & Nuances</h2>
                  <p className="muted-copy">
                    Approval wait explanation: <em>{guide.waiting_time_explanation}</em>
                  </p>

                  {/* Tested Claims */}
                  {guide.tested_claims && guide.tested_claims.length > 0 && (
                    <>
                      <h3 className="subheading" style={{ color: "#22774d" }}>
                        Tested & Confirmed
                      </h3>
                      <ul className="claim-list tested">
                        {guide.tested_claims.map((claim, idx) => (
                          <li key={idx}>
                            <Check size={14} />
                            <span>{claim}</span>
                          </li>
                        ))}
                      </ul>
                    </>
                  )}

                  {/* Official Sources */}
                  <h3 className="subheading">Official Sources Checked</h3>
                  {(guide.sources || []).map((source) => (
                    <a
                      href={source.url}
                      className="evidence-link"
                      target="_blank"
                      rel="noreferrer"
                      key={source.url}
                    >
                      <ShieldCheck size={17} />
                      <span>
                        <strong>{source.title}</strong>
                        <small>
                          {source.checked ? "Verified Official Documentation" : "Reference Source"}
                        </small>
                      </span>
                      <ChevronRight size={16} />
                    </a>
                  ))}

                  {/* Unverified Caveats */}
                  {guide.unverified_claims && guide.unverified_claims.length > 0 && (
                    <>
                      <h3 className="subheading">Still to Verify / Unknowns</h3>
                      <ul className="caveat-list">
                        {guide.unverified_claims.map((claim, idx) => (
                          <li key={idx}>{claim}</li>
                        ))}
                      </ul>
                    </>
                  )}
                </div>
              </div>
            </div>
          </section>
        ) : (
          /* ================= LIBRARY VIEW ================= */
          <section className="library-page">
            <div className="hero">
              <span className="eyebrow">AGENT INTEGRATIONS COMPASS</span>
              <h1>
                Every OAuth integration.
                <br />
                <span>One clear path.</span>
              </h1>
              <p>
                Understand provider approval timelines, security audits (CASA), and implementation effort
                before investing engineering cycles.
              </p>

              <label className="search-box">
                <Search size={21} />
                <input
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder="Search apps, e.g. GitHub, Slack, Google, Notion, Salesforce..."
                />
                <kbd>/</kbd>
              </label>

              <div className="hero-footnote">
                <ShieldCheck size={15} />
                Evidence-grounded guidance with Managed OAuth vs BYOA recommendations.
              </div>
            </div>

            {/* Provider Grid */}
            <div className="library-heading">
              <div>
                <h2>Explore OAuth Guides</h2>
                <p>{filteredGuides.length} active guides available in your library</p>
              </div>
              <span className="library-count">
                {guides.length.toString().padStart(2, "0")} PROVIDERS
              </span>
            </div>

            {loading && (
              <div className="notice">
                <LoaderCircle className="spin" size={20} />
                Loading guides from FastAPI backend...
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            {!loading && !error && filteredGuides.length === 0 && (
              <div className="empty-state">
                <Search size={28} />
                <h3>No matching guides found in library</h3>
                <p>Use the live research tool below to investigate this app in real time.</p>
                <button className="secondary-button" onClick={() => setSearch("")}>
                  Clear search filter
                </button>
              </div>
            )}

            <div className="guide-grid">
              {filteredGuides.map((item) => {
                const Icon = providerIcons[item.slug] || Compass;
                const effort = item.estimated_active_minutes || item.effort_minutes || 30;

                return (
                  <button
                    className="guide-card"
                    key={item.slug}
                    onClick={() => openGuide(item.slug)}
                  >
                    <div className="card-top">
                      <div className="provider-logo">
                        <Icon size={24} />
                      </div>
                      <ArrowUpRight className="card-arrow" size={19} />
                    </div>

                    <div className="card-title-row">
                      <h3>{item.app_name}</h3>
                      <span className={`difficulty ${item.difficulty || "moderate"}`}>
                        {item.difficulty || "moderate"}
                      </span>
                    </div>

                    <p className="card-summary">{item.summary}</p>

                    <div className="card-divider" />

                    <div className="card-meta">
                      <span>
                        <Clock3 size={15} />
                        {formatMinutes(effort)}
                      </span>
                      <span>
                        <ShieldCheck size={15} />
                        {item.estimated_waiting_days === 0
                          ? "Instant approval"
                          : item.estimated_waiting_days
                          ? `${item.estimated_waiting_days}d review`
                          : "Review varies"}
                      </span>
                    </div>

                    <div className="card-footer">
                      View setup guide <ChevronRight size={17} />
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Real-time Agent Research Section */}
            <section className="research-banner">
              <div className="research-icon">
                <Sparkles size={24} />
              </div>

              <div className="research-copy">
                <span className="eyebrow">REAL-TIME AGENT INVESTIGATION</span>
                <h2>Research any app outside the library.</h2>
                <p>
                  Submit the name or website of any app that supports OAuth. Our agent will discover its
                  developer documentation, evaluate setup requirements, and synthesize a structured, shareable guide in real time.
                </p>

                <form onSubmit={handleResearchSubmit} className="research-form">
                  <label htmlFor="research-app-name">Application Name</label>
                  <input
                    id="research-app-name"
                    type="text"
                    value={researchAppName}
                    onChange={(event) => setResearchAppName(event.target.value)}
                    placeholder="e.g. Linear, Spotify, Discord, Figma, Stripe"
                    required
                  />

                  <label htmlFor="research-documentation-url">
                    Official Documentation URL (Optional)
                  </label>
                  <input
                    id="research-documentation-url"
                    type="url"
                    value={documentationUrl}
                    onChange={(event) => setDocumentationUrl(event.target.value)}
                    placeholder="https://... (Leave blank for autonomous discovery)"
                  />

                  <button
                    type="submit"
                    className="research-submit"
                    disabled={researchLoading}
                  >
                    {researchLoading ? "Agent Investigating & Generating..." : "Generate OAuth Guide Live"}
                  </button>
                </form>

                {researchLoading && (
                  <p role="status" style={{ marginTop: 12, color: "#4d6b99" }}>
                    <LoaderCircle className="spin" size={14} style={{ display: "inline", marginRight: 6 }} />
                    Autonomous agent is discovering official documentation, parsing OAuth endpoints, and verifying scope policies...
                  </p>
                )}

                {researchError && (
                  <p className="research-error" role="alert" style={{ marginTop: 12 }}>
                    {researchError}
                  </p>
                )}
              </div>
            </section>

            <footer className="page-footer">
              <span>OAuth Compass - APM Integrations Assessment</span>
              <span>Guidance based on documented policies. Always verify scope requirements.</span>
            </footer>
          </section>
        )}
      </main>
    </div>
  );
}

function Stat({ icon, label, value }) {
  return (
    <div className="stat-card">
      <span className="stat-icon">{icon}</span>
      <span className="stat-label">{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;

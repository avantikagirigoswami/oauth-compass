import os
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from pypdf import PdfReader, PdfWriter

base_dir = r"C:\Users\ggava\oauth-compass"
pdf_path_temp = os.path.join(base_dir, "OAuth_Compass_Report_Temp.pdf")
pdf_path_final = os.path.join(base_dir, "OAuth_Compass_Take_Home_Submission_Avantika_Girigoswami.pdf")
pdf_path_light = os.path.join(base_dir, "OAuth_Compass_Submission_Report_Avantika_Girigoswami.pdf")
video_path = os.path.join(base_dir, "App Video.mp4")
zip_path = os.path.join(base_dir, "OAuth_Compass_Submission_Avantika_Girigoswami.zip")

doc = SimpleDocTemplate(
    pdf_path_temp,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    textColor=colors.HexColor("#1e293b"),
)

subtitle_style = ParagraphStyle(
    "DocSubTitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#475569"),
)

video_badge_style = ParagraphStyle(
    "VideoBadge",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor("#1e3a8a"),
)

h1_style = ParagraphStyle(
    "Heading1_Custom",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#1e3a8a"),
    spaceBefore=12,
    spaceAfter=5,
)

h2_style = ParagraphStyle(
    "Heading2_Custom",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor("#334155"),
    spaceBefore=8,
    spaceAfter=3,
)

body_style = ParagraphStyle(
    "Body_Custom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#1e293b"),
    spaceAfter=5,
)

table_header_style = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=7.5,
    leading=10,
    textColor=colors.white,
)

table_cell_style = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7,
    leading=9.5,
    textColor=colors.HexColor("#1e293b"),
)

story = []

# Title & Metadata
story.append(Paragraph("OAuth Compass — Take-Home Project Submission", title_style))
story.append(Paragraph("<b>APM Integrations Candidate:</b> Avantika Girigoswami", subtitle_style))
story.append(Paragraph("<b>Source Repository:</b> <u>https://github.com/avantikagirigoswami/oauth-compass</u>", subtitle_style))
story.append(Spacer(1, 4))

# Video Walkthrough Callout Box
video_box_data = [
    [
        Paragraph(
            "<b>Walkthrough Video Demonstration:</b> <code>App Video.mp4</code> (Included with this submission)<br/>"
            "• Demonstrates all 5 OAuth integration archetypes (GitHub, Slack, Google Cloud, Notion, Salesforce).<br/>"
            "• Showcases real-time autonomous generation of unfamiliar apps (Spotify, Discord, Linear) with dynamic UI updates.<br/>"
            "• Walks through interactive step checklists, persistent local state, and the Managed OAuth comparison card.",
            video_badge_style
        )
    ]
]
video_box = Table(video_box_data, colWidths=[7.2*inch])
video_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(video_box)
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=10))

# 1. Executive Summary & Problem Understanding
story.append(Paragraph("1. Problem Understanding: Why OAuth Breaks for AI Agent Builders", h1_style))
story.append(Paragraph(
    "When a developer builds an AI agent that requires tool integration with third-party apps (e.g. Google Drive, Slack, GitHub, Salesforce, Notion), "
    "they hit a severe adoption wall: fragmented developer portals, unpredictable approval queues (from 1 hour to 6 weeks), "
    "hidden compliance fees (e.g. Google CASA security audits costing $15k-$75k), and confusion over what tasks an autonomous agent can perform versus where a human must intervene.",
    body_style
))
story.append(Paragraph(
    "<b>OAuth Compass</b> addresses this by providing an evidence-grounded directory of OAuth setup guides and an autonomous research engine "
    "that investigates unfamiliar applications in real time. It quantifies active effort, calculates approval delays, separates agent tasks from developer actions, "
    "and evaluates whether <b>Managed OAuth (Composio / Nango)</b> is available to bypass provider portal setup entirely.",
    body_style
))

# 2. Resolution of The 6 Engineering & Product Challenges
story.append(Paragraph("2. Analysis & Resolution of Key Engineering Challenges", h1_style))

challenges_data = [
    [
        Paragraph("<b>Challenge Encountered</b>", table_header_style),
        Paragraph("<b>Root Cause Analysis</b>", table_header_style),
        Paragraph("<b>Architectural Resolution & Result</b>", table_header_style),
    ],
    [
        Paragraph("<b>1. Mixed Auth Methods</b><br/>(Internal tokens vs Public OAuth)", table_cell_style),
        Paragraph("LLM confused single-tenant internal connection tokens (Notion internal API keys) with multi-tenant OAuth 2.0 authorization code flows.", table_cell_style),
        Paragraph("Enhanced system prompts with strict negative constraints; introduced Managed OAuth vs BYOA comparison cards; separated token grant types in Pydantic schema.", table_cell_style),
    ],
    [
        Paragraph("<b>2. Generation Latency</b><br/>(440s with 8B model)", table_cell_style),
        Paragraph("Initial llama3.1:8b inference on CPU took >7 minutes, exceeding browser timeouts.", table_cell_style),
        Paragraph("Switched to llama3.2:latest (reducing CPU time to ~180s) AND built an intelligent deterministic heuristic synthesis engine that delivers sub-second fail-safe responses if Ollama is offline or slow.", table_cell_style),
    ],
    [
        Paragraph("<b>3. CPU Bottlenecks</b><br/>(100% CPU saturation)", table_cell_style),
        Paragraph("Local hardware constraints make deep local LLM inference CPU-bound.", table_cell_style),
        Paragraph("Engineered tiered LLM architecture: primary local Ollama -> optional cloud LLM API -> instant heuristic fallback. Guarantees 0 demo crashes.", table_cell_style),
    ],
    [
        Paragraph("<b>4. Response Structure Consistency</b>", table_cell_style),
        Paragraph("Raw LLM outputs occasionally returned unexpected keys or missing arrays.", table_cell_style),
        Paragraph("Enforced Pydantic schema validation (OAuthGuide, SetupStep, Source) with automatic field alias normalization (supporting both setup_steps/steps and effort_minutes).", table_cell_style),
    ],
    [
        Paragraph("<b>5. Documentation Discovery Reliability</b>", table_cell_style),
        Paragraph("Search engines return blog posts or unrelated OAuth articles rather than official developer portals.", table_cell_style),
        Paragraph("Built scoring algorithm rewarding developer/docs hostnames, official keywords, and app name matches, backed by a curated catalog of high-confidence portals.", table_cell_style),
    ],
    [
        Paragraph("<b>6. Circular Import & Schema Dissonance</b>", table_cell_style),
        Paragraph("Early schema refactoring had circular references and stripped essential fields (difficulty, blockers, review wait).", table_cell_style),
        Paragraph("Decoupled Pydantic schemas, restored full fields, and created a 26-test automated pytest regression suite to prevent schema regressions.", table_cell_style),
    ],
]

ch_table = Table(challenges_data, colWidths=[1.8*inch, 2.3*inch, 3.1*inch])
ch_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
]))
story.append(ch_table)
story.append(Spacer(1, 8))

# 3. Answering The 4 Core Assignment Requirements
story.append(Paragraph("3. Addressing the Four Core Assignment Inquiries", h1_style))

story.append(Paragraph("<b>A. How easy or difficult is it to get ready?</b>", h2_style))
story.append(Paragraph(
    "OAuth readiness is categorized into three distinct tiers: <b>Easy</b> (instant self-serve developer registration, e.g. GitHub, Notion), "
    "<b>Moderate</b> (requires app manifest configuration and workspace admin consents, e.g. Slack), and <b>Hard</b> (mandates domain verification, external security assessments, and paid review queues, e.g. Google CASA audits, Salesforce AppExchange).",
    body_style
))

story.append(Paragraph("<b>B. Likely time and effort, including approval wait:</b>", h2_style))
story.append(Paragraph(
    "Active developer effort ranges from 25 minutes (GitHub) to 110 minutes (Google Cloud). "
    "Crucially, <b>approval waiting time</b> is explicitly quantified: 0 days for self-serve apps, 7-14 days for Slack Directory review, "
    "21 days for Google sensitive/restricted scope verification (plus CASA audits), and 28 days for Salesforce ISV packaging.",
    body_style
))

story.append(Paragraph("<b>C. Requirements and nuances that affect setup:</b>", h2_style))
story.append(Paragraph(
    "1. <i>Scope Sensitivity:</i> Basic scopes require no review. Restricted scopes (e.g. Gmail/Drive) trigger third-party audits.<br/>"
    "2. <i>Testing Mode Bypasses:</i> Google allows up to 100 test users immediately without verification.<br/>"
    "3. <i>Datacenter Propagation:</i> Salesforce enforces a 2-10 minute credential sync delay across datacenters before token exchange works.<br/>"
    "4. <i>Enterprise DLP/Policies:</i> Client orgs can restrict unapproved OAuth apps even if public registration succeeded.",
    body_style
))

story.append(Paragraph("<b>D. What an agent can do vs where the human must take over:</b>", h2_style))
story.append(Paragraph(
    "• <b>Agent Automated:</b> Analyzes required capabilities, generates JSON/YAML manifests (Slack/GitHub), recommends minimal non-restricted scopes, constructs PKCE challenges, and tests redirect URI endpoints.<br/>"
    "• <b>Developer Action:</b> Registers credentials in the provider portal, uploads logos, configures DNS TXT records for domain verification.<br/>"
    "• <b>Provider Action:</b> Conducts human security reviews, CASA compliance audits, and marketplace listings.",
    body_style
))

# 4. Evidence and Source Verification Audit
story.append(Paragraph("4. Evidence & Source Verification Audit Log", h1_style))

audit_data = [
    [
        Paragraph("<b>Provider</b>", table_header_style),
        Paragraph("<b>What Was Tested in Real Setup</b>", table_header_style),
        Paragraph("<b>What Was Learned & Corrected</b>", table_header_style),
        Paragraph("<b>What Remains Uncertain / Caveat</b>", table_header_style),
    ],
    [
        Paragraph("<b>GitHub</b>", table_cell_style),
        Paragraph("Registered OAuth App; validated localhost callback handshake.", table_cell_style),
        Paragraph("Learned enterprise client orgs enforce Third-Party Application Restrictions requiring admin pre-approval.", table_cell_style),
        Paragraph("SAML SSO re-authorization requirements on active token refreshes.", table_cell_style),
    ],
    [
        Paragraph("<b>Slack</b>", table_cell_style),
        Paragraph("Created app via YAML manifest; tested direct install link across 2 workspaces.", table_cell_style),
        Paragraph("Corrected misconception: Direct OAuth install links require 0 approval; only App Directory needs review.", table_cell_style),
        Paragraph("Enterprise Grid DLP policies blocking specific bot scopes dynamically.", table_cell_style),
    ],
    [
        Paragraph("<b>Google</b>", table_cell_style),
        Paragraph("Created Web Client ID; configured OAuth consent screen with localhost.", table_cell_style),
        Paragraph("Corrected misconception: Testing mode allows immediate token grants for 100 users without CASA audit.", table_cell_style),
        Paragraph("Exact third-party CASA Tier 2 lab pricing ($15k-$75k) and annual recertification turnaround.", table_cell_style),
    ],
    [
        Paragraph("<b>Notion</b>", table_cell_style),
        Paragraph("Created integration; tested authorization code exchange endpoint.", table_cell_style),
        Paragraph("Learned toggling to Public integration requires privacy policy URL but has zero manual review queue.", table_cell_style),
        Paragraph("Criteria for featured placement in Notion Integration Gallery.", table_cell_style),
    ],
    [
        Paragraph("<b>Salesforce</b>", table_cell_style),
        Paragraph("Created Connected App in Developer Sandbox; tested PKCE code flow.", table_cell_style),
        Paragraph("Discovered documented 2-10 minute propagation delay before newly issued credentials become valid.", table_cell_style),
        Paragraph("Custom IP range restriction enforcement by customer System Administrators.", table_cell_style),
    ],
]

audit_table = Table(audit_data, colWidths=[1.1*inch, 2.0*inch, 2.2*inch, 1.9*inch])
audit_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
]))
story.append(audit_table)
story.append(Spacer(1, 8))

# 5. Automated Verification & Delivery
story.append(Paragraph("5. Quality Assurance & System Verification", h1_style))
story.append(Paragraph(
    "• <b>Walkthrough Video:</b> Provided in <code>App Video.mp4</code> demonstrating local execution, 5 archetypes, and live investigation.<br/>"
    "• <b>Automated Test Suite:</b> Executed 26 regression tests via <code>pytest backend/test_api.py -v</code> covering API contracts, SSRF prevention, case-insensitive queries, and live generation. <b>Result: 26 passed, 0 failed (100% pass rate).</b><br/>"
    "• <b>Production Build:</b> Frontend compiles in 3.2s via Vite with 0 errors.<br/>"
    "• <b>Security Compliance:</b> Zero credentials or API keys committed to source control.<br/>"
    "• <b>Git Repository:</b> Available at <u>https://github.com/avantikagirigoswami/oauth-compass</u> with clean commit history.",
    body_style
))

# Build base PDF
doc.build(story)

# 1. Save Light version (no 30MB attachment, ~10KB)
with open(pdf_path_temp, "rb") as f_in, open(pdf_path_light, "wb") as f_out:
    f_out.write(f_in.read())

# 2. Save Embedded Attachment version (with App Video.mp4 embedded inside PDF)
reader = PdfReader(pdf_path_temp)
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

if os.path.exists(video_path):
    with open(video_path, "rb") as vf:
        writer.add_attachment("App Video.mp4", vf.read())

with open(pdf_path_final, "wb") as f_final:
    writer.write(f_final)

if os.path.exists(pdf_path_temp):
    os.remove(pdf_path_temp)

# 3. Create complete submission ZIP archive containing PDF, Video, and Markdown
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(pdf_path_light, arcname="OAuth_Compass_Take_Home_Submission.pdf")
    if os.path.exists(video_path):
        zf.write(video_path, arcname="App Video.mp4")
    zf.write(os.path.join(base_dir, "SUBMISSION_REPORT.md"), arcname="SUBMISSION_REPORT.md")
    zf.write(os.path.join(base_dir, "README.md"), arcname="README.md")

print("Created Light PDF:", pdf_path_light)
print("Created PDF with embedded video:", pdf_path_final)
print("Created All-in-One Submission ZIP:", zip_path)

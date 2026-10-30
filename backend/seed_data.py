"""
Seed OAuth guides for OAuth Compass.
Demonstrates varied authentication profiles across instant self-serve,
workspace permissions, enterprise security reviews, and managed auth tradeoffs.
"""

GUIDES = [
    {
        "slug": "github",
        "app_name": "GitHub",
        "official_url": "https://github.com",
        "difficulty": "easy",
        "summary": "Instant self-serve registration for personal and organization-level OAuth applications.",
        "prerequisites": [
            "Active GitHub user account",
            "Public HTTPS callback / redirect URL",
            "Application homepage URL and logo",
        ],
        "setup_steps": [
            {
                "title": "Analyze and select minimal scopes",
                "description": "Determine required OAuth scopes (e.g., read:user, repo) to minimize permission warnings during user consent.",
                "estimated_minutes": 5,
                "owner": "agent",
                "status": "not_started",
                "blocker": None,
                "source_urls": [
                    "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps"
                ],
            },
            {
                "title": "Register OAuth Application",
                "description": "Navigate to Settings > Developer settings > OAuth Apps > New OAuth App. Enter name, homepage URL, and callback URL.",
                "estimated_minutes": 10,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": [
                    "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app"
                ],
            },
            {
                "title": "Generate and secure Client Secret",
                "description": "Generate a new client secret and store it securely in your server's secret manager or environment variables.",
                "estimated_minutes": 5,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": [
                    "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps"
                ],
            },
            {
                "title": "Verify organization access policies",
                "description": "Ensure target user organizations do not have OAuth App access restrictions enabled that require explicit organization admin approval.",
                "estimated_minutes": 5,
                "owner": "developer",
                "status": "not_started",
                "blocker": "Target organizations may enforce Third-Party Application Access Restrictions, requiring organization owner approval before members can authorize.",
                "source_urls": [
                    "https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data"
                ],
            },
        ],
        "estimated_active_minutes": 25,
        "estimated_waiting_days": 0,
        "waiting_time_explanation": "Instant activation upon registration. No provider verification or wait time is required for standard OAuth apps.",
        "approval_required": False,
        "approval_notes": "No central GitHub verification needed. However, enterprise organization owners must grant access if OAuth App Restrictions are enabled.",
        "managed_oauth_available": "yes",
        "managed_oauth_notes": "Supported out-of-the-box by Managed OAuth providers (e.g. Composio, Nango). Zero portal setup required if using managed tokens.",
        "sources": [
            {
                "title": "GitHub Docs - Creating an OAuth App",
                "url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app",
                "source_type": "official_docs",
                "supports": ["Self-serve registration", "Callback URI setup"],
                "checked": True,
            },
            {
                "title": "GitHub Docs - Scopes for OAuth Apps",
                "url": "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps",
                "source_type": "official_docs",
                "supports": ["Scope definitions and least-privilege principles"],
                "checked": True,
            },
        ],
        "tested_claims": [
            "OAuth Client ID and Secret generation is instantaneous upon form submission.",
            "Testing OAuth authorization code grant flow succeeds locally with localhost callbacks.",
        ],
        "unverified_claims": [
            "Enterprise Cloud organizations with SAML SSO enforcement may require custom SAML re-authorization.",
        ],
        "next_action": "Open GitHub Developer Settings and register your application callback URL.",
    },
    {
        "slug": "slack",
        "app_name": "Slack",
        "official_url": "https://api.slack.com",
        "difficulty": "moderate",
        "summary": "Workspace installation is instant; public distribution in the Slack App Directory requires security review.",
        "prerequisites": [
            "Slack workspace where you have app-creation permissions",
            "Defined bot/user scopes (e.g. chat:write, channels:read)",
            "Public HTTPS redirect URL",
        ],
        "setup_steps": [
            {
                "title": "Generate Slack App Manifest",
                "description": "Agent constructs a valid JSON/YAML manifest specifying bot scopes, slash commands, and event subscriptions.",
                "estimated_minutes": 5,
                "owner": "agent",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://api.slack.com/reference/manifests"],
            },
            {
                "title": "Create Slack App from Manifest",
                "description": "Open api.slack.com/apps, choose 'From an app manifest', paste the agent-generated manifest, and select your workspace.",
                "estimated_minutes": 10,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://api.slack.com/authentication/oauth-v2"],
            },
            {
                "title": "Install to workspace & test token",
                "description": "Install the app to your development workspace to verify OAuth scopes and test Web API calls.",
                "estimated_minutes": 15,
                "owner": "developer",
                "status": "not_started",
                "blocker": "Workspace admin permission is required if installing into a workspace with app installation restrictions.",
                "source_urls": ["https://api.slack.com/docs"],
            },
            {
                "title": "Submit for Slack App Directory (Optional for Public Distribution)",
                "description": "For multi-workspace distribution to third parties, complete the App Directory checklist including security policy and support URL.",
                "estimated_minutes": 30,
                "owner": "provider",
                "status": "not_started",
                "blocker": "Requires privacy policy, terms of service, detailed app description, and manual Slack team review (takes 7-14 business days).",
                "source_urls": ["https://api.slack.com/start/distributing/directory"],
            },
        ],
        "estimated_active_minutes": 60,
        "estimated_waiting_days": 10,
        "waiting_time_explanation": "0 days for direct install link / internal workspace distribution. 7-14 business days if submitting to Slack App Directory.",
        "approval_required": True,
        "approval_notes": "Self-distributed OAuth install links do NOT require directory review. Official App Directory listing requires manual review.",
        "managed_oauth_available": "yes",
        "managed_oauth_notes": "Supported by Composio/Nango managed auth. Eliminates App Directory submission if you use their managed connector.",
        "sources": [
            {
                "title": "Slack API - OAuth v2",
                "url": "https://api.slack.com/authentication/oauth-v2",
                "source_type": "official_docs",
                "supports": ["Manifest creation", "OAuth v2 flow", "Granular scopes"],
                "checked": True,
            },
            {
                "title": "Slack API - App Directory Review Guidelines",
                "url": "https://api.slack.com/start/distributing/directory",
                "source_type": "policy",
                "supports": ["App directory review timeline and security requirements"],
                "checked": True,
            },
        ],
        "tested_claims": [
            "App Manifest creation via api.slack.com/apps configures scopes in 1 click.",
            "OAuth v2 direct install link works across distinct free and Pro workspaces without directory approval.",
        ],
        "unverified_claims": [
            "Slack Enterprise Grid orgs with DLP (Data Loss Prevention) policies may restrict webhook and bot token access.",
        ],
        "next_action": "Use the agent to generate your App Manifest YAML and import it at api.slack.com.",
    },
    {
        "slug": "google",
        "app_name": "Google Cloud / Workspace",
        "official_url": "https://console.cloud.google.com",
        "difficulty": "hard",
        "summary": "Multi-tier setup: consent screen, OAuth client credentials, and potential CASA Tier 2 security assessment for sensitive/restricted scopes.",
        "prerequisites": [
            "Google Cloud Platform (GCP) account and active billing project",
            "Domain ownership verification in Google Search Console",
            "Public Privacy Policy URL and Terms of Service",
            "Screen recording video demonstrating user consent and data usage",
        ],
        "setup_steps": [
            {
                "title": "GCP Project & API enablement",
                "description": "Create or select a GCP project. Enable target APIs (e.g. Gmail API, Google Drive API, Google Calendar API).",
                "estimated_minutes": 15,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://console.cloud.google.com/apis/dashboard"],
            },
            {
                "title": "Scope Classification & Minimization",
                "description": "Agent categorizes requested scopes into Non-sensitive (e.g. email, profile), Sensitive, or Restricted (e.g. drive, gmail) to identify audit liabilities.",
                "estimated_minutes": 10,
                "owner": "agent",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://developers.google.com/identity/protocols/oauth2/scopes"],
            },
            {
                "title": "Configure OAuth Consent Screen",
                "description": "Configure User Type (External), application name, user support email, authorized domains, developer contact info, and requested scopes.",
                "estimated_minutes": 25,
                "owner": "developer",
                "status": "not_started",
                "blocker": "Authorized domains must be verified in Google Search Console under the same GCP account.",
                "source_urls": [
                    "https://developers.google.com/workspace/guides/configure-oauth-consent"
                ],
            },
            {
                "title": "Create Web Application Credentials",
                "description": "Create OAuth 2.0 Client ID for Web application. Add Authorized JavaScript origins and Authorized redirect URIs.",
                "estimated_minutes": 15,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://developers.google.com/identity/protocols/oauth2"],
            },
            {
                "title": "Submit for Google Verification & CASA Assessment",
                "description": "Submit app for Google Trust & Safety verification. Provide YouTube demo video. Complete third-party CASA Tier 2 assessment if using restricted scopes.",
                "estimated_minutes": 45,
                "owner": "provider",
                "status": "not_started",
                "blocker": "Restricted scopes (Gmail/Drive) require CASA Tier 2/3 security assessment ($15k-$75k audit fee or free tier self-scan through authorized lab) and 3-6 weeks review.",
                "source_urls": [
                    "https://developers.google.com/identity/protocols/oauth2/production-readiness"
                ],
            },
        ],
        "estimated_active_minutes": 110,
        "estimated_waiting_days": 21,
        "waiting_time_explanation": "Test mode is immediate (max 100 users). Production verification for sensitive scopes takes 4-8 business days; restricted scopes take 3-6 weeks including CASA assessment.",
        "approval_required": True,
        "approval_notes": "Required if serving external users outside your Google Workspace domain with sensitive or restricted scopes. Test mode bypasses approval for 100 pre-approved test users.",
        "managed_oauth_available": "yes",
        "managed_oauth_notes": "Composio and Nango offer Managed Google OAuth with pre-verified consent screens, completely bypassing CASA audits for prototyping.",
        "sources": [
            {
                "title": "Google Identity - OAuth 2.0 Protocols",
                "url": "https://developers.google.com/identity/protocols/oauth2",
                "source_type": "official_docs",
                "supports": ["GCP credentials", "Redirect URI constraints"],
                "checked": True,
            },
            {
                "title": "Google Cloud - OAuth API Verification FAQ",
                "url": "https://support.google.com/cloud/answer/9110914",
                "source_type": "policy",
                "supports": ["Scope verification criteria", "CASA assessment requirements"],
                "checked": True,
            },
        ],
        "tested_claims": [
            "OAuth Client ID works immediately in 'Testing' status for listed test users without submitting for verification.",
            "Redirect URIs with localhost / 127.0.0.1 are permitted for development without HTTPS.",
        ],
        "unverified_claims": [
            "Annual CASA re-certification timeline and cost varies by authorized assessment lab.",
        ],
        "next_action": "Check whether your agent's required scopes are Restricted vs Sensitive to determine verification burden.",
    },
    {
        "slug": "notion",
        "app_name": "Notion",
        "official_url": "https://developers.notion.com",
        "difficulty": "easy",
        "summary": "Dual-mode integration: Internal tokens are instant; Public OAuth apps require redirect URI configuration and multi-tenant consent.",
        "prerequisites": [
            "Notion workspace where you have admin permissions",
            "Public HTTPS redirect URI for OAuth callback",
            "Integration name and icon",
        ],
        "setup_steps": [
            {
                "title": "Create Integration in Notion Developer Portal",
                "description": "Navigate to notion.so/profile/integrations. Click 'New integration', name your integration, and associate with an owner workspace.",
                "estimated_minutes": 5,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://developers.notion.com/docs/create-a-notion-integration"],
            },
            {
                "title": "Configure Integration Capabilities",
                "description": "Agent selects minimal required capabilities: Read content, Update content, Insert content, or Read user information.",
                "estimated_minutes": 5,
                "owner": "agent",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://developers.notion.com/reference/capabilities"],
            },
            {
                "title": "Switch to Public Distribution (OAuth 2.0)",
                "description": "In the Distribution tab, toggle 'Make integration public'. Enter company name, homepage URL, privacy policy, and Redirect URIs.",
                "estimated_minutes": 15,
                "owner": "developer",
                "status": "not_started",
                "blocker": "Toggling to public requires valid Privacy Policy, Terms of Service, and Support email URLs.",
                "source_urls": ["https://developers.notion.com/docs/authorization"],
            },
            {
                "title": "Implement Authorization Code Grant",
                "description": "Redirect user to Notion's authorization URL. Exchange code at https://api.notion.com/v1/oauth/token with basic auth (client_id:client_secret).",
                "estimated_minutes": 15,
                "owner": "agent",
                "status": "not_started",
                "blocker": None,
                "source_urls": ["https://developers.notion.com/docs/authorization#step-2-exchange-the-code-for-an-access-token"],
            },
        ],
        "estimated_active_minutes": 40,
        "estimated_waiting_days": 0,
        "waiting_time_explanation": "Instant approval. Once distribution fields are populated, public OAuth authorization links work immediately without manual review.",
        "approval_required": False,
        "approval_notes": "Notion does not impose a mandatory manual review queue for public integrations to function across workspaces.",
        "managed_oauth_available": "yes",
        "managed_oauth_notes": "Fully supported in Composio toolkit. Developers can authenticate users with 1 line of SDK code.",
        "sources": [
            {
                "title": "Notion Developers - Authorization Guide",
                "url": "https://developers.notion.com/docs/authorization",
                "source_type": "official_docs",
                "supports": ["Public integration configuration", "Token exchange format"],
                "checked": True,
            }
        ],
        "tested_claims": [
            "Internal integration tokens can be created in under 60 seconds for single-workspace use.",
            "Public OAuth token endpoint returns bot_id, workspace_id, and access_token immediately upon valid exchange.",
        ],
        "unverified_claims": [
            "Featured placement in the Notion Integration Gallery requires a separate partner application.",
        ],
        "next_action": "Decide between Internal Integration (single workspace) or Public Integration (multi-tenant OAuth).",
    },
    {
        "slug": "salesforce",
        "app_name": "Salesforce",
        "official_url": "https://developer.salesforce.com",
        "difficulty": "hard",
        "summary": "Enterprise Connected App registration with PKCE requirements, IP relaxation policies, and AppExchange security reviews for ISVs.",
        "prerequisites": [
            "Salesforce Developer Edition or Sandbox org with System Administrator profile",
            "Public HTTPS callback URI",
            "Defined OAuth scopes (e.g., api, refresh_token, offline_access)",
        ],
        "setup_steps": [
            {
                "title": "Create Connected App in App Manager",
                "description": "In Salesforce Setup, navigate to App Manager > New Connected App. Enter App Name, API Name, and Contact Email.",
                "estimated_minutes": 15,
                "owner": "developer",
                "status": "not_started",
                "blocker": None,
                "source_urls": [
                    "https://help.salesforce.com/s/articleView?id=sf.connected_app_create_basics.htm"
                ],
            },
            {
                "title": "Enable OAuth Settings & PKCE",
                "description": "Agent specifies recommended OAuth scopes (api, refresh_token) and enforces Proof Key for Code Exchange (PKCE) for modern security.",
                "estimated_minutes": 10,
                "owner": "agent",
                "status": "not_started",
                "blocker": None,
                "source_urls": [
                    "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm"
                ],
            },
            {
                "title": "Configure OAuth Policies & IP Relaxation",
                "description": "Under Manage Connected Apps, set 'Permitted Users' (All users may self-authorize vs Admin approved) and Relax IP Restrictions if connecting from cloud agents.",
                "estimated_minutes": 15,
                "owner": "developer",
                "status": "not_started",
                "blocker": "Connected App changes take 2 to 10 minutes to propagate across Salesforce datacenters.",
                "source_urls": [
                    "https://help.salesforce.com/s/articleView?id=sf.connected_app_manage_oauth.htm"
                ],
            },
            {
                "title": "AppExchange Security Review (Commercial ISV Distribution)",
                "description": "For public marketplace distribution, package the app, run Checkmarx Source Code Scanner, and submit to Salesforce Security Review.",
                "estimated_minutes": 45,
                "owner": "provider",
                "status": "not_started",
                "blocker": "$999-$2,550 security review fee and 4-8 weeks review queue for commercial multi-tenant AppExchange packages.",
                "source_urls": [
                    "https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/security_review_overview.htm"
                ],
            },
        ],
        "estimated_active_minutes": 85,
        "estimated_waiting_days": 28,
        "waiting_time_explanation": "0 days for direct Connected App authorization in your own or client orgs. 4-8 weeks if packaging as an AppExchange managed package.",
        "approval_required": True,
        "approval_notes": "Customer org System Administrators can pre-authorize or block Connected Apps. Commercial AppExchange listing requires paid security review.",
        "managed_oauth_available": "yes",
        "managed_oauth_notes": "Supported by Composio/Nango managed OAuth, avoiding custom Connected App setup for each agent environment.",
        "sources": [
            {
                "title": "Salesforce Help - Create a Connected App",
                "url": "https://help.salesforce.com/s/articleView?id=sf.connected_app_create_basics.htm",
                "source_type": "official_docs",
                "supports": ["Connected App OAuth parameters", "Consumer Key & Secret"],
                "checked": True,
            },
            {
                "title": "Salesforce Partner - Security Review",
                "url": "https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/security_review_overview.htm",
                "source_type": "policy",
                "supports": ["AppExchange security review fees and timeline"],
                "checked": True,
            },
        ],
        "tested_claims": [
            "Connected App Consumer Key and Consumer Secret are issued immediately upon saving in App Manager.",
            "Wait time of 5-10 minutes is consistently required for newly created Connected App credentials to become valid for token exchange.",
        ],
        "unverified_claims": [
            "Enterprise client orgs with custom IP Range restrictions may block OAuth token refresh without static IP egress.",
        ],
        "next_action": "Decide whether direct Connected App integration or Managed OAuth (Composio) fits your user model.",
    },
]

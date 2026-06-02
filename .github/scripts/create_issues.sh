#!/bin/bash

# Create remaining 25 development feature issues

gh issue create --title "[Foundation][P0] .gitignore configuration" --body "Create .gitignore to exclude venv, database files, and secrets.\n\n(WBS 1.1.3)\nOwner: xeeshan74" --label "P0,foundation" --assignee xeeshan74

gh issue create --title "[Foundation][P0] Module layout & initial commit" --body "Set up module layout with initial files: app.py, models.py, config.py, etc.\n\n(WBS 1.1.6)\nOwner: Team" --label "P0,foundation" --assignee xeeshan74

gh issue create --title "[Auth][P0] DNS TXT verification" --body "Implement DNS TXT record verification for domain ownership validation.\n\n(WBS 1.2.1)\nOwner: xeeshan74" --label "P0,auth" --assignee xeeshan74

gh issue create --title "[Auth][P0] Demo & manual classroom modes" --body "Implement demo mode and manual classroom verification modes for testing without TXT records.\n\n(WBS 1.2.2)\nOwner: xeeshan74" --label "P0,auth" --assignee xeeshan74

gh issue create --title "[Auth][P0] Rate limit & private IP block" --body "Implement rate limiting and block private IP address scanning.\n\n(WBS 1.2.3)\nOwner: xeeshan74" --label "P0,auth" --assignee xeeshan74

gh issue create --title "[Discovery][P0] Apex DNS resolution" --body "Implement apex domain DNS resolution for subdomain discovery.\n\n(WBS 1.3.1)\nOwner: xeeshan74" --label "P0,discovery" --assignee xeeshan74

gh issue create --title "[Discovery][P0] Wordlist subdomain discovery" --body "Implement wordlist-based subdomain discovery.\n\n(WBS 1.3.2)\nOwner: xeeshan74" --label "P0,discovery" --assignee xeeshan74

gh issue create --title "[Checks][P0] HTTP/HTTPS metadata retrieval" --body "Implement HTTP/HTTPS metadata collection (GET only) for discovered subdomains.\n\n(WBS 1.4.1)\nOwner: hardi-umar, xeeshan74" --label "P0,checks" --assignee hardi-umar --assignee xeeshan74

gh issue create --title "[Checks][P0] TLS certificate expiry checks" --body "Check TLS certificate validity and expiry dates.\n\n(WBS 1.4.2)\nOwner: hardi-umar, xeeshan74" --label "P0,checks" --assignee hardi-umar --assignee xeeshan74

gh issue create --title "[Checks][P0] SPF / DMARC from DNS" --body "Query and validate SPF and DMARC DNS records for email security.\n\n(WBS 1.4.3)\nOwner: xeeshan74" --label "P0,checks" --assignee xeeshan74

gh issue create --title "[Checks][P0] Security header findings" --body "Identify missing or misconfigured security headers (CSP, HSTS, X-Frame-Options, etc.).\n\n(WBS 1.4.4)\nOwner: xeeshan74" --label "P0,checks" --assignee xeeshan74

gh issue create --title "[Analysis][P0] Page classification & confidence scoring" --body "Classify discovered pages/surfaces and assign confidence scores.\n\n(WBS 1.5.1)\nOwner: hardi-umar" --label "P0,analysis" --assignee hardi-umar

gh issue create --title "[Analysis][P0] Findings & risk scoring" --body "Generate findings and compute risk scores for each discovery.\n\n(WBS 1.5.2)\nOwner: xeeshan74" --label "P0,analysis" --assignee xeeshan74

gh issue create --title "[UI][P0] Executive dashboard with charts" --body "Build executive summary dashboard with visual charts and key findings.\n\n(WBS 1.5.3)\nOwner: briantwai" --label "P0,ui" --assignee briantwai

gh issue create --title "[Reporting][P0] Markdown report export" --body "Implement Markdown report generation and export functionality.\n\n(WBS 1.5.4)\nOwner: briantwai" --label "P0,reporting" --assignee briantwai

gh issue create --title "[Storage][P0] SQLite schema & CRUD operations" --body "Design and implement SQLite schema with CRUD operations for data persistence.\n\n(WBS 1.6.1)\nOwner: xeeshan74" --label "P0,storage" --assignee xeeshan74

gh issue create --title "[Workflow][P0] End-to-end assessment flow" --body "Implement complete end-to-end domain assessment workflow.\n\n(WBS 1.6.2)\nOwner: xeeshan74" --label "P0,workflow" --assignee xeeshan74

gh issue create --title "[AWS][P1] AWS credits, billing alert & tags" --body "Set up AWS account, configure billing alerts, and establish resource tagging strategy.\n\n(WBS 1.7.1)\nOwner: briantwai\nTarget week: 4\nStatus: Prep" --label "P1,aws" --assignee briantwai

gh issue create --title "[AWS][P1] Deploy design (App Runner or Lightsail)" --body "Design and plan deployment architecture for AWS App Runner or Lightsail.\n\n(WBS 1.7.2)\nOwner: briantwai\nTarget week: 5\nStatus: Planned" --label "P1,aws" --assignee briantwai

gh issue create --title "[AWS][P1] Deploy configuration in repo" --body "Add deployment configuration files to deploy/ directory in repository.\n\n(WBS 1.7.3)\nOwner: briantwai\nTarget week: 6\nStatus: Planned" --label "P1,aws" --assignee briantwai

gh issue create --title "[AWS][P1] Public HTTPS URL for class demo" --body "Deploy application to AWS and provide public HTTPS URL for Week 8 class demonstration.\n\n(WBS 1.7.4)\nOwner: briantwai\nTarget week: 8\nStatus: Planned" --label "P1,aws" --assignee briantwai

gh issue create --title "[AWS][P1] Demo runbook & laptop fallback" --body "Create demo runbook and prepare laptop fallback for Week 8 presentation.\n\n(WBS 1.7.5)\nOwner: briantwai\nTarget week: 8\nStatus: Planned" --label "P1,aws" --assignee briantwai

gh issue create --title "[Stretch][P2] Certificate Transparency discovery" --body "Implement Certificate Transparency log checks for domain discovery.\n\n(WBS P2)\nNotes: Rate limits, extra API work" --label "P2,stretch" --assignee xeeshan74

gh issue create --title "[Stretch][P2] PDF / HTML report export" --body "Implement PDF and HTML report export functionality.\n\n(WBS P2)\nNotes: Markdown is MVP" --label "P2,stretch" --assignee ghostfruitleat

gh issue create --title "[Stretch][P2] REST API (FastAPI)" --body "Build REST API using FastAPI for programmatic access to PROBE.\n\n(WBS P2)\nNotes: Streamlit-only for now" --label "P2,stretch" --assignee hardi-umar

gh issue create --title "[Stretch][P2] Historical compare across runs" --body "Implement historical comparison of assessment results across multiple runs.\n\n(WBS P2)\nNotes: Needs schema design" --label "P2,stretch" --assignee xeeshan74

gh issue create --title "[Stretch][P2] Full public IP correlation" --body "Implement full public IP address correlation and correlation features.\n\n(WBS P2)\nNotes: Optional field only today" --label "P2,stretch" --assignee hardi-umar

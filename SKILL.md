---
name: crowdsec
description: |
  CrowdSec security monitoring and management for OpenClaw agents.
  Query active bans, recent alerts, system metrics, and manage IP decisions.
  Designed for Pulse (monitoring) and Atlas (infra) personas.
triggers:
  - "security status"
  - "show bans"
  - "ban ip"
  - "unban ip"
  - "crowdsec"
  - "who is attacking"
  - "security report"
  - "intrusion"
  - "blocked ips"
---

# CrowdSec Security Skill

Monitor and manage CrowdSec intrusion detection from any OpenClaw agent.

## Commands

### Status Overview
Trigger: "security status", "crowdsec status", "are we under attack"

```bash
crowdsec-skill status
```

Returns: active bans count, recent alerts, top attacking IPs, system health.

### List Active Bans
Trigger: "show bans", "blocked ips", "who is banned"

```bash
crowdsec-skill bans [--limit N] [--country XX]
```

Returns: table of banned IPs with reason, country, expiry.

### Recent Alerts
Trigger: "recent attacks", "security alerts", "who is attacking"

```bash
crowdsec-skill alerts [--since 1h|24h|7d]
```

Returns: recent intrusion alerts with source IP, scenario triggered, timestamp.

### Metrics
Trigger: "security metrics", "crowdsec metrics"

```bash
crowdsec-skill metrics
```

Returns: lines parsed, events processed, active decisions, bouncer health.

### Ban an IP
Trigger: "ban ip X.X.X.X", "block ip"

```bash
crowdsec-skill ban <ip> [--duration 24h] [--reason "manual ban"]
```

### Unban an IP
Trigger: "unban ip X.X.X.X", "unblock ip"

```bash
crowdsec-skill unban <ip>
```

### Security Report
Trigger: "security report", "daily security summary"

```bash
crowdsec-skill report [--period 24h|7d|30d]
```

Returns: formatted summary suitable for WhatsApp delivery — top attackers,
geographic breakdown, scenario hits, recommendations.

## Agent Routing

Best suited for:
- **Pulse** (monitor): automated security checks, alert delivery
- **Atlas** (infra): manual ban/unban, incident response
- **Jarvis** (orchestrator): security status on demand

## Example Flows

### WhatsApp: "Jarvis, are we under attack?"
```
Jarvis -> routes to Pulse
Pulse -> crowdsec-skill status
Pulse -> formats response
Pulse -> delivers via WhatsApp
```

### Cron: Daily security digest (08:00)
```
Pulse -> crowdsec-skill report --period 24h
Pulse -> delivers summary via WhatsApp
```

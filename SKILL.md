---
name: crowdsec
description: |
  CrowdSec Sentinel — install, monitor, and manage CrowdSec intrusion
  detection for OpenClaw agents. Includes proactive alerting, auth log
  analysis, firewall management, and security hardening checks.
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
  - "install crowdsec"
  - "upgrade crowdsec"
  - "whitelist ip"
  - "crowdsec collections"
  - "failed logins"
  - "auth log"
  - "hardening"
  - "firewall status"
  - "security alert"
---

# CrowdSec Sentinel Skill

Install, monitor, and manage CrowdSec intrusion detection from any OpenClaw agent.

## Commands

### Install & Upgrade
Trigger: "install crowdsec", "set up crowdsec", "upgrade crowdsec"

```bash
crowdsec-skill install    # Full install: engine + bouncer + collections
crowdsec-skill upgrade    # Upgrade packages and hub content
```

### Status Overview
Trigger: "security status", "crowdsec status", "are we under attack"

```bash
crowdsec-skill status
```

### List Active Bans
Trigger: "show bans", "blocked ips", "who is banned"

```bash
crowdsec-skill bans [limit]
```

### Recent Alerts
Trigger: "recent attacks", "security alerts", "who is attacking"

```bash
crowdsec-skill alerts [1h|24h|7d]
```

### Security Report
Trigger: "security report", "daily security summary"

```bash
crowdsec-skill report [24h|7d|30d]
```

### Proactive Alert Check
Trigger: "security alert", "check security", "run alert check"

```bash
crowdsec-skill alert
```

Returns exit code 0 (clear), 1 (warning), or 2 (critical) for automation.
Checks: ban count, alert rate, failed logins, service health.

### Ban / Unban
Trigger: "ban ip X.X.X.X", "block ip", "unban ip"

```bash
crowdsec-skill ban <ip> [duration] [reason]
crowdsec-skill unban <ip>
```

### Auth Logs
Trigger: "failed logins", "auth log", "who logged in", "sudo usage"

```bash
crowdsec-skill auth recent         # Recent auth events
crowdsec-skill auth failed         # Failed login attempts
crowdsec-skill auth success        # Successful logins
crowdsec-skill auth sudo           # Sudo usage
crowdsec-skill auth stats          # Today's auth summary
```

### System Logs
Trigger: "syslog", "kernel errors", "security events"

```bash
crowdsec-skill syslog recent       # Recent syslog
crowdsec-skill syslog errors       # Error entries
crowdsec-skill syslog kernel       # Kernel/dmesg
crowdsec-skill syslog security     # Security events
crowdsec-skill logs recent|errors|watch|stats  # CrowdSec logs
```

### Firewall Management
Trigger: "firewall status", "flush bans", "reload firewall"

```bash
crowdsec-skill firewall status     # ipset counts, rules
crowdsec-skill firewall reload     # Reload bouncer
crowdsec-skill firewall flush      # Clear all bans
crowdsec-skill firewall switch <iptables|ufw>
```

### Whitelist Management
Trigger: "whitelist ip", "add to whitelist"

```bash
crowdsec-skill whitelist list
crowdsec-skill whitelist add <ip-or-cidr>
crowdsec-skill whitelist remove <ip-or-cidr>
```

### Collections
Trigger: "crowdsec collections", "install collection"

```bash
crowdsec-skill collections list
crowdsec-skill collections available
crowdsec-skill collections install <name>
crowdsec-skill collections remove <name>
```

### Log Management
Trigger: "log rotation", "log retention"

```bash
crowdsec-skill logging status
crowdsec-skill logging setup
crowdsec-skill logging retention <days>
crowdsec-skill logging report [7d]
crowdsec-skill logging rotate
```

### Service Management

```bash
crowdsec-skill services start|stop|restart|health
```

### Security Hardening
Trigger: "hardening check", "security audit"

```bash
crowdsec-skill hardening
```

Checks SSH config, firewall, CrowdSec status, automatic updates, file permissions.

### CrowdSec vs Fail2ban

```bash
crowdsec-skill compare
```

## Agent Routing

Best suited for:
- **Pulse** (monitor): automated security checks, alert delivery
- **Atlas** (infra): manual ban/unban, incident response, hardening
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

### Cron: Proactive alert (every 15 min)
```
crowdsec-skill alert || Pulse -> send WhatsApp alert
```

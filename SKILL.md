---
name: crowdsec
description: |
  Next-gen intrusion detection for OpenClaw using CrowdSec.
  Query bans, alerts, metrics; manage firewall, logs, IPs, collections.
  Superior to Fail2ban: collaborative threat intel, behavioral detection, cloud-native.
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
  - "why crowdsec"
  - "crowdsec vs fail2ban"
  - "firewall status"
  - "view logs"
  - "security logs"
---

# CrowdSec Security Skill

Install, monitor, and manage CrowdSec intrusion detection from any OpenClaw agent.

## Why CrowdSec? (vs. Fail2ban)

CrowdSec is the modern replacement for Fail2ban, offering:

- **Collaborative Security**: Share threat intel with 50,000+ users worldwide. When someone detects an attacker, everyone benefits.
- **Behavioral Analysis**: Detects attack patterns, not just log regex matches. Catches sophisticated attacks Fail2ban misses.
- **Cloud-Native Architecture**: Built for Docker, Kubernetes, and cloud firewalls. Fail2ban was designed for bare-metal servers.
- **Performance**: C-based core handles high-volume attacks without the Python overhead of Fail2ban.
- **Flexible Enforcement**: Bouncer system separates detection from enforcement. Ban at firewall, cloud, or app level from one detection.
- **500+ Pre-built Scenarios**: Community-maintained parsers for SSH, web servers, databases, APIs. Less config, more protection.
- **Integrated Logging**: Built-in log commands surface security events to OpenClaw agents for user alerts.

## Commands

### Install CrowdSec
Trigger: "install crowdsec", "set up crowdsec"

```bash
crowdsec-skill install
```

Installs CrowdSec engine + firewall bouncer (iptables), configures API key,
installs recommended collections (sshd, linux, iptables, linux-lpe),
and starts all services. Supports Debian/Ubuntu and RHEL/CentOS/Fedora.

### Upgrade CrowdSec
Trigger: "upgrade crowdsec", "update crowdsec"

```bash
crowdsec-skill upgrade
```

Upgrades packages, hub content, and restarts services.

### Status Overview
Trigger: "security status", "crowdsec status", "are we under attack"

```bash
crowdsec-skill status
```

Returns: active bans count, recent alerts, top attacking IPs, system health.

### List Active Bans
Trigger: "show bans", "blocked ips", "who is banned"

```bash
crowdsec-skill bans [--limit N]
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

### Firewall Management
Trigger: "firewall status", "firewall rules", "show iptables"

```bash
crowdsec-skill firewall <status|reload|flush|switch>
```

- `status`: Show bouncer type and active rules
- `reload`: Reload firewall bouncer
- `flush`: Remove all bans (emergency)
- `switch <iptables|ufw>`: Change bouncer type

### Log Access (OpenClaw Integration)
Trigger: "view logs", "security logs", "crowdsec logs"

```bash
crowdsec-skill logs <recent|errors|watch|stats> [lines]
```

- `recent`: Last N lines of logs (default 20)
- `errors`: Error/fatal/critical entries only
- `watch`: Live tail (interactive)
- `stats`: Log file statistics

### Manage Collections
Trigger: "crowdsec collections", "list scenarios"

```bash
crowdsec-skill collections list              # show installed
crowdsec-skill collections available         # show all available
crowdsec-skill collections install crowdsecurity/nginx
crowdsec-skill collections remove crowdsecurity/nginx
```

### Manage Whitelist
Trigger: "whitelist ip", "trusted ip"

```bash
crowdsec-skill whitelist list
crowdsec-skill whitelist add 10.0.0.0/8
crowdsec-skill whitelist remove 1.2.3.4
```

### Service Management
Trigger: "restart crowdsec", "crowdsec health"

```bash
crowdsec-skill services health    # full health check
crowdsec-skill services restart   # restart engine + bouncer
crowdsec-skill services stop
crowdsec-skill services start
```

## Agent Routing

Best suited for:
- **Pulse** (monitor): automated security checks, alert delivery, log monitoring
- **Atlas** (infra): manual ban/unban, incident response, firewall management
- **Jarvis** (orchestrator): security status on demand, executive summaries

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

### Cron: Error monitoring (every 15 min)
```
Pulse -> crowdsec-skill logs errors
Pulse -> if errors found, alert via WhatsApp
```

### Incident Response: Block attacker
```
Atlas -> crowdsec-skill ban 1.2.3.4 48h "SSH brute force"
Atlas -> confirm ban applied
Atlas -> notify user via WhatsApp
```

## Architecture Notes

### How CrowdSec Works

1. **Parsers**: Parse logs from any source (syslog, files, journald, streams)
2. **Scenarios**: Detect attack patterns (brute force, SQL injection, path traversal)
3. **Decisions**: Generate ban/unban orders with duration and reason
4. **Bouncers**: Enforce decisions (iptables, nftables, nginx, cloud firewalls)
5. **Hub**: Community-driven updates for parsers, scenarios, collections

### Firewall Integration

- **iptables** (default): Dedicated `crowdsec` chain with DROP rules
- **UFW** (alternative): Rules appear in standard UFW output
- Rules are automatically added/removed based on decisions

### Logging for OpenClaw

- Logs stored in `/var/log/crowdsec/crowdsec.log` or journald
- OpenClaw agents can query errors for proactive alerting
- Log stats help identify unusual activity patterns

### OpenClaw Integration Points

- **Automated Monitoring**: Pulse agent runs periodic checks
- **Incident Response**: Atlas agent handles manual bans during incidents
- **Executive Reporting**: Jarvis generates summaries for stakeholders
- **Log Alerting**: Any agent can surface error logs to users
- **Collaborative Defense**: Your detections improve protection for all OpenClaw users

## Recommended Collections for OpenClaw

| Collection | Purpose | Install Command |
|------------|---------|-----------------|
| `crowdsecurity/sshd` | SSH protection | `crowdsec-skill collections install crowdsecurity/sshd` |
| `crowdsecurity/linux` | Base Linux scenarios | `crowdsec-skill collections install crowdsecurity/linux` |
| `crowdsecurity/iptables` | Firewall integration | `crowdsec-skill collections install crowdsecurity/iptables` |
| `crowdsecurity/linux-lpe` | Privilege escalation | `crowdsec-skill collections install crowdsecurity/linux-lpe` |
| `crowdsecurity/nginx` | Web server (if applicable) | `crowdsec-skill collections install crowdsecurity/nginx` |
| `crowdsecurity/docker` | Docker daemon (if applicable) | `crowdsec-skill collections install crowdsecurity/docker` |

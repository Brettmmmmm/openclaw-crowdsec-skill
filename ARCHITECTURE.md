# OpenClaw CrowdSec Skill - Architecture Blueprint

## Overview

This document describes the architecture of the CrowdSec security monitoring skill for OpenClaw, including data flows, component interactions, and integration points.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           OpenClaw Ecosystem                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │  Pulse   │  │  Atlas   │  │  Jarvis  │  │  Other   │                    │
│  │ (Monitor)│  │ (Infra)  │  │(Orchestr.)│  │  Agents  │                    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                    │
│       │             │             │             │                           │
│       └─────────────┴─────────────┴─────────────┘                           │
│                           │                                                 │
│                  crowdsec-skill CLI                                         │
└───────────────────────────┼─────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CrowdSec Security Layer                               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    cscli (CLI Interface)                             │    │
│  │  - decisions list/add/delete                                        │    │
│  │  - alerts list                                                      │    │
│  │  - metrics                                                          │    │
│  │  - collections manage                                               │    │
│  │  - bouncers manage                                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                            │                                                 │
│                            ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  CrowdSec Engine (crowdsec)                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │   Parsers    │  │  Scenarios   │  │  Decisions   │               │    │
│  │  │  (s00/s01)   │  │   (s02)      │  │   Engine     │               │    │
│  │  │              │  │              │  │              │               │    │
│  │  │ - syslog     │  │ - brute      │  │ - ban        │               │    │
│  │  │ - journald   │  │   force      │  │ - unban      │               │    │
│  │  │ - file logs  │  │ - scan       │  │ - duration   │               │    │
│  │  │ - docker     │  │   probing    │  │ - reason     │               │    │
│  │  │ - k8s logs   │  │ - injection  │  │              │               │    │
│  │  │              │  │ - overflow   │  │              │               │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                            │                                                 │
│                            ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              Firewall Bouncer (crowdsec-firewall-bouncer)            │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                    iptables/nftables                          │   │    │
│  │  │  - INPUT chain rules                                         │   │    │
│  │  │  - crowdsec chain                                            │   │    │
│  │  │  - DROP/REJECT rules                                         │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │    Network Traffic      │
              │    (Filtered)           │
              └─────────────────────────┘
```

## Data Flow

### 1. Attack Detection Flow

```
1. Log Source (sshd, nginx, etc.)
         │
         ▼
2. CrowdSec Parser (s00-s01)
   - Parse log format
   - Extract IP, timestamp, event type
         │
         ▼
3. Scenario Engine (s02)
   - Match against attack patterns
   - Track behavior over time
   - Calculate threat score
         │
         ▼
4. Decision Engine
   - Generate ban decision
   - Set duration (default 4h, configurable)
   - Add reason/scenario
         │
         ▼
5. Bouncer Notification
   - Push decision via API
   - Bouncer enforces at firewall
```

### 2. OpenClaw Query Flow

```
User (WhatsApp/CLI)
         │
         ▼
OpenClaw Agent (Pulse/Atlas/Jarvis)
         │
         ▼
crowdsec-skill command
         │
         ▼
cscli query (decisions/alerts/metrics)
         │
         ▼
JSON/Text output
         │
         ▼
Formatted response to user
```

## Components

### crowdsec-skill Script

| Component | Purpose | Location |
|-----------|---------|----------|
| `cmd_status` | Overview of security posture | Lines 43-85 |
| `cmd_bans` | List active IP bans | Lines 87-127 |
| `cmd_alerts` | Recent attack alerts | Lines 129-165 |
| `cmd_metrics` | Engine performance metrics | Lines 167-170 |
| `cmd_ban` | Manual IP ban | Lines 172-186 |
| `cmd_unban` | Remove IP ban | Lines 188-193 |
| `cmd_report` | Security summary report | Lines 195-265 |
| `cmd_install` | Install CrowdSec + bouncer | Lines 267-325 |
| `cmd_upgrade` | Upgrade packages | Lines 327-362 |
| `cmd_collections` | Manage detection modules | Lines 364-391 |
| `cmd_whitelist` | Manage IP whitelist | Lines 393-451 |
| `cmd_services` | Service management | Lines 453-487 |
| `cmd_compare` | CrowdSec vs Fail2ban | Lines 489-537 |
| `cmd_help` | Usage information | Lines 539-575 |

### Required CrowdSec Collections

| Collection | Purpose | Priority |
|------------|---------|----------|
| `crowdsecurity/sshd` | SSH brute-force detection | Critical |
| `crowdsecurity/linux` | Base Linux security scenarios | Critical |
| `crowdsecurity/iptables` | Firewall integration | Critical |
| `crowdsecurity/linux-lpe` | Local privilege escalation | High |
| `crowdsecurity/nginx` | Web server protection | Medium |
| `crowdsecurity/apache2` | Apache protection | Medium |
| `crowdsecurity/postfix` | Mail server protection | Medium |
| `crowdsecurity/dovecot` | IMAP/POP3 protection | Medium |
| `crowdsecurity/mysql` | Database protection | Medium |
| `crowdsecurity/redis` | Redis protection | Low |

### Firewall Configuration

#### iptables Rules (Default)

```bash
# Chain created by crowdsec-firewall-bouncer
:crowdsec - [0:0]

# Jump from INPUT to crowdsec chain
-A INPUT -j crowdsec

# Ban rules (added dynamically)
-A crowdsec -s 1.2.3.4/32 -j DROP
-A crowdsec -s 5.6.7.8/32 -j DROP
```

#### UFW Integration (Alternative)

For systems using UFW instead of raw iptables:

```bash
# Install UFW bouncer instead
apt install crowdsec-firewall-bouncer-ufw

# Rules appear in ufw status:
ufw status numbered
# [1] DROP FROM 1.2.3.4
```

### Logging Architecture

```
/var/log/crowdsec/
├── crowdsec.log          # Engine logs (INFO/WARN/ERROR)
└── crowdsec_api.log      # API access logs

/var/log/journal/
└── crowdsec.service      # Systemd journal entries

cscli logs                # View via CLI
```

#### Log Levels

| Level | Purpose | OpenClaw Alert Trigger |
|-------|---------|------------------------|
| INFO | Normal operations | No |
| WARN | Unusual activity | Optional digest |
| ERROR | System issues | Immediate alert |
| CRITICAL | Service down | Immediate alert + escalation |

## Integration Points

### OpenClaw Agent Personas

| Agent | Commands | Use Case |
|-------|----------|----------|
| **Pulse** | status, alerts, report | Automated monitoring, WhatsApp alerts |
| **Atlas** | ban, unban, services | Incident response, manual intervention |
| **Jarvis** | status, metrics, compare | Executive summaries, on-demand queries |

### Cron Integration

```bash
# Daily security digest (08:00)
0 8 * * * openclaw agent --agent pulse \
  -m "Run crowdsec-skill report --period 24h" \
  --deliver --reply-channel whatsapp \
  --reply-to <user-number>

# Hourly status check
0 * * * * openclaw agent --agent pulse \
  -m "Run crowdsec-skill status" \
  --deliver --reply-channel whatsapp \
  --reply-to <user-number>
```

### Alert Triggers

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Active bans > 10 | Any time | Digest alert |
| Alerts > 50/hour | Sustained 15min | Immediate alert |
| Service down | Any | Immediate escalation |
| New country in top attackers | Per report | Highlight in digest |

## Security Considerations

### API Key Management

- Bouncer API key stored in `/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml`
- Key permissions: `640` (root:root)
- Key rotation: Run `cscli bouncers remove <name>` then `cscli bouncers add <name>`

### Whitelist Management

- OpenClaw whitelist: `/etc/crowdsec/parsers/s02-enrich/whitelist-openclaw.yaml`
- Always whitelist:
  - OpenClaw agent IPs
  - Monitoring system IPs
  - Trusted admin IPs

### Rate Limiting

- cscli commands should be rate-limited in OpenClaw
- Recommended: Max 1 command per 10 seconds per agent
- Prevents API flooding during incidents

## Performance Characteristics

| Metric | Expected Value | Alert Threshold |
|--------|----------------|-----------------|
| Parsers EPS | 100-1000 events/sec | > 5000 |
| Decision latency | < 1 second | > 5 seconds |
| Bouncer sync | < 500ms | > 2 seconds |
| Log file size | < 100MB/day | > 500MB |

## Troubleshooting

### Common Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| cscli not found | Command fails | Run `crowdsec-skill install` |
| No bans showing | Empty decisions | Check scenarios, verify logs |
| Service inactive | status shows inactive | `crowdsec-skill services restart` |
| Firewall not blocking | IP not dropped | Check bouncer registration |

### Diagnostic Commands

```bash
# Full health check
crowdsec-skill services health

# View live logs
journalctl -u crowdsec -f

# Test scenario triggering
cscli alerts list --last 10

# Verify bouncer connection
cscli bouncers list
```

## Version Compatibility

| Component | Min Version | Recommended |
|-----------|-------------|-------------|
| CrowdSec | 1.4.0 | 1.6.0+ |
| cscli | 1.4.0 | 1.6.0+ |
| Python | 3.7 | 3.10+ |
| bash | 4.0 | 5.0+ |
| iptables | 1.6.0 | 1.8.0+ |

## Future Enhancements

1. **Cloud Bouncers**: AWS Security Groups, GCP Firewall Rules
2. **Slack/Teams Integration**: Direct alert forwarding
3. **GeoIP Enrichment**: Country-based filtering
4. **Automated Response**: Auto-ban thresholds
5. **Dashboard Export**: Grafana/Prometheus metrics

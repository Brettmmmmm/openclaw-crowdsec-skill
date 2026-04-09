# openclaw-crowdsec-skill

Next-generation security monitoring and management skill for [OpenClaw](https://github.com/anthropics/openclaw).

Query active bans, view intrusion alerts, generate security reports, manage firewall rules, and access logs — all from your OpenClaw agents via WhatsApp, CLI, or any supported channel.

## Prerequisites

- [CrowdSec](https://www.crowdsec.net/) installed and running
- `cscli` available in PATH
- Python 3 (for JSON formatting and data processing)
- Root privileges (for firewall and service management)

## Why CrowdSec Over Fail2ban?

CrowdSec represents a modern, collaborative approach to intrusion detection that significantly outperforms traditional Fail2ban deployments:

| Feature | CrowdSec | Fail2ban |
|---------|----------|----------|
| **Threat Intelligence** | Global community-driven IP reputation database | Local-only, no shared intelligence |
| **Detection Engine** | Scenario-based with pattern matching & behavioral analysis | Regex-based log parsing only |
| **Performance** | Optimized C core with efficient event processing | Python-based, can struggle under load |
| **Scalability** | Built-in API, distributed architecture | Single-server focused |
| **Bouncer System** | Pluggable enforcement (iptables, nftables, cloud firewalls) | Tied to iptables/nftables directly |
| **Community Hub** | 500+ pre-built scenarios, parsers, collections | Manual configuration required |
| **False Positive Reduction** | Community-validated scenarios, IP reputation scoring | Manual tuning required |
| **Cloud-Native** | Native support for Docker, Kubernetes, cloud firewalls | Primarily designed for bare metal |
| **Active Development** | Modern codebase, regular security updates | Mature but slower evolution |

### Key Advantages for OpenClaw

1. **Collaborative Defense**: When one CrowdSec user detects an attacker, the entire community benefits. Your OpenClaw agents get protection from threats discovered globally.
2. **Behavioral Detection**: CrowdSec analyzes patterns over time, catching sophisticated attacks that simple regex matching misses.
3. **Flexible Enforcement**: The bouncer system means you can ban IPs at the firewall level, cloud provider level, or application level — all from the same detection.
4. **Lower Maintenance**: Pre-built collections for SSH, web servers, databases, and more mean less time configuring and more time protecting.
5. **Integrated Logging**: Built-in log commands let OpenClaw agents surface security events directly to users via WhatsApp or other channels.

## Installation

### As an OpenClaw skill

```bash
cp SKILL.md /path/to/openclaw/skills/crowdsec.md
cp crowdsec-skill /usr/local/bin/crowdsec-skill
chmod +x /usr/local/bin/crowdsec-skill
```

### Standalone

```bash
git clone https://github.com/Brettmmmmm/openclaw-crowdsec-skill.git
cd openclaw-crowdsec-skill
sudo cp crowdsec-skill /usr/local/bin/
```

### Quick Install via Skill Command

```bash
crowdsec-skill install
```

This installs CrowdSec engine, firewall bouncer (iptables), and recommended collections.

## Usage

### Security Monitoring

```bash
# Quick status check
crowdsec-skill status

# List active bans
crowdsec-skill bans

# Recent alerts (last hour)
crowdsec-skill alerts 1h

# Full security report (last 7 days)
crowdsec-skill report 7d

# Engine metrics
crowdsec-skill metrics
```

### Firewall Management

```bash
# View firewall status and rules
crowdsec-skill firewall status

# Reload firewall rules
crowdsec-skill firewall reload

# Flush all bans (emergency)
crowdsec-skill firewall flush

# Switch bouncer type (iptables <-> ufw)
crowdsec-skill firewall switch ufw
```

### Log Access (OpenClaw Integration)

```bash
# Recent logs (last 20 lines)
crowdsec-skill logs recent

# Error logs only
crowdsec-skill logs errors

# Log statistics
crowdsec-skill logs stats

# Watch live logs (for interactive sessions)
crowdsec-skill logs watch
```

### Manual Actions

```bash
# Ban an IP for 48 hours
crowdsec-skill ban 1.2.3.4 48h "port scanning"

# Unban an IP
crowdsec-skill unban 1.2.3.4

# Whitelist trusted IP/network
crowdsec-skill whitelist add 10.0.0.0/8
```

### Service Management

```bash
# Full health check
crowdsec-skill services health

# Restart services
crowdsec-skill services restart
```

### Collections Management

```bash
# List installed collections
crowdsec-skill collections list

# Install nginx protection
crowdsec-skill collections install crowdsecurity/nginx
```

## OpenClaw Agent Integration

The skill is designed for these agent personas:

| Agent | Use Case | Commands |
|-------|----------|----------|
| **Pulse** (monitor) | Automated security checks, alert delivery via WhatsApp | `status`, `alerts`, `report`, `logs errors` |
| **Atlas** (infra) | Manual ban/unban, incident response, firewall management | `ban`, `unban`, `firewall`, `services` |
| **Jarvis** (orchestrator) | On-demand security status, executive summaries | `status`, `metrics`, `compare`, `report` |

### Example: WhatsApp voice command

> "Jarvis, are we under attack?"

Jarvis routes to Pulse, which runs `crowdsec-skill status` and delivers the result.

### Example: Cron-based daily digest

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

### Example: Alert on errors

```bash
# Check for errors every 15 minutes
*/15 * * * * openclaw agent --agent pulse \
  -m "Run crowdsec-skill logs errors" \
  --deliver --reply-channel whatsapp \
  --reply-to <user-number>
```

## JSON Output

Set `OUTPUT_FORMAT=json` for machine-readable output (supported on `status` command):

```bash
OUTPUT_FORMAT=json crowdsec-skill status
```

Response:
```json
{"active_bans":5,"alerts_last_hour":12,"crowdsec":"active","bouncer":"active","version":"1.3.0"}
```

## Firewall Configuration

### iptables (Default)

The skill uses iptables by default. Rules are added to a dedicated `crowdsec` chain:

```bash
crowdsec-skill firewall status
```

Shows active ban rules with line numbers.

### UFW Alternative

For systems using UFW:

```bash
crowdsec-skill firewall switch ufw
```

Ensure UFW is enabled:
```bash
ufw enable
```

### Whitelist Configuration

OpenClaw-managed whitelist location:
`/etc/crowdsec/parsers/s02-enrich/whitelist-openclaw.yaml`

Always whitelist:
- OpenClaw agent IPs
- Monitoring system IPs
- Trusted admin networks

## Comparison: Real-World Impact

### Fail2ban Approach
```
Attacker probes SSH → Log entry written → Fail2ban parses log → Regex matches → IP banned
```
- Detection happens AFTER successful log entry
- Only protects this server
- Attacker can probe other servers freely

### CrowdSec Approach
```
Attacker probes SSH → Pattern detected → IP checked against global reputation → 
  → If known bad: instant ban + community alert
  → If new: behavioral analysis → ban + share with community
```
- Detection can happen BEFORE successful authentication
- Protection shared across 50,000+ community members
- Attacker's IP becomes toxic across the entire network

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system architecture, data flows, and integration points.

## Recommended Collections

| Collection | Purpose | Priority |
|------------|---------|----------|
| `crowdsecurity/sshd` | SSH brute-force detection | Critical |
| `crowdsecurity/linux` | Base Linux security scenarios | Critical |
| `crowdsecurity/iptables` | Firewall integration | Critical |
| `crowdsecurity/linux-lpe` | Local privilege escalation | High |
| `crowdsecurity/nginx` | Web server protection | Medium |
| `crowdsecurity/apache2` | Apache protection | Medium |
| `crowdsecurity/docker` | Docker daemon protection | Medium |
| `crowdsecurity/postfix` | Mail server protection | Low |

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| `cscli not found` | Run `crowdsec-skill install` |
| No bans showing | Check scenarios with `crowdsec-skill collections list` |
| Service inactive | Run `crowdsec-skill services restart` |
| Firewall not blocking | Check bouncer with `crowdsec-skill firewall status` |
| No logs found | Check journald: `journalctl -u crowdsec` |

## License

MIT

## Author

Brett Moore (InfraForesight Ltd)

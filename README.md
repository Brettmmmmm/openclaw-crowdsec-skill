# openclaw-crowdsec-skill

CrowdSec Sentinel — security monitoring, intrusion detection, and server hardening skill for [OpenClaw](https://github.com/anthropics/openclaw).

Install, monitor, and manage CrowdSec from your OpenClaw agents via WhatsApp, CLI, or any supported channel. Includes proactive alerting, auth log analysis, firewall management, and security hardening checks.

## Prerequisites

- Linux (Debian/Ubuntu or RHEL/CentOS/Fedora)
- Python 3 (for JSON formatting)
- Root access (for install/manage commands)

CrowdSec itself is **not** required beforehand — `crowdsec-skill install` handles everything.

## Installation

### As an OpenClaw skill

```bash
git clone https://github.com/Brettmmmmm/openclaw-crowdsec-skill.git
cd openclaw-crowdsec-skill
sudo cp crowdsec-skill /usr/local/bin/
chmod +x /usr/local/bin/crowdsec-skill
cp SKILL.md /path/to/openclaw/skills/crowdsec.md
```

### First-time CrowdSec setup

```bash
crowdsec-skill install
```

This installs CrowdSec engine + firewall bouncer, configures the API key, installs recommended collections (sshd, linux, iptables, linux-lpe), and starts all services.

## Usage

### Security Monitoring

```bash
crowdsec-skill status              # Quick health check
crowdsec-skill bans [limit]        # List banned IPs
crowdsec-skill alerts [1h|24h|7d]  # Recent intrusion alerts
crowdsec-skill metrics             # CrowdSec engine metrics
crowdsec-skill report [24h|7d|30d] # Full security summary
```

### Proactive Alerting

```bash
crowdsec-skill alert               # Check for issues, returns exit codes:
                                   #   0 = all clear
                                   #   1 = warning
                                   #   2 = critical
```

### IP Management

```bash
crowdsec-skill ban 1.2.3.4 48h "port scanning"
crowdsec-skill unban 1.2.3.4
crowdsec-skill whitelist add 10.0.0.0/8
crowdsec-skill whitelist remove 1.2.3.4
crowdsec-skill whitelist list
```

### System Logs

```bash
crowdsec-skill auth recent         # Recent auth events
crowdsec-skill auth failed         # Failed login attempts
crowdsec-skill auth success        # Successful logins
crowdsec-skill auth sudo           # Sudo usage
crowdsec-skill auth stats          # Today's auth summary

crowdsec-skill syslog recent       # Recent syslog
crowdsec-skill syslog errors       # Error entries
crowdsec-skill syslog kernel       # Kernel/dmesg messages
crowdsec-skill syslog security     # Security-related events

crowdsec-skill logs recent         # CrowdSec logs
crowdsec-skill logs errors         # CrowdSec errors
crowdsec-skill logs watch          # Live tail (Ctrl+C to stop)
crowdsec-skill logs stats          # Log file statistics
```

### Firewall Management

```bash
crowdsec-skill firewall status     # Show firewall state + ipset counts
crowdsec-skill firewall reload     # Reload bouncer
crowdsec-skill firewall flush      # Clear all bans
crowdsec-skill firewall switch ufw # Switch bouncer type
```

### Log Rotation & Retention

```bash
crowdsec-skill logging status      # Current config
crowdsec-skill logging setup       # Configure logrotate
crowdsec-skill logging retention 30 # Set retention (days)
crowdsec-skill logging report 7d   # Log analysis report
crowdsec-skill logging rotate      # Force rotation now
```

### Install & Manage

```bash
crowdsec-skill install             # Full install from scratch
crowdsec-skill upgrade             # Upgrade packages + hub
crowdsec-skill services health     # Full health check
crowdsec-skill services restart    # Restart engine + bouncer
crowdsec-skill collections list    # Show installed collections
crowdsec-skill collections available # Show all available
crowdsec-skill collections install crowdsecurity/nginx
```

### Security Hardening

```bash
crowdsec-skill hardening           # Check SSH config, firewall,
                                   # permissions, update status
```

### Why CrowdSec?

```bash
crowdsec-skill compare             # CrowdSec vs Fail2ban explained
```

## OpenClaw Agent Integration

| Agent | Use Case |
|-------|----------|
| **Pulse** (monitor) | Automated security checks, alert delivery via WhatsApp |
| **Atlas** (infra) | Manual ban/unban, incident response, hardening |
| **Jarvis** (orchestrator) | On-demand security status |

### Example: Cron-based daily digest

```bash
openclaw agent --agent pulse \
  -m "Run crowdsec-skill report --period 24h and send me the summary" \
  --deliver --reply-channel whatsapp \
  --reply-to 447480265496@s.whatsapp.net
```

### Example: Proactive alerting in a cron job

```bash
crowdsec-skill alert || openclaw agent --agent pulse \
  -m "Security alert triggered — run crowdsec-skill alert and send the output" \
  --deliver --reply-channel whatsapp \
  --reply-to 447480265496@s.whatsapp.net
```

## JSON Output

```bash
OUTPUT_FORMAT=json crowdsec-skill status
# {"active_bans":100,"alerts_last_hour":50,"crowdsec":"active","bouncer":"active","version":"1.5.0"}
```

## License

MIT — Brett Moore / InfraForesight Ltd

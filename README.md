# openclaw-crowdsec-skill

CrowdSec security monitoring and management skill for [OpenClaw](https://github.com/anthropics/openclaw).

Query active bans, view intrusion alerts, generate security reports, and manage IP decisions — all from your OpenClaw agents via WhatsApp, CLI, or any supported channel.

## Prerequisites

- [CrowdSec](https://www.crowdsec.net/) installed and running
- `cscli` available in PATH
- Python 3 (for JSON formatting)

## Installation

### As an OpenClaw skill

Copy the skill files into your OpenClaw skills directory:

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

## Usage

```bash
# Quick status check
crowdsec-skill status

# List active bans
crowdsec-skill bans

# Recent alerts (last hour)
crowdsec-skill alerts 1h

# Ban an IP for 48 hours
crowdsec-skill ban 1.2.3.4 48h "port scanning"

# Unban
crowdsec-skill unban 1.2.3.4

# Full security report (last 7 days)
crowdsec-skill report 7d

# CrowdSec engine metrics
crowdsec-skill metrics
```

## OpenClaw Agent Integration

The skill is designed for these agent personas:

| Agent | Use Case |
|-------|----------|
| **Pulse** (monitor) | Automated security checks, alert delivery via WhatsApp |
| **Atlas** (infra) | Manual ban/unban, incident response |
| **Jarvis** (orchestrator) | On-demand security status |

### Example: WhatsApp voice command

> "Jarvis, are we under attack?"

Jarvis routes to Pulse, which runs `crowdsec-skill status` and delivers the result.

### Example: Cron-based daily digest

Add to your OpenClaw cron jobs:

```bash
openclaw agent --agent pulse -m "Run crowdsec-skill report --period 24h and send me the summary" --deliver --reply-channel whatsapp --reply-to 447480265496@s.whatsapp.net
```

## JSON Output

Set `OUTPUT_FORMAT=json` for machine-readable output (currently supported on the `status` command):

```bash
OUTPUT_FORMAT=json crowdsec-skill status
```

## License

MIT

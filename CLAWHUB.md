# CrowdSec Sentinel

**Version:** 1.5.0  
**Author:** Brett Moore (InfraForesight Ltd)  
**License:** MIT  
**Repository:** https://github.com/Brettmmmmm/openclaw-crowdsec-skill  
**ClawHub Category:** Security & Monitoring

## Overview

CrowdSec Sentinel is a comprehensive security monitoring and management skill for OpenClaw. It provides command-and-control for your VPA's security posture, integrating CrowdSec intrusion detection with system log monitoring, proactive alerting, security hardening checks, and professional log management.

## Why "Sentinel"?

A sentinel stands guard, watching for threats and raising alarms. This skill embodies that role for your OpenClaw deployment:

- **Vigilant Monitoring**: Continuous security status checks
- **Proactive Alerting**: Automated threat detection with severity levels
- **Command & Control**: Centralized security management via OpenClaw agents
- **Best Practices**: Built-in hardening checks for your VPA
- **Professional Logging**: Log rotation, retention policies, and analysis reports

## Features

### Security Monitoring
- Real-time CrowdSec status (bans, alerts, service health)
- Active ban management with IP, reason, and expiry tracking
- Recent attack alerts with source IP and scenario details
- Engine metrics and performance monitoring

### Proactive Alerting
- Automated security checks with exit codes for automation
- Failed login monitoring with configurable thresholds
- Service health monitoring (CrowdSec, bouncer)
- Ban count anomaly detection
- Integration with OpenClaw alert delivery (WhatsApp, etc.)

### System Log Integration
- **Auth logs**: Failed/successful logins, sudo usage, stats
- **Syslog**: System events, errors, security events, kernel messages
- **Kernel logs**: dmesg output for hardware/driver issues
- **CrowdSec logs**: Engine-specific logging with error filtering

### Log Management (Best Practices)
- **Automatic rotation**: Daily log rotation with compression
- **Retention policies**: Configurable retention (default 30 days)
- **Log reports**: Periodic analysis reports with statistics
- **Disk management**: Automatic cleanup of old compressed logs
- **Journald integration**: Falls back to journald when file logs unavailable

### Firewall Management
- iptables and UFW support
- Rule viewing and counting
- Emergency ban flush
- Bouncer type switching

### Security Hardening
- SSH configuration audit (root login, password auth, empty passwords)
- Firewall status verification
- Automatic security updates check
- World-writable file detection
- Fail2ban conflict detection (should not run with CrowdSec)

## Installation

### Quick Install
```bash
crowdsec-skill install
```

This installs CrowdSec, configures firewall bouncer, installs recommended collections, and sets up log rotation.

### Manual Install
```bash
git clone https://github.com/Brettmmmmm/openclaw-crowdsec-skill.git
cd openclaw-crowdsec-skill
sudo cp crowdsec-skill /usr/local/bin/
sudo cp SKILL.md /path/to/openclaw/skills/crowdsec.md
```

## Usage Examples

### Daily Security Check
```bash
crowdsec-skill status
crowdsec-skill alert
```

### Check Failed Logins
```bash
crowdsec-skill auth failed
crowdsec-skill auth stats
```

### Security Hardening
```bash
crowdsec-skill hardening
```

### Log Management
```bash
# View logging configuration
crowdsec-skill logging status

# Set up log rotation (best practices)
crowdsec-skill logging setup

# Generate weekly log report
crowdsec-skill logging report 7d

# Change retention to 60 days
crowdsec-skill logging retention 60

# Force log rotation
crowdsec-skill logging rotate
```

### View Security Events
```bash
crowdsec-skill syslog security
crowdsec-skill logs errors
```

## OpenClaw Integration

### Agent Personas

| Agent | Commands | Use Case |
|-------|----------|----------|
| **Pulse** | `alert`, `status`, `auth failed`, `logging report` | Automated monitoring, WhatsApp alerts, log analysis |
| **Atlas** | `ban`, `unban`, `firewall`, `hardening`, `logging setup` | Incident response, security management, log config |
| **Jarvis** | `status`, `report`, `compare`, `logging report` | Executive summaries, on-demand queries, compliance reports |

### Cron Automation

```bash
# Proactive security check every 15 minutes
*/15 * * * * crowdsec-skill alert >/dev/null 2>&1 || \
  openclaw agent --agent pulse -m "Security alert detected - check system" \
  --deliver --reply-channel whatsapp --reply-to <number>

# Daily security report at 08:00
0 8 * * * openclaw agent --agent pulse \
  -m "Run crowdsec-skill report --period 24h" \
  --deliver --reply-channel whatsapp --reply-to <number>

# Weekly log analysis report (Monday 09:00)
0 9 * * 1 openclaw agent --agent pulse \
  -m "Run crowdsec-skill logging report 7d" \
  --deliver --reply-channel whatsapp --reply-to <number>

# Hourly failed login check
0 * * * * openclaw agent --agent pulse \
  -m "Run crowdsec-skill auth stats" \
  --deliver --reply-channel whatsapp --reply-to <number>
```

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Active bans | ≥ 20 | - |
| Alerts/hour | ≥ 10 | - |
| Failed logins/day | ≥ 5 | ≥ 10 |
| Service down | - | Immediate |

## Commands Reference

### Monitoring
- `status` - Overview of security posture
- `bans [limit]` - List active bans
- `alerts [since]` - Recent alerts
- `metrics` - Engine performance
- `report [period]` - Security summary

### Proactive
- `alert` - Proactive check with exit codes (0=OK, 1=warn, 2=critical)

### Logs
- `auth <recent|failed|success|sudo|stats>` - Authentication logs
- `syslog <recent|errors|kernel|security>` - System logs
- `logs <recent|errors|watch|stats>` - CrowdSec logs

### Log Management
- `logging status` - View logging configuration
- `logging setup` - Configure log rotation (best practices)
- `logging retention <days>` - Set retention period
- `logging report [period]` - Generate log analysis report
- `logging rotate` - Force log rotation

### Actions
- `ban <ip> [duration] [reason]` - Ban an IP
- `unban <ip>` - Remove ban
- `firewall <status|reload|flush|switch>` - Firewall management
- `whitelist <add|remove|list>` - Manage whitelist

### Management
- `install` - Install CrowdSec with log rotation
- `upgrade` - Upgrade CrowdSec
- `services <start|stop|restart|health>` - Service control
- `collections <list|install|remove>` - Manage collections
- `hardening` - Security best practices check

## Log Management Best Practices

### Default Configuration
- **Rotation**: Daily
- **Retention**: 30 days
- **Compression**: Enabled (gzip)
- **Permissions**: 0640 root:adm
- **Post-rotation**: CrowdSec reload

### Custom Retention
```bash
# Keep logs for 90 days (compliance)
crowdsec-skill logging retention 90

# Keep logs for 7 days (minimal disk usage)
crowdsec-skill logging retention 7
```

### Log Report Output
The `logging report` command provides:
- Total log entries count
- Error/fatal/critical entry count
- Ban-related events count
- Failed/successful login stats
- Disk usage breakdown

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system architecture.

## Requirements

- CrowdSec 1.4.0+ (installed by skill)
- Python 3.7+
- bash 4.0+
- Root privileges (for firewall, service, and log management)
- Systemd (for service management)
- logrotate (recommended, optional)

## Why CrowdSec Over Fail2ban?

| Feature | CrowdSec | Fail2ban |
|---------|----------|----------|
| Threat Intelligence | Global community | Local only |
| Detection | Behavioral analysis | Regex matching |
| Performance | C-based core | Python-based |
| Architecture | Distributed | Single-server |
| Enforcement | Pluggable bouncers | Direct iptables |
| Scenarios | 500+ pre-built | Manual config |
| Logging | Centralized with API | File-based only |

## Files Included

| File | Purpose |
|------|---------|
| `crowdsec-skill` | Main executable script |
| `SKILL.md` | OpenClaw skill definition |
| `README.md` | User documentation |
| `ARCHITECTURE.md` | Technical architecture |
| `CLAWHUB.md` | This file (ClawHub package info) |
| `LICENSE` | MIT license |
| `skill.json` | Skill metadata |

## License

MIT License - See [LICENSE](./LICENSE) for details.

## Support

- Documentation: See README.md, SKILL.md, ARCHITECTURE.md
- Issues: https://github.com/Brettmmmmm/openclaw-crowdsec-skill/issues
- CrowdSec Docs: https://docs.crowdsec.net/

## Changelog

### v1.5.0 - Log Management Release
- Added `logging` command suite for professional log management
- `logging setup` - Configures logrotate with best practices
- `logging retention <days>` - Set custom retention periods
- `logging report [period]` - Generate analysis reports
- `logging rotate` - Force log rotation
- Automatic log rotation setup during install
- Journald fallback when file logs unavailable

### v1.4.0 - Sentinel Release
- Added proactive `alert` command with exit codes
- Added `auth` log monitoring (failed logins, sudo)
- Added `syslog` monitoring (errors, kernel, security)
- Added `hardening` security best practices checker
- Enhanced OpenClaw integration for automated alerting
- Configurable alert thresholds

### v1.3.0
- Added firewall management (iptables/UFW)
- Added log viewing commands
- UFW bouncer support

### v1.2.0
- Added `compare` command (CrowdSec vs Fail2ban)
- Improved ban/alert formatting

### v1.1.0
- Added collection management
- Added whitelist management
- Added service health checks

### v1.0.0
- Initial release

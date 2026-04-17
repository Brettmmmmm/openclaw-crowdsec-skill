---
name: taylor-swift-tickets
description: |
  Taylor Swift UK Ticket Monitor — uses a Dockerised Playwright browser
  to check Ticketmaster, See Tickets, Gigsandtours, Live Nation, and AXS
  for ticket availability. Monitoring only, not purchasing.
  Alerts via OpenClaw when tickets go on sale.
triggers:
  - "taylor swift tickets"
  - "check tickets"
  - "ticket availability"
  - "taylor swift uk"
  - "when do tickets go on sale"
  - "watch for tickets"
  - "ticket alert"
  - "monitor tickets"
  - "any tickets available"
  - "ticketmaster taylor swift"
  - "set up ticket monitor"
---

# Taylor Swift UK Ticket Monitor Skill

Monitors UK ticketing sites for Taylor Swift ticket availability using a real browser running in Docker (Playwright + Chromium).

**Legal notice:** This skill monitors availability only. It does not automate purchases or assist with resale. Automated ticket purchasing for resale is an offence under the UK Digital Economy Act 2017.

## Setup (run once)

Trigger: "set up ticket monitor", "build ticket checker"

```bash
tickets-skill setup
```

Builds the Playwright Docker image with Chromium (~500 MB, one-time).

## One-Shot Check

Trigger: "check taylor swift tickets", "any tickets available"

```bash
tickets-skill check
tickets-skill check --sites ticketmaster,seetickets
tickets-skill check --json
```

Returns exit 0 if tickets found, exit 1 if none.

## Continuous Monitoring

Trigger: "watch for tickets", "monitor tickets every 5 minutes"

```bash
tickets-skill watch 5m
tickets-skill watch 10m ticketmaster,axs
tickets-skill watch 5m all
```

Polls on the given interval and fires `openclaw-notify` if tickets appear.

## Screenshots

Trigger: "screenshot the ticket site", "show me the ticketmaster page"

```bash
tickets-skill screenshot
tickets-skill screenshot ticketmaster
```

Saves browser screenshots to `/tmp/ticket-screenshots/` for verification.

## Available Sites

| ID | Site |
|----|------|
| `ticketmaster` | Ticketmaster UK |
| `seetickets` | See Tickets |
| `gigsandtours` | Gigsandtours |
| `livenation` | Live Nation UK |
| `axs` | AXS UK |

```bash
tickets-skill sites          # list all
tickets-skill status         # image/config info
```

## Agent Routing

| Agent | Commands | Use Case |
|-------|----------|----------|
| **Pulse** | `watch`, `check` | Automated polling, WhatsApp alert when found |
| **Jarvis** | `check` | On-demand status query |
| **Atlas** | `setup`, `status` | First-time setup, maintenance |

## Example Flows

### WhatsApp: "Jarvis, any Taylor Swift tickets?"
```
Jarvis -> tickets-skill check
Jarvis -> formats result
Jarvis -> delivers via WhatsApp
```

### Cron: Check every 5 minutes, alert on availability
```bash
*/5 * * * * /usr/local/bin/tickets-skill check --json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d['available_count'] else 1)" \
  && openclaw agent --agent pulse \
       -m "Taylor Swift tickets available! Check sites now." \
       --deliver --reply-channel whatsapp --reply-to <number>
```

### Continuous watch with built-in alerting
```bash
tickets-skill watch 5m
```

## Requirements

- Docker (image built via `tickets-skill setup`)
- ~500 MB disk for the Playwright/Chromium image
- Internet access to reach UK ticketing sites

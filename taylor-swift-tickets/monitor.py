#!/usr/bin/env python3
"""
Taylor Swift UK Ticket Monitor
Checks multiple UK ticketing sites for ticket availability using a real browser.

MONITORING ONLY — does not purchase tickets.
UK Digital Economy Act 2017: automated purchasing for resale is illegal.
Use this tool to be alerted when tickets go on sale, then buy manually.
"""

import asyncio
import json
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

SITES = [
    {
        "id": "ticketmaster",
        "name": "Ticketmaster UK",
        "url": "https://www.ticketmaster.co.uk/search?q=taylor+swift",
        "available_keywords": ["buy tickets", "get tickets", "on sale", "book now", "buy now"],
        "unavail_keywords": ["no events found", "no results found", "0 events"],
    },
    {
        "id": "seetickets",
        "name": "See Tickets",
        "url": "https://www.seetickets.com/search?q=taylor+swift",
        "available_keywords": ["buy tickets", "book tickets", "on sale", "add to basket"],
        "unavail_keywords": ["no results", "nothing found", "0 results"],
    },
    {
        "id": "gigsandtours",
        "name": "Gigsandtours",
        "url": "https://www.gigsandtours.com/tour/taylor-swift",
        "available_keywords": ["buy tickets", "book now", "on sale now", "get tickets"],
        "unavail_keywords": ["no tour dates", "no upcoming", "no shows"],
    },
    {
        "id": "livenation",
        "name": "Live Nation UK",
        "url": "https://www.livenation.co.uk/artist/taylor-swift-tickets",
        "available_keywords": ["buy tickets", "get tickets", "on sale", "book now"],
        "unavail_keywords": ["no upcoming events", "no events", "no shows scheduled"],
    },
    {
        "id": "axs",
        "name": "AXS UK",
        "url": "https://www.axs.com/search?q=taylor+swift&country=GB",
        "available_keywords": ["buy tickets", "get tickets", "on sale", "find tickets"],
        "unavail_keywords": ["no results", "no events found"],
    },
]

# Date pattern for extracting event info from page text
DATE_RE = re.compile(
    r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)?\s*"
    r"(\d{1,2})\s+"
    r"(january|february|march|april|may|june|july|august|september|october|november|december|"
    r"jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    r"\s+(20\d{2})",
    re.IGNORECASE,
)

UK_VENUES = [
    "wembley", "o2", "tottenham", "london", "manchester", "birmingham",
    "glasgow", "cardiff", "leeds", "sheffield", "liverpool", "newcastle",
    "edinburgh", "bristol", "nottingham", "arena", "stadium", "ground",
]


def extract_events(text: str) -> list[str]:
    """Pull date-containing lines that look like UK event listings."""
    events = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        if DATE_RE.search(line) and len(line) < 250:
            # Widen the context window to grab venue/artist info nearby
            ctx = " | ".join(lines[max(0, i - 2): min(len(lines), i + 4)])
            if "taylor swift" in ctx.lower() or any(v in ctx.lower() for v in UK_VENUES):
                events.append(ctx[:300])
    return events[:10]


async def check_site(page, site: dict, screenshot_dir: str | None, verbose: bool) -> dict:
    result = {
        "id": site["id"],
        "name": site["name"],
        "url": site["url"],
        "status": "unknown",
        "available": False,
        "events": [],
        "error": None,
        "checked_at": datetime.utcnow().isoformat() + "Z",
    }

    try:
        if verbose:
            print(f"  Checking {site['name']} ...", file=sys.stderr)

        await page.goto(site["url"], wait_until="domcontentloaded", timeout=30_000)

        # Give JS-heavy pages a moment to render
        await asyncio.sleep(2)
        try:
            await page.wait_for_load_state("networkidle", timeout=8_000)
        except PlaywrightTimeout:
            pass  # take what we have

        text = await page.evaluate("() => document.body.innerText")
        text_lower = text.lower()

        has_available = any(kw in text_lower for kw in site["available_keywords"])
        has_unavail = any(kw in text_lower for kw in site["unavail_keywords"])

        result["events"] = extract_events(text)
        result["available"] = has_available and not has_unavail
        result["status"] = "ok"

        if screenshot_dir:
            path = Path(screenshot_dir) / f"{site['id']}.png"
            await page.screenshot(path=str(path))
            result["screenshot"] = str(path)

    except PlaywrightTimeout:
        result["status"] = "timeout"
        result["error"] = "Page load timed out"
    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)

    return result


async def run(sites: list[dict], screenshot_dir: str | None, verbose: bool) -> list[dict]:
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="en-GB",
        )
        page = await ctx.new_page()

        for site in sites:
            result = await check_site(page, site, screenshot_dir, verbose)
            results.append(result)

        await browser.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Taylor Swift UK Ticket Monitor")
    parser.add_argument(
        "--sites",
        default="all",
        help="Comma-separated site IDs, or 'all' (default)",
    )
    parser.add_argument("--json", action="store_true", dest="json_out", help="JSON output")
    parser.add_argument("--screenshots", metavar="DIR", help="Save screenshots to DIR")
    parser.add_argument("--verbose", action="store_true", help="Progress to stderr")
    parser.add_argument("--list-sites", action="store_true", help="Print available site IDs")
    args = parser.parse_args()

    if args.list_sites:
        for s in SITES:
            print(f"{s['id']:<16} {s['name']}")
        return

    if args.sites == "all":
        sites = SITES
    else:
        ids = {s.strip() for s in args.sites.split(",")}
        sites = [s for s in SITES if s["id"] in ids]
        if not sites:
            print(f"ERROR: no recognised site IDs in '{args.sites}'", file=sys.stderr)
            sys.exit(1)

    if args.screenshots:
        Path(args.screenshots).mkdir(parents=True, exist_ok=True)

    results = asyncio.run(run(sites, args.screenshots, args.verbose))
    available = [r for r in results if r["available"]]

    if args.json_out:
        print(json.dumps({
            "checked_at": datetime.utcnow().isoformat() + "Z",
            "available_count": len(available),
            "results": results,
        }, indent=2))
        sys.exit(0 if available else 1)

    # Human-readable output
    print(f"\nTaylor Swift UK Ticket Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)

    for r in results:
        if r["status"] == "ok":
            label = "*** TICKETS AVAILABLE ***" if r["available"] else "none found"
        else:
            label = f"[{r['status']}] {r.get('error', '')}"

        print(f"\n{r['name']}: {label}")
        for event in r.get("events", []):
            print(f"  • {event}")
        print(f"  {r['url']}")

    print("\n" + "=" * 62)
    if available:
        print(f"ALERT: Possible availability on {len(available)} site(s) — check links above!")
        sys.exit(0)
    else:
        print("No tickets found at this time.")
        sys.exit(1)


if __name__ == "__main__":
    main()

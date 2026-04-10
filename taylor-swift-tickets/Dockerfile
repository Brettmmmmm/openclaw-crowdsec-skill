# Pinned to Bookworm (Debian 12) — Playwright's --with-deps fails on Trixie (Debian 13)
# due to missing ttf-unifont / ttf-ubuntu-font-family packages in that release.
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install Playwright and Chromium with all system dependencies
RUN pip install --no-cache-dir playwright==1.44.0 && \
    playwright install chromium --with-deps

COPY monitor.py .

ENTRYPOINT ["python", "monitor.py"]

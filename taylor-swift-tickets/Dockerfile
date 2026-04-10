FROM python:3.11-slim

WORKDIR /app

# Install Playwright and Chromium with all system dependencies
RUN pip install --no-cache-dir playwright==1.44.0 && \
    playwright install chromium --with-deps

COPY monitor.py .

ENTRYPOINT ["python", "monitor.py"]

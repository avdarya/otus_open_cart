FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget unzip ca-certificates gnupg \
    chromium chromium-driver firefox-esr \
    && wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && wget -O /tmp/yandexdriver.zip https://github.com/yandex/yandexdriver/releases/download/vLATEST/yandexdriver_linux64.zip || true \
    && unzip -o /tmp/yandexdriver.zip -d /usr/local/bin/ || true \
    && chmod +x /usr/local/bin/yandexdriver || true \
    && rm -rf /tmp/geckodriver.tar.gz /tmp/yandexdriver.zip /var/lib/apt/lists/*

WORKDIR /root/opencart
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV GECKODRIVER_PATH=/usr/local/bin/geckodriver
ENV FIREFOX_BIN=/usr/bin/firefox-esr
ENV YANDEXDRIVER_PATH=/usr/local/bin/yandexdriver
ENV IN_DOCKER=true

COPY entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
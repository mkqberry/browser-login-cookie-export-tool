# YouTube Login Tool

Automate browser login to YouTube and export session cookies. Used to bypass rate limits and authentication requirements in downstream data collection tools.

## Features

- Selenium-based browser automation
- YouTube login handling (2FA support)
- Cookie extraction and serialization
- Cookie refresh capability
- Account rotation for multi-user scenarios

## Setup

```bash
pip install -r requirements.txt
```

Download ChromeDriver matching your Chrome version:
https://chromedriver.chromium.org/

## Usage

Login and export cookies:

```bash
python scripts/main.py \
  --email your.email@gmail.com \
  --password your-password \
  --output cookies.txt \
  --headless false  # Show browser for 2FA
```

With multiple accounts (for rotation):

```bash
python scripts/main.py \
  --account-list accounts.csv \
  --output-dir cookies_per_account/ \
  --rotate true
```

## Stored Format

Cookies exported as Netscape cookie file (compatible with curl, aria2, yt-dlp).

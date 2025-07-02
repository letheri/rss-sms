# News SMS Bot

A Python script that fetches recent news articles from RSS feeds, summarizes them using AI, and sends the summaries via SMS to your phone using Android Debug Bridge (ADB).

## Features

- Fetches articles from RSS feeds (currently only configured for Ars Technica)
- Filters articles from the last 24 hours
- Scrapes full article content from web pages
- Summarizes articles using Hugging Face transformers
- Splits long summaries into SMS-sized chunks (320 characters each)
- Sends SMS messages via ADB to connected Android device

## Requirements

- Python 3.x
- Android device with USB debugging enabled
- ADB (Android Debug Bridge) installed and configured
- Required Python packages (install with `pip install -r requirements.txt`):
  - transformers
  - feedparser
  - beautifulsoup4
  - torch (for transformers)

## Setup

1. Install required packages:
   ```bash
   pip install transformers feedparser beautifulsoup4 torch
   ```

2. Enable USB debugging on your Android device:
   - Go to Settings > Developer Options > USB Debugging
   - Connect your device to your computer via USB

3. Install ADB and verify connection:
   ```bash
   adb devices
   ```

4. Update the `TARGET_NUMBER` variable in the script with your phone number

## Usage

Run the script:
```bash
python news_sms_bot.py
```

The script will:
1. Check RSS feeds for articles from the last 24 hours
2. Scrape and summarize each new article
3. Send SMS summaries to the specified phone number

## Configuration

- `TARGET_NUMBER`: Phone number to send SMS messages to
- `SMS_CHAR_COUNT`: Maximum characters per SMS (default: 320)
- `url`: List of RSS feed URLs to monitor
- `time_range`: How far back to look for articles (default: 1 day)

## Notes

- Currently only supports Ars Technica article scraping
- Your Android device must remain connected via USB
- The AI summarization model will be downloaded on first run
- Designed to be used with daily scheduled task
- ABD SMS service sometimes does not send first part of the 2 SMS's

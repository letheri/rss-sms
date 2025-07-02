import os
from transformers import pipeline
import feedparser as fp
from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup

TARGET_NUMBER = "+90506 xxx xxxx"
SMS_CHAR_COUNT = 320

summarizer = pipeline("summarization", model="Falconsai/text_summarization")
url = [
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.technopat.net/feed/",
]
feed = fp.parse(url[0])

# Define the time range (e.g., the last 24 hours)
now = datetime.now()
time_range = timedelta(days=1)
# Iterate through entries and filter by the time range
for entry in feed.entries:
    entry_date = (
        datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    ).replace(tzinfo=None)
    if now - entry_date <= time_range:
        print("Entry Title:", entry.title)
        print("Entry Link:", entry.link)
        print("\n")

        # Data scrapping to get article contents
        if 'arstechnica' in entry.link:
            html = urlopen(entry.link).read()
            soup = BeautifulSoup(html, features="html.parser")
            specific_class_element = soup.find(class_="article-content")
            paragraphs = specific_class_element.find_all("p")
        
        article_paragraph_content = ""
        for paragraph in paragraphs:
            article_paragraph_content += paragraph.get_text()
        
        # Get the summary of the article content
        # Summarized text can be of maximum of 2 SMS's
        summary = summarizer(
            article_paragraph_content,
            max_length=SMS_CHAR_COUNT * 2,
            min_length=30,
            do_sample=False,
        )[0]["summary_text"]

        # Split the summarized text into 2 parts
        parts = [
            summary[i : i + SMS_CHAR_COUNT]
            for i in range(0, len(summary), SMS_CHAR_COUNT)
        ]

        # With ADB, use Android SMS service on a connected phone
        for part in parts:
            message = part.replace("'", "")
            code = f"""adb shell service call isms 5 i32 0 s16 "com.android.mms.service" s16 "null" s16 "{TARGET_NUMBER}" s16 "null" s16 "'{message}'" s16 "null" s16 "null" i32 0 i64 0"""
            print(code)
            os.system(code)
    

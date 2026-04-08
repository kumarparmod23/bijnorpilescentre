#!/usr/bin/env python3
"""Submit today's new URLs to Google Indexing API + Bing IndexNow."""
import os, json, glob, datetime, pathlib, re, sys, requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

REPO   = pathlib.Path(__file__).resolve().parent.parent
SITE   = "https://bijnorpilescentre.com"
today  = datetime.date.today().isoformat()

def google_service():
    info  = json.loads(os.environ["GOOGLE_INDEXING_JSON"])
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/indexing"])
    return build("indexing", "v3", credentials=creds, cache_discovery=False)

def post_urls():
    svc  = google_service()
    key  = os.environ.get("INDEXNOW_KEY", "")
    files = glob.glob(str(REPO / "_posts" / "*" / f"{today}-*.md"))
    if not files:
        print("No new posts found for", today); return
    for f in files:
        lang = "en" if f"{os.sep}en{os.sep}" in f else "hi"
        slug = re.sub(r".*-\d{4}-\d{2}-\d{2}-", "", os.path.basename(f)).replace(".md", "")
        url  = f"{SITE}/{lang}/{slug}/"
        try:
            svc.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}).execute()
            print("Google:", url)
        except Exception as e:
            print("Google FAILED:", url, e)
        if key:
            r = requests.get("https://api.indexnow.org/indexnow",
                             params={"url": url, "key": key})
            print("IndexNow:", r.status_code, url)

    # Ping sitemap
    try:
        requests.get(f"https://www.google.com/ping?sitemap={SITE}/sitemap.xml")
        requests.get(f"https://www.bing.com/ping?sitemap={SITE}/sitemap.xml")
        print("Sitemap pinged.")
    except Exception as e:
        print("Sitemap ping failed:", e)

if __name__ == "__main__":
    post_urls()

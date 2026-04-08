#!/usr/bin/env python3
"""
Cowork Daily Blog Runner — Bijnor Piles Centre
Runs every morning at 06:00 IST via Cowork scheduled task.
Generates 1 English + 1 Hindi SEO blog post and pushes directly to GitHub via REST API.

REQUIRED ENV VARS (set in your system environment or edit SECRETS section below):
  ANTHROPIC_API_KEY   — your Claude API key (https://console.anthropic.com)
  GITHUB_PAT          — GitHub fine-grained PAT with Contents: Read+Write on bijnorpilescentre repo
"""
import os, json, datetime, re, base64, urllib.request, urllib.error, time

# ─── SECRETS (edit here OR set as environment variables) ───────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GITHUB_PAT        = os.environ.get("GITHUB_PAT", "")
GITHUB_OWNER      = "kumarparmod23"
GITHUB_REPO       = "bijnorpilescentre"
SITE_URL          = "https://kumarparmod23.github.io/bijnorpilescentre"
# ────────────────────────────────────────────────────────────────────────────

CALENDAR = [
  {"english": "What Are Piles? Causes, Symptoms & Modern Treatment Options", "hindi": "बवासीर क्या है? कारण, लक्षण और आधुनिक इलाज", "condition": "Piles"},
  {"english": "Anal Fissure Explained: Why It Happens and How to Heal", "hindi": "एनल फिशर क्यों होता है और इसका इलाज कैसे करें", "condition": "Fissure"},
  {"english": "Anal Fistula: Symptoms You Should Never Ignore", "hindi": "भगन्दर (फिस्टुला) के लक्षण जिन्हें नज़रअंदाज़ न करें", "condition": "Fistula"},
  {"english": "Pilonidal Sinus: Causes, Risks and Permanent Cure", "hindi": "पाइलोनिडल साइनस: कारण और स्थायी इलाज", "condition": "Pilonidal Sinus"},
  {"english": "Kshar Sutra Therapy: Ancient Ayurvedic Cure for Fistula", "hindi": "क्षार सूत्र चिकित्सा: भगन्दर का प्राचीन आयुर्वेदिक इलाज", "condition": "Fistula"},
  {"english": "Kshar Karma: Painless Treatment for Piles", "hindi": "क्षार कर्म: बवासीर का बिना दर्द इलाज", "condition": "Piles"},
  {"english": "Rubber Band Ligation: How It Works and Recovery", "hindi": "रबर बैंड लिगेशन क्या है और रिकवरी कैसे होती है", "condition": "Piles"},
  {"english": "Top 7 Foods to Eat If You Have Piles", "hindi": "बवासीर में खाने योग्य 7 सबसे अच्छी चीज़ें", "condition": "Piles"},
  {"english": "Foods to Avoid in Piles, Fissure and Fistula", "hindi": "बवासीर, फिशर और भगन्दर में क्या नहीं खाना चाहिए", "condition": "Piles"},
  {"english": "Myths vs Facts About Piles Surgery", "hindi": "बवासीर सर्जरी के बारे में मिथक और सच्चाई", "condition": "Piles"},
  {"english": "Bleeding While Passing Stool — When to See a Doctor", "hindi": "मल त्याग के समय खून आना — डॉक्टर को कब दिखाएँ", "condition": "Piles"},
  {"english": "Constipation: The #1 Cause of Anorectal Problems", "hindi": "कब्ज: गुदा रोगों का सबसे बड़ा कारण", "condition": "Piles"},
  {"english": "Lifestyle Changes to Prevent Piles Naturally", "hindi": "बवासीर से बचाव के लिए जीवनशैली में बदलाव", "condition": "Piles"},
  {"english": "Internal vs External Piles: Difference and Treatment", "hindi": "आंतरिक और बाहरी बवासीर में अंतर", "condition": "Piles"},
  {"english": "Pre-Treatment Care Before Kshar Sutra Therapy", "hindi": "क्षार सूत्र से पहले की तैयारी", "condition": "Fistula"},
  {"english": "Post-Treatment Recovery Tips for Piles Patients", "hindi": "बवासीर इलाज के बाद रिकवरी टिप्स", "condition": "Piles"},
  {"english": "Why Ayurveda Works Best for Fistula", "hindi": "फिस्टुला के लिए आयुर्वेद क्यों सबसे बेहतर है", "condition": "Fistula"},
  {"english": "Pregnancy and Piles: Safe Treatment Options", "hindi": "गर्भावस्था में बवासीर: सुरक्षित उपचार", "condition": "Piles"},
  {"english": "Piles in Young Adults: A Growing Concern", "hindi": "युवाओं में बढ़ता बवासीर — एक चेतावनी", "condition": "Piles"},
  {"english": "Sitz Bath: Benefits and Correct Method", "hindi": "सिट्ज़ बाथ कैसे लें और इसके फायदे", "condition": "Fissure"},
  {"english": "Office Job and Piles: Sitting Too Long Risks", "hindi": "ऑफिस जॉब और बवासीर: लंबे समय तक बैठने के नुकसान", "condition": "Piles"},
  {"english": "Recurring Fissure: Why It Comes Back", "hindi": "बार-बार फिशर क्यों होता है?", "condition": "Fissure"},
  {"english": "High-Fiber Indian Diet Plan for Piles Patients", "hindi": "बवासीर रोगियों के लिए भारतीय हाई-फाइबर डाइट", "condition": "Piles"},
  {"english": "Yoga Asanas That Help Cure Piles", "hindi": "बवासीर ठीक करने में मददगार योगासन", "condition": "Piles"},
  {"english": "When Is Surgery Necessary for Piles?", "hindi": "बवासीर में सर्जरी कब ज़रूरी होती है?", "condition": "Piles"},
  {"english": "Patient FAQs About Kshar Sutra Treatment", "hindi": "क्षार सूत्र चिकित्सा पर मरीज़ों के सवाल-जवाब", "condition": "Fistula"},
  {"english": "Hydration and Anorectal Health", "hindi": "पानी पीना और गुदा स्वास्थ्य", "condition": "Piles"},
  {"english": "Children and Anal Fissure: A Parent's Guide", "hindi": "बच्चों में फिशर: माता-पिता के लिए जानकारी", "condition": "Fissure"},
  {"english": "Why Choose Bijnor Piles Centre for Treatment", "hindi": "बिजनौर पाइल्स सेंटर क्यों चुनें", "condition": "Piles"},
  {"english": "Success Stories: Patients Cured by Kshar Sutra", "hindi": "क्षार सूत्र से ठीक हुए मरीज़ों की कहानियाँ", "condition": "Fistula"},
]

INTERNAL = {
    "en": {"piles":"/bijnorpilescentre/en/what-are-piles/","fissure":"/bijnorpilescentre/en/anal-fissure-explained/","fistula":"/bijnorpilescentre/en/anal-fistula-symptoms/"},
    "hi": {"piles":"/bijnorpilescentre/hi/bawasir-kya-hai/","fissure":"/bijnorpilescentre/hi/anal-fissure-ilaj/","fistula":"/bijnorpilescentre/hi/bhagandar-lakshan/"},
}
LABELS = {
    "en": {"piles":"Piles (Hemorrhoids)","fissure":"Anal Fissure","fistula":"Anal Fistula"},
    "hi": {"piles":"बवासीर","fissure":"एनल फिशर","fistula":"भगन्दर"},
}

TODAY      = datetime.date.today()
START_DATE = datetime.date(2026, 4, 7)
DAY_IDX    = (TODAY - START_DATE).days % len(CALENDAR)
TOPIC      = CALENDAR[DAY_IDX]

SYSTEM = """You are Dr. Parmod Kumar, a senior proctologist at Bijnor Piles Centre,
Kiratpur Road, Bijnor, Uttar Pradesh 246701, India (phone +91 70177 90760).
You write warm, authoritative, patient-friendly medical blog posts following Google's
E-E-A-T and YMYL guidelines. Never promise a 'guaranteed cure'. Always advise
consulting a qualified doctor. Use simple language ordinary Indian patients understand."""

EN_PROMPT = '''Write a complete SEO-optimized English blog post on: "{topic}"

STRUCTURE (Markdown):
# H1 Title (≤60 chars, includes main keyword)

Hook: 1–2 engaging sentences.

## What Is [Condition]?
Clear definition. Use [[piles]], [[fissure]], or [[fistula]] placeholder naturally.

## Causes
3–5 bullet points.

## Symptoms — When to Worry
Numbered list. One more internal link placeholder.

## Treatment at Bijnor Piles Centre
Mention Kshar Sutra, Kshar Karma, Rubber Band Ligation where relevant. One more placeholder.

## Diet & Lifestyle Tips
2-column Markdown table: Eat ✅ | Avoid ❌

## Frequently Asked Questions
### Q1? Answer.
### Q2? Answer.
### Q3? Answer.

## Conclusion + CTA
End with: Book a free consultation at **Bijnor Piles Centre**, St. Mary\'s ke pass,
Shree Hospital ke samne, Kiratpur Road, Bijnor UP. 📞 +91 70177 90760 | 💬 WhatsApp.

LENGTH: 900–1100 words. Use [[piles]], [[fissure]], [[fistula]] placeholders (2–4 total).

Return ONLY this — no code fences:
---
layout: post
title: "<≤60 char SEO title>"
meta_description: "<≤155 chars with keyword + Bijnor>"
keywords: [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10]
condition: "{condition}"
slug: "<lowercase-hyphen-slug>"
lang: en
date: {date} 09:00:00 +0530
---
[article body]'''

HI_PROMPT = '''हिन्दी में पूरी SEO blog post लिखें: "{topic}"

संरचना (Markdown):
# H1 शीर्षक (≤60 अक्षर, मुख्य keyword शामिल)

Hook: 1–2 आकर्षक वाक्य।

## [स्थिति] क्या है?
[[piles]], [[fissure]], या [[fistula]] placeholder का उपयोग करें।

## कारण — 3–5 bullet points

## लक्षण — एक और placeholder

## बिजनौर पाइल्स सेंटर में उपचार
क्षार सूत्र, क्षार कर्म, रबर बैंड लिगेशन। एक और placeholder।

## खान-पान टिप्स — table: खाएं ✅ | न खाएं ❌

## अक्सर पूछे जाने वाले सवाल
### Q1? जवाब।
### Q2? जवाब।
### Q3? जवाब।

## निष्कर्ष + CTA
अंत में: **बिजनौर पाइल्स सेंटर** में निःशुल्क परामर्श बुक करें।
St. Mary\'s ke pass, Shree Hospital ke samne, Kiratpur Road, Bijnor UP.
📞 +91 70177 90760 | 💬 WhatsApp।

लंबाई: 900–1100 शब्द। [[piles]], [[fissure]], [[fistula]] (2–4 बार)।

ONLY यही return करें — कोई code fence नहीं:
---
layout: post
title: "<≤60 अक्षर SEO शीर्षक>"
meta_description: "<≤155 अक्षर, keyword + Bijnor>"
keywords: [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10]
condition: "{condition}"
slug: "<lowercase-hyphen-slug>"
lang: hi
date: {date} 09:00:00 +0530
---
[article body]'''


def call_anthropic(prompt):
    url  = "https://api.anthropic.com/v1/messages"
    body = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 5000,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("x-api-key", ANTHROPIC_API_KEY)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["content"][0]["text"].strip()


def gh(method, path, data=None):
    url  = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    req  = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {GITHUB_PAT}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    body = json.dumps(data).encode() if data else None
    if body: req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, body) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def push_file(path, content, msg):
    code, info = gh("GET", path)
    sha = info.get("sha") if code == 200 else None
    payload = {"message": msg, "content": base64.b64encode(content.encode()).decode(), "branch": "main"}
    if sha: payload["sha"] = sha
    code, _ = gh("PUT", path, payload)
    return code


def replace_links(body, lang):
    for k, url in INTERNAL[lang].items():
        body = body.replace(f"[[{k}]]", f"[{LABELS[lang][k]}]({url})")
    return body


def extract_slug(body):
    m = re.search(r"^slug:\s*[\"']?([a-zA-Z0-9\-]+)[\"']?", body, re.M)
    return m.group(1).lower() if m else f"post-{TODAY}"


def ping_sitemap():
    sitemap = f"{SITE_URL}/sitemap.xml"
    for name, url in [("Google", f"https://www.google.com/ping?sitemap={sitemap}"),
                      ("Bing",   f"https://www.bing.com/ping?sitemap={sitemap}")]:
        try:
            with urllib.request.urlopen(url) as r:
                print(f"  📡 {name}: {r.status}")
        except Exception as e:
            print(f"  ⚠️  {name} ping failed: {e}")


def main():
    if not ANTHROPIC_API_KEY:
        raise SystemExit("❌ ANTHROPIC_API_KEY not set")
    if not GITHUB_PAT:
        raise SystemExit("❌ GITHUB_PAT not set")

    print(f"\n📅 {TODAY}  |  Day {DAY_IDX+1}/{len(CALENDAR)}")
    print(f"   EN: {TOPIC['english']}")
    print(f"   HI: {TOPIC['hindi']}\n")

    # Generate English
    print("⏳ Generating English post via Claude...")
    en_body = call_anthropic(EN_PROMPT.format(topic=TOPIC["english"], condition=TOPIC["condition"], date=TODAY))
    en_body = re.sub(r"^```[a-z]*\n?", "", en_body, flags=re.M).replace("```","").strip()
    en_body = replace_links(en_body, "en")
    en_slug = extract_slug(en_body)
    en_path = f"_posts/en/{TODAY}-{en_slug}.md"
    code    = push_file(en_path, en_body, f"📝 Auto EN blog: {TOPIC['english'][:50]}")
    print(f"  {'✅' if code in (200,201) else '❌'} English → {en_path} ({code})")

    time.sleep(1)

    # Generate Hindi
    print("⏳ Generating Hindi post via Claude...")
    hi_body = call_anthropic(HI_PROMPT.format(topic=TOPIC["hindi"], condition=TOPIC["condition"], date=TODAY))
    hi_body = re.sub(r"^```[a-z]*\n?", "", hi_body, flags=re.M).replace("```","").strip()
    hi_body = replace_links(hi_body, "hi")
    hi_slug = extract_slug(hi_body)
    hi_path = f"_posts/hi/{TODAY}-{hi_slug}.md"
    code    = push_file(hi_path, hi_body, f"📝 Auto HI blog: {TOPIC['hindi'][:40]}")
    print(f"  {'✅' if code in (200,201) else '❌'} Hindi   → {hi_path} ({code})")

    # Wait for Pages rebuild then ping sitemaps
    print("\n⏳ Waiting 2 min for GitHub Pages to rebuild...")
    time.sleep(120)
    print("📡 Pinging search engine sitemaps...")
    ping_sitemap()

    print(f"\n✅ Done! Live at {SITE_URL}/blog/")


if __name__ == "__main__":
    main()

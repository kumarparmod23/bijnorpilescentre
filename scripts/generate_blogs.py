#!/usr/bin/env python3
"""
Daily SEO blog generator for Bijnor Piles Centre.
Generates 1 English + 1 Hindi post per day using Claude API.
Run via GitHub Actions at 00:30 UTC (06:00 IST).
"""
import os, json, datetime, re, pathlib, sys
import anthropic

REPO      = pathlib.Path(__file__).resolve().parent.parent
CAL       = json.loads((REPO / "_data" / "calendar.json").read_text(encoding="utf-8"))
SITE_URL  = "https://kumarparmod23.github.io/bijnorpilescentre"

START_DATE = datetime.date(2026, 4, 7)
today      = datetime.date.today()
day_idx    = (today - START_DATE).days % len(CAL)
topic      = CAL[day_idx]

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM = """You are Dr. Parmod Kumar, a senior proctologist at Bijnor Piles Centre,
Kiratpur Road, Bijnor, Uttar Pradesh 246701, India (phone +91 70177 90760).
You write warm, authoritative, patient-friendly medical blog posts following
Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) and
YMYL (Your Money or Your Life) guidelines.

Rules:
- Never promise a "guaranteed cure"
- Always advise consulting a qualified doctor
- Use simple language ordinary Indian patients understand
- Mention Bijnor Piles Centre naturally — not as advertising but as the author's clinic
- Include accurate medical information
"""

EN_PROMPT = """Write a complete SEO-optimized blog post in ENGLISH on the topic:
"{topic}"

STRUCTURE (strict — use Markdown headings):
# H1: compelling SEO title (≤60 chars, includes main keyword)

1–2 sentence hook that grabs the reader's attention.

## What Is [Condition]?
Clear definition. Link to related condition using placeholder [[piles]], [[fissure]], or [[fistula]] naturally in a sentence.

## Causes
3–5 bullet points with brief explanation each.

## Symptoms — When to Worry
Numbered list of symptoms. One internal link placeholder [[piles]], [[fissure]], or [[fistula]].

## Treatment Options at Bijnor Piles Centre
Mention Kshar Sutra, Kshar Karma, Rubber Band Ligation where relevant.
Explain each briefly. One more internal link [[piles]], [[fissure]], or [[fistula]].

## Diet & Lifestyle Tips
A 2-column Markdown table: "Eat ✅ / Avoid ❌"

## Frequently Asked Questions
### Question 1?
Answer.
### Question 2?
Answer.
### Question 3?
Answer.

## Conclusion
1–2 sentences summarising and empowering the reader.

CALL TO ACTION (last paragraph, plain text):
Book a free consultation at **Bijnor Piles Centre**, St. Mary's ke pass,
Shree Hospital ke samne, Kiratpur Road, Bijnor, UP.
📞 +91 70177 90760 | 💬 WhatsApp same number.

---
LENGTH: 900–1100 words.
INTERNAL LINKS: use [[piles]], [[fissure]], [[fistula]] — at least 2, max 4 total across the article.

OUTPUT: Return ONLY the following, no code fences, no extra text:

---
layout: post
title: "<SEO title ≤60 chars>"
meta_description: "<≤155 chars — must include main keyword and location Bijnor>"
keywords: [keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, keyword8, keyword9, keyword10]
condition: "{condition}"
slug: "<lowercase-hyphen-slug>"
lang: en
date: {date} 09:00:00 +0530
---

[full markdown article body]
"""

HI_PROMPT = """हिन्दी में एक पूरी SEO-अनुकूलित ब्लॉग पोस्ट लिखें इस विषय पर:
"{topic}"

संरचना (सख्त — Markdown headings का उपयोग करें):
# H1: आकर्षक SEO शीर्षक (≤60 अक्षर, मुख्य कीवर्ड शामिल हो)

1–2 वाक्य का हुक जो पाठक का ध्यान खींचे।

## [स्थिति] क्या होती है?
सरल परिभाषा। [[piles]], [[fissure]], या [[fistula]] में से एक placeholder का उपयोग करें।

## कारण
3–5 बुलेट पॉइंट।

## लक्षण — कब सावधान हों?
नंबरदार सूची। एक internal link placeholder।

## बिजनौर पाइल्स सेंटर में उपचार के विकल्प
क्षार सूत्र, क्षार कर्म, रबर बैंड लिगेशन जहाँ उचित हो। एक और placeholder।

## खान-पान और जीवनशैली टिप्स
2-कॉलम Markdown table: "खाएं ✅ / न खाएं ❌"

## अक्सर पूछे जाने वाले सवाल
### सवाल 1?
जवाब।
### सवाल 2?
जवाब।
### सवाल 3?
जवाब।

## निष्कर्ष
1–2 वाक्य।

CALL TO ACTION (अंतिम पैराग्राफ):
**बिजनौर पाइल्स सेंटर** में निःशुल्क परामर्श बुक करें।
St. Mary's ke pass, Shree Hospital ke samne, Kiratpur Road, Bijnor.
📞 +91 70177 90760 | 💬 WhatsApp इसी नंबर पर।

---
लंबाई: 900–1100 शब्द।
INTERNAL LINKS: [[piles]], [[fissure]], [[fistula]] — कम से कम 2, अधिकतम 4।

आउटपुट: ONLY नीचे दिया गया format, कोई code fence नहीं:

---
layout: post
title: "<SEO शीर्षक ≤60 अक्षर>"
meta_description: "<≤155 अक्षर — मुख्य कीवर्ड + Bijnor अवश्य हो>"
keywords: [keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, keyword8, keyword9, keyword10]
condition: "{condition}"
slug: "<lowercase-hyphen-hindi-slug>"
lang: hi
date: {date} 09:00:00 +0530
---

[पूरा markdown article body]
"""

INTERNAL_LINKS = {
    "en": {
        "piles":   "/bijnorpilescentre/en/what-are-piles/",
        "fissure": "/bijnorpilescentre/en/anal-fissure-explained/",
        "fistula": "/bijnorpilescentre/en/anal-fistula-symptoms/",
    },
    "hi": {
        "piles":   "/bijnorpilescentre/hi/bawasir-kya-hai/",
        "fissure": "/bijnorpilescentre/hi/anal-fissure-ilaj/",
        "fistula": "/bijnorpilescentre/hi/bhagandar-lakshan/",
    },
}

LINK_LABELS = {
    "en": {"piles": "Piles (Hemorrhoids)", "fissure": "Anal Fissure", "fistula": "Anal Fistula"},
    "hi": {"piles": "बवासीर", "fissure": "एनल फिशर", "fistula": "भगन्दर"},
}

def call_claude(prompt_template, topic_text, condition):
    prompt = prompt_template.format(
        topic=topic_text,
        condition=condition,
        date=today.isoformat(),
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=5000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()

def replace_links(body, lang_code):
    for k, url in INTERNAL_LINKS[lang_code].items():
        label = LINK_LABELS[lang_code][k]
        body = body.replace(f"[[{k}]]", f"[{label}]({url})")
    return body

def extract_slug(body):
    m = re.search(r"^slug:\s*[\"']?([a-zA-Z0-9\-]+)[\"']?", body, re.M)
    return m.group(1).lower() if m else f"post-{today}"

def write_post(body, lang_code):
    # Strip any accidental code fences
    body = re.sub(r"^```[a-z]*\n?", "", body, flags=re.M)
    body = body.replace("```", "").strip()
    # Ensure starts with front matter
    if not body.startswith("---"):
        print(f"WARNING: post body doesn't start with front-matter for {lang_code}")
    body  = replace_links(body, lang_code)
    slug  = extract_slug(body)
    out   = REPO / "_posts" / lang_code / f"{today}-{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"✔ Wrote {out.relative_to(REPO)}")
    return out, slug

def get_urls(en_slug, hi_slug):
    return [
        f"{SITE_URL}/en/{en_slug}/",
        f"{SITE_URL}/hi/{hi_slug}/",
    ]

def main():
    print(f"\n📅 {today}  Day {day_idx+1}/{len(CAL)}")
    print(f"   EN: {topic['english']}")
    print(f"   HI: {topic['hindi']}\n")

    print("⏳ Generating English post...")
    en_body = call_claude(EN_PROMPT, topic["english"], topic["condition"])
    _, en_slug = write_post(en_body, "en")

    print("⏳ Generating Hindi post...")
    hi_body = call_claude(HI_PROMPT, topic["hindi"], topic["condition"])
    _, hi_slug = write_post(hi_body, "hi")

    # Save URLs for the submit script
    urls_file = REPO / "scripts" / ".today_urls.json"
    urls_file.write_text(json.dumps(get_urls(en_slug, hi_slug)), encoding="utf-8")
    print(f"\n✅ Both posts written. URLs saved to {urls_file.name}")

if __name__ == "__main__":
    main()

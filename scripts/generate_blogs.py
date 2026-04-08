#!/usr/bin/env python3
"""Generate two SEO-optimized blog posts (English + Hindi) per day for Bijnor Piles Centre."""
import os, json, datetime, re, pathlib, sys
import anthropic

REPO = pathlib.Path(__file__).resolve().parent.parent
CAL  = json.loads((REPO / "_data" / "calendar.json").read_text(encoding="utf-8"))

START_DATE = datetime.date(2026, 4, 7)  # day-0 of rotation
today      = datetime.date.today()
day_idx    = (today - START_DATE).days % len(CAL)
topic      = CAL[day_idx]

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM = """You are Dr. [Your Name], a senior proctologist at Bijnor Piles Centre,
Bijnor, Uttar Pradesh, India. You write warm, simple, patient-friendly medical
blog posts that follow Google's E-E-A-T and YMYL guidelines. Never claim a
'guaranteed cure'. Always recommend consulting a qualified doctor."""

PROMPT = """Write a complete SEO-optimized blog post in **{language}** on the topic:
"{topic}"

REQUIREMENTS
- Length: 850–1000 words.
- Audience: ordinary patients in India. Avoid heavy jargon; explain terms simply.
- Structure (use Markdown):
  # H1 Title
  Short engaging intro paragraph (2–3 sentences).
  ## H2 What is it?
  ## H2 Causes / Symptoms
  ## H2 Treatment Options (mention Kshar Sutra, Kshar Karma, Rubber Band Ligation where relevant)
  ## H2 Diet & Lifestyle Tips
  ## H2 When to See a Doctor
  ## H2 Frequently Asked Questions
     ### Q1, ### Q2, ### Q3 (use H3)
  ## H2 Conclusion
- Insert exactly THREE internal-link placeholders that the build script will replace:
  [[piles]], [[fissure]], [[fistula]]   (use each one at least once)
- End with a clear Call-To-Action paragraph telling the reader to book a
  consultation at **Bijnor Piles Centre, Bijnor, UP** (phone, WhatsApp).

OUTPUT FORMAT — return ONE Markdown file with this YAML front-matter at the very top:
---
layout: post
title: "<SEO title, ≤60 chars>"
meta_description: "<≤155 chars compelling meta description>"
keywords: [<10 comma-separated SEO keywords>]
condition: "{condition}"
slug: "<url-safe slug, lowercase, hyphens>"
lang: "{lang_code}"
date: {date} 09:00:00 +0530
---

Then the full Markdown article body. Do NOT wrap in code fences.
"""

INTERNAL_LINKS = {
    "en": {
        "piles":   "/en/what-are-piles/",
        "fissure": "/en/anal-fissure-explained/",
        "fistula": "/en/anal-fistula-symptoms/",
    },
    "hi": {
        "piles":   "/hi/bawasir-kya-hai/",
        "fissure": "/hi/anal-fissure-ilaj/",
        "fistula": "/hi/bhagandar-lakshan/",
    },
}

def call_claude(language, lang_code, topic_text, condition):
    prompt = PROMPT.format(
        language=language,
        topic=topic_text,
        condition=condition,
        lang_code=lang_code,
        date=today.isoformat(),
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()

def replace_links(body, lang_code):
    for k, v in INTERNAL_LINKS[lang_code].items():
        body = body.replace(f"[[{k}]]", f"[{k}]({v})")
    return body

def slug_from_front_matter(body):
    m = re.search(r"^slug:\s*\"?([a-z0-9\-]+)\"?", body, re.M)
    return m.group(1) if m else f"post-{today}"

def write_post(body, lang_code):
    body  = replace_links(body, lang_code)
    slug  = slug_from_front_matter(body)
    out   = REPO / "_posts" / lang_code / f"{today}-{slug}.md"
    out.write_text(body, encoding="utf-8")
    print(f"✔ Wrote {out.relative_to(REPO)}")
    return out

def main():
    print(f"Day {day_idx+1}/{len(CAL)}  →  {topic['english']}  /  {topic['hindi']}")
    en = call_claude("English", "en", topic["english"], topic["condition"])
    write_post(en, "en")
    hi = call_claude("Hindi",   "hi", topic["hindi"],   topic["condition"])
    write_post(hi, "hi")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Auto-publish daily blog posts from live-news.json — GitHub Actions compatible.

Reads data/live-news.json, groups by topic, creates Hugo posts with
simple gradient cover images (no external dependencies except Pillow).
"""

import json
import os
from datetime import datetime, timezone, timedelta

BDT = timezone(timedelta(hours=6))

# ── Config ──────────────────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data", "live-news.json")
CONTENT_DIR = os.path.join(REPO_ROOT, "content", "posts")
IMAGES_DIR = os.path.join(REPO_ROOT, "static", "images")
TODAY = datetime.now(BDT).strftime("%Y-%m-%d")

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
BN_MONTHS = [
    "", "জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল",
    "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর",
    "অক্টোবর", "নভেম্বর", "ডিসেম্বর",
]

CATEGORY_MAP = {
    "AI/ML": ("ai-ml", "AI / ML", "🤖"),
    "Security": ("security", "সিকিউরিটি", "🔒"),
    "Cloud/DevOps": ("cloud-devops", "ক্লাউড / DevOps", "☁️"),
    "Mobile": ("mobile", "মোবাইল", "📱"),
    "Web/JavaScript": ("web-javascript", "ওয়েব / JS", "🌐"),
    "Hardware": ("hardware", "হার্ডওয়্যার", "💻"),
    "Startups": ("startups", "স্টার্টআপ", "🚀"),
    "Open Source": ("open-source", "ওপেন সোর্স", "🔓"),
    "Regulation": ("regulation", "নিয়মনীতি", "⚖️"),
    "Other": ("other", "অন্যান্য", "📰"),
}


def bn_date():
    d = datetime.now(BDT)
    return f"{str(d.day).translate(BN_DIGITS)} {BN_MONTHS[d.month]} {str(d.year).translate(BN_DIGITS)}"


def generate_simple_cover(category, title_bn, out_path):
    """Generate a simple gradient cover with Pillow — no external fonts needed."""
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1200, 630
    img = Image.new("RGB", (W, H))

    # Gradient colors based on category
    gradients = {
        "AI/ML": ((20, 0, 50), (0, 0, 0)),
        "Security": ((0, 30, 0), (0, 0, 0)),
        "Cloud/DevOps": ((0, 0, 40), (0, 0, 0)),
        "Mobile": ((40, 0, 40), (0, 0, 0)),
        "Web/JavaScript": ((0, 20, 40), (0, 0, 0)),
        "Hardware": ((30, 30, 0), (0, 0, 0)),
        "Startups": ((40, 10, 0), (0, 0, 0)),
        "Open Source": ((0, 30, 30), (0, 0, 0)),
        "Regulation": ((30, 0, 10), (0, 0, 0)),
        "Other": ((20, 20, 20), (0, 0, 0)),
    }
    top, bot = gradients.get(category, ((20, 20, 20), (0, 0, 0)))

    # Draw gradient
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(top[0] + (bot[0] - top[0]) * y / H)
        g = int(top[1] + (bot[1] - top[1]) * y / H)
        b = int(top[2] + (bot[2] - top[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Red accent bar at top
    draw.rectangle([(0, 0), (W, 8)], fill=(184, 0, 0))

    # Category badge
    try:
        font_badge = ImageFont.truetype(os.path.join(REPO_ROOT, "tools", "fonts", "HindSiliguri-SemiBold.ttf"), 28)
        font_title = ImageFont.truetype(os.path.join(REPO_ROOT, "tools", "fonts", "HindSiliguri-Bold.ttf"), 44)
        font_sub = ImageFont.truetype(os.path.join(REPO_ROOT, "tools", "fonts", "HindSiliguri-Regular.ttf"), 30)
    except (OSError, IOError):
        font_badge = ImageFont.load_default()
        font_title = font_badge
        font_sub = font_badge

    # "Tech Intelligence বাংলা" badge
    cat_slug, cat_bn, cat_icon = CATEGORY_MAP.get(category, ("other", "অন্যান্য", "📰"))
    draw.text((40, 30), f"{cat_icon}  Tech Intelligence বাংলা", fill=(184, 0, 0), font=font_badge)

    # Title (truncated if too long)
    max_title_len = 30
    display_title = title_bn[:max_title_len] + "…" if len(title_bn) > max_title_len else title_bn
    draw.text((40, 200), display_title, fill=(255, 255, 255), font=font_title)

    # Date
    draw.text((40, 280), f"📅 {bn_date()}", fill=(180, 180, 180), font=font_sub)

    # Bottom bar
    draw.rectangle([(0, H - 40), (W, H)], fill=(184, 0, 0))
    draw.text((40, H - 32), "salauddinahmad.github.io/tech-blog", fill=(255, 255, 255), font=font_sub)

    img.save(out_path, "PNG")
    print(f"  Cover: {out_path}")


def build_post_content(category_bn, cat_icon, news_items):
    """Build markdown content for a Hugo post from news items."""
    lines = []
    lines.append(f"# {cat_icon} {category_bn} — আজকের টেক নিউজ")
    lines.append("")
    lines.append(f"*{bn_date()} — স্বয়ংক্রিয়ভাবে সংকলিত*")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, item in enumerate(news_items[:10], 1):  # Max 10 items per post
        title = item.get("title", "")
        link = item.get("link", "")
        source = item.get("source", "")
        summary = item.get("summary_en", "") or item.get("description", "")[:120]

        lines.append(f"## {i}. {title}")
        lines.append("")
        lines.append(f"**সোর্স:** [{source}]({link})")
        lines.append("")
        lines.append(f"{summary}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(f"*📅 {bn_date()} • Tech Intelligence বাংলা • স্বয়ংক্রিয় রিপোর্ট*")
    return "\n".join(lines)


def main():
    # Load live news data
    if not os.path.exists(DATA_PATH):
        print("No live-news.json found. Nothing to publish.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    news_items = data.get("news", [])
    if not news_items:
        print("No news items. Nothing to publish.")
        return

    today_bdt = bn_date()
    print(f"📝 Auto-publishing for {today_bdt}...")

    # Group by topic
    topics = {}
    for item in news_items:
        topic = item.get("topic", "Other")
        if topic not in topics:
            topics[topic] = []
        topics[topic].append(item)

    any_created = False

    # Create a post for each topic with items
    for topic, items in topics.items():
        if not items:
            continue

        cat_slug, cat_bn, cat_icon = CATEGORY_MAP.get(topic, ("other", "অন্যান্য", "📰"))

        # Check if post already exists
        post_dir = os.path.join(CONTENT_DIR, cat_slug, f"daily-{cat_slug}-{TODAY}")
        if os.path.exists(post_dir):
            print(f"  ⏭️ Skipping {cat_slug} (already exists)")
            continue

        # Generate cover
        os.makedirs(post_dir, exist_ok=True)
        cover_png = os.path.join(IMAGES_DIR, f"cover-{cat_slug}-{TODAY}.png")
        generate_simple_cover(topic, cat_bn, cover_png)

        # Build post content
        content = build_post_content(cat_bn, cat_icon, items)

        # Write front matter + content
        index_path = os.path.join(post_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{cat_bn} — {today_bdt}"
date: {TODAY}T10:00:00+06:00
draft: false
slug: "daily-{cat_slug}-{TODAY}"
categories: ["{cat_slug}"]
tags: ["ai", "technology", "bangla", "daily-report", "seo"]
description: "{cat_bn} — প্রতিদিনের অটো-জেনারেটেড রিপোর্ট।"
summary: "{cat_bn} — {today_bdt} — স্বয়ংক্রিয় টেক নিউজ রিপোর্ট।"
cover:
  image: "/images/cover-{cat_slug}-{TODAY}.png"
  alt: "{cat_bn} — {today_bdt}"
---

{content}
""")
        print(f"  ✅ {cat_slug}: /posts/{cat_slug}/daily-{cat_slug}-{TODAY}/")
        any_created = True

    if not any_created:
        print("  ⏭️ All posts already exist for today.")

    # Also create a combined "Tech Intelligence" daily digest
    digest_dir = os.path.join(CONTENT_DIR, "tech-intelligence", f"daily-tech-intelligence-{TODAY}")
    if not os.path.exists(digest_dir):
        os.makedirs(digest_dir, exist_ok=True)
        cover_png = os.path.join(IMAGES_DIR, f"cover-tech-intelligence-{TODAY}.png")
        generate_simple_cover("AI/ML", f"টেক ইন্টেলিজেন্স — {today_bdt}", cover_png)

        # Build digest from top items across all topics
        top_items = sorted(news_items, key=lambda x: x.get("importance", 0), reverse=True)[:15]
        content = build_post_content("টেক ইন্টেলিজেন্স", "🤖", top_items)

        with open(os.path.join(digest_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(f"""---
title: "টেক ইন্টেলিজেন্স — {today_bdt}"
date: {TODAY}T10:00:00+06:00
draft: false
slug: "daily-tech-intelligence-{TODAY}"
categories: ["tech-intelligence"]
tags: ["ai", "technology", "bangla", "daily-report", "seo", "digest"]
description: "প্রতিদিনের টেক ইন্টেলিজেন্স ডাইজেস্ট — {today_bdt}"
summary: "টেক ইন্টেলিজেন্স — {today_bdt} — স্বয়ংক্রিয় টেক নিউজ ডাইজেস্ট।"
cover:
  image: "/images/cover-tech-intelligence-{TODAY}.png"
  alt: "টেক ইন্টেলিজেন্স — {today_bdt}"
---

{content}
""")
        print(f"  ✅ digest: /posts/tech-intelligence/daily-tech-intelligence-{TODAY}/")

    print("📊 Auto-publish complete!")


if __name__ == "__main__":
    main()

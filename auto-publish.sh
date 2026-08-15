#!/bin/bash
# ═══════════════════════════════════════════════════
# 🇧🇩 Tech Intelligence বাংলা — Auto-Publish (single-language)
# রিপোর্ট (বাংলা) → কভার + পোস্ট → GitHub
# ═══════════════════════════════════════════════════
set -e

BLOG_DIR="/Users/salaudinahmad/Documents/A/Agent_Work/Agent_Autometion/tech-blog"
TOOLS_DIR="$BLOG_DIR/tools"
TODAY=$(date +%Y-%m-%d)
DRY_RUN=false
[ "$1" = "--dry-run" ] && DRY_RUN=true && shift
REPORT_FILE="${1:-$BLOG_DIR/latest-report.md}"

TODAY_BN=$(python3 -c "
import datetime
en_bn = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')
months = ['', 'জানুয়ারি','ফেব্রুয়ারি','মার্চ','এপ্রিল','মে','জুন','জুলাই','আগস্ট','সেপ্টেম্বর','অক্টোবর','নভেম্বর','ডিসেম্বর']
d = datetime.date.today()
print(f'{str(d.day).translate(en_bn)} {months[d.month]} {str(d.year).translate(en_bn)}')
")

echo "📝 BN Auto-publishing for $TODAY_BN..."

extract_bn() { sed -n "/$2/,/^## /p" "$1" | sed '$d' | sed '/^---$/d'; }

create_post() {
    local CATEGORY="$1" TITLE="$2" CONTENT="$3" SLUG="$4"
    /Users/salaudinahmad/.venvs/pillow-raqm/bin/python "$TOOLS_DIR/generate-cover.py" --title "$TITLE" --category "$CATEGORY" --lang bn \
        --date "$TODAY_BN" --out "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.png" --bg-cache "$BLOG_DIR/static/images/ai-bg" || true
    # ── Image pipeline: PNG (1200×630) → WebP (q80) + responsive srcset variants (+AVIF q40) ──
    # Measured: cwebp q80 ≈ 91% saving, avifenc q40 ≈ 97% (audit subagent_04-F2).
    # Sizes must stay in sync with layouts/_partials/cover.html (1200×630 / 768w / 480w).
    if command -v cwebp >/dev/null 2>&1; then
        cwebp -q 80 "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.png" -o "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.webp" 2>/dev/null || true
        cwebp -q 80 -resize 768 403 "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.png" -o "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}-768w.webp" 2>/dev/null || true
        cwebp -q 80 -resize 480 252 "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.png" -o "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}-480w.webp" 2>/dev/null || true
    else
        echo "⚠️  cwebp not found — WebP variants skipped (brew install webp)"
    fi
    if command -v avifenc >/dev/null 2>&1; then
        avifenc -q 40 -s 4 "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.png" -o "$BLOG_DIR/static/images/cover-${CATEGORY}-${TODAY}.avif" 2>/dev/null || true
    fi
    mkdir -p "$BLOG_DIR/content/posts/${CATEGORY}/${SLUG}"
    cat > "$BLOG_DIR/content/posts/${CATEGORY}/${SLUG}/index.md" << MDEOF
---
title: "${TITLE}"
date: ${TODAY}T10:00:00+06:00
draft: false
slug: "${SLUG}"
categories: ["${CATEGORY}"]
tags: ["ai", "technology", "bangla", "daily-report", "seo"]
description: "${TITLE}"
summary: "${TITLE} — প্রতিদিনের অটো-জেনারেটেড রিপোর্ট, কভার ইমেজ সহ।"
cover:
  image: "/images/cover-${CATEGORY}-${TODAY}.png"
  alt: "${TITLE}"
---

${CONTENT}

---
*📅 ${TODAY_BN} • Tech Intelligence বাংলা*
MDEOF
    echo "✅ BN ${CATEGORY}: /${SLUG}/"
}

found=false
if [ -f "$REPORT_FILE" ]; then
    C=$(extract_bn "$REPORT_FILE" '## 🤖.*Tech Intelligence')
    if [ -n "$C" ]; then
        create_post "tech-intelligence" "টেক ইন্টেলিজেন্স — ${TODAY_BN}" "$C" "daily-tech-intelligence-${TODAY}"
        found=true
    fi
    C=$(extract_bn "$REPORT_FILE" '## 🧠.*Adaptability')
    if [ -n "$C" ]; then
        create_post "adaptability" "অ্যাডাপ্টাবিলিটি ইন্টেলিজেন্স — ${TODAY_BN}" "$C" "daily-adaptability-intelligence-${TODAY}"
        found=true
    fi
    C=$(extract_bn "$REPORT_FILE" '🕌.*নামাজ')
    if [ -n "$C" ]; then
        create_post "prayer-times" "আজকের নামাজের সময় — ${TODAY_BN}" "$C" "prayer-times-${TODAY}"
        found=true
    fi
fi

[ "$found" = "false" ] && echo "⚠️  কোনো রিপোর্ট পাওয়া যায়নি" && exit 1
echo "📊 BN posts generated!"

if [ "$DRY_RUN" = "true" ]; then echo "🔍 Dry-run — push skipped."; exit 0; fi

cd "$BLOG_DIR"
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "⚠️  Not a git repo. Instructions in README."
    exit 1
fi
git add content/ static/images/
if git diff --cached --quiet; then
    echo "No changes."
else
    git commit -m "📝 BN Auto-post: ${TODAY}"
    git push origin main && echo "🚀 BN Pushed — deploy running!"
fi

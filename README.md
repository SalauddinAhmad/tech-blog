# 🇧🇩 Tech Intelligence বাংলা — ব্লগ সাইট (পুরো সাইট বাংলায়)

**প্রতিদিনের রিপোর্ট → বাংলা কভার ইমেজ → বাংলা ব্লগ পোস্ট → GitHub Pages অটো-ডিপ্লয়**

🎨 মডার্ন ক্রিয়েটিভ প্রফেশনাল ডিজাইন (PaperMod + কাস্টম CSS) • মোবাইল-ফার্স্ট • SEO-ready

---

## 🌐 ২টি আলাদা ব্লগ সাইট

| সাইট | ভাষা | Repo | URL |
|---|---|---|---|
| **Tech Intelligence বাংলা** | 🇧🇩 বাংলা (সবকিছু বাংলায়) | `tech-blog` | https://salauddinahmad.github.io/tech-blog/ |
| **Tech Intelligence English** | 🇬🇧 English (সবকিছু English-এ) | `tech-blog-en` | https://salauddinahmad.github.io/tech-blog-en/ |

একই সাইটে ২ ভাষা মেশানো নয় — **২টি সম্পূর্ণ আলাদা সাইট**, নিজস্ব ডিজাইন ও কনটেন্ট।

---

## 📁 এই সাইটের স্ট্রাকচার (বাংলা)

```
tech-blog/
├── config.toml                  # বাংলা সাইট কনফিগ + SEO
├── auto-publish.sh              # রিপোর্ট → কভার + পোস্ট → git push
├── tools/generate-cover.py      # বাংলা কভার জেনারেটর (--lang bn)
├── assets/css/extended/custom.css  # 🎨 ক্রিয়েটিভ ডিজাইন (গ্র্যাডিয়েন্ট, কার্ড)
├── .github/workflows/deploy.yml # GitHub Actions
├── content/posts/<category>/<slug>/index.md
├── static/images/               # বাংলা কভার ইমেজ
└── latest-report.md             # বাংলা রিপোর্ট (ইনপুট)
```

---

## ⚡ সেটআপ — ৩ স্টেপ

1. **GitHub-এ ২টা repo বানান:** `tech-blog` + `tech-blog-en` (দুটো Public)
   - প্রতিটির Settings → Pages → Source: **GitHub Actions**
   - Settings → Actions → Workflow permissions: **Read and write**
2. **পুশ করুন:**
   ```bash
   cd /Users/salaudinahmad/Documents/A/Agent_Work/Agent_Autometion/tech-blog
   git init && git add . && git commit -m "🚀 BN blog" && git branch -M main
   git remote add origin https://github.com/SalauddinAhmad/tech-blog.git && git push -u origin main

   cd ../tech-blog-en
   git init && git add . && git commit -m "🚀 EN blog" && git branch -M main
   git remote add origin https://github.com/SalauddinAhmad/tech-blog-en.git && git push -u origin main
   ```
3. **টেস্ট:**
   ```bash
   ./auto-publish.sh --dry-run    # বাংলা সাইট
   ```

এরপর প্রতিদিন ১০:১৫-এ cron নিজে ২টা সাইটেই পোস্ট করবে। 🎉

---

## 🔍 SEO (অটো গুগল)

- SEO-friendly slug URL: `/posts/daily-tech-intelligence-2026-08-12/`
- sitemap.xml (daily) + robots.txt — অটো
- canonical + Open Graph + JSON-LD
- Meta description প্রতি পোস্টে ইউনিক
- মোবাইল-ফার্স্ট — গুগল ranking-এ বোনাস

---

*Powered by Flux 🧞*

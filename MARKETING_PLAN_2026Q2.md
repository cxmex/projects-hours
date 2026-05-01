# Terex / Fundastock — Q2 2026 Growth Plan

**Status:** Living document. Last updated 2026-05-01.
**Owner:** Horacio (founder) + AI assistant + team.

This is the full-stack growth plan derived from the analytics work on 2026-05-01: 8,943 units sold over 30 days, ~298/day, $500K MXN/month margin from top 15 SKUs, 0% conversion on FB ad spend, 142 of 190 active styles invisible online (no photos).

The strategy is to **double down on what works** (ORANGE iPhone 17 Pro Max aesthetic), **fix the funnel** (landing page + WhatsApp sales agent), and **build a content engine** that runs on AI so it scales without proportional headcount.

---

## Section 1 — Brand refresh

### Why rename

`Terex` is a US heavy-machinery brand (cranes, dump trucks). Hard to own in search. `Fundastock` is descriptive but not aspirational. Neither is chant-able on TikTok. We need a brand that:

- Works as a hashtag (#X)
- Sounds Mexican-Gen-Z, not corporate
- Owns the "match your case to your phone" insight
- Available as `.com`, `.mx`, IG handle, TikTok handle (verify before commit)

### Top 5 candidates (ranked)

| Brand | Pitch | Pros | Cons |
|---|---|---|---|
| **MATCH** | "Match your case to your vibe" — leans into the color-coordination behavior we see in sales | Short, English-Spanish dual, hashtag-friendly | May conflict with Match.com SEO |
| **HUE** | One-syllable, color-first, premium feel | Owns the color positioning, easy logo | Generic, hard to trademark |
| **CASEY** | Friendly, female-leaning (matches buyer demo for ORANGE family) | Memorable, can be a "personality" | Common name |
| **NARANJA** | Hero color becomes the brand. Counterintuitive but distinctive. | Owns the breakout color, super Mexican | Limits expansion to other colors over time |
| **CARÁTULA** | Spanish for "cover", sounds elegant | Mexican-rooted, premium | Long, harder to chant |

**Recommendation: MATCH.** Logo treatment: lowercase `match.` with a period. Color palette: orange-led with a white/black system. Tagline: *"tu caso, tu color."*

Test domain availability: `match.mx`, `matchcases.mx`, `matchstore.mx`, IG `@match.mx`, TT `@match.mx`.

### Sub-brands

Keep `MATCH` as the consumer brand. Keep `Fundastock` as the legal/wholesale entity (B2B). Two stores: `match Eje Central` and `match Centro` (cleaner than Terex1/Terex2).

---

## Section 2 — TikTok campaign with AI influencer

### The character: "Naia"

A virtual Mexican Gen Z influencer who lives in CDMX, obsesses over phone aesthetics, and tries on a different case every day. She is:

- 22 years old, mestiza, Roma Norte aesthetic
- Has a NARANJA iPhone 17 Pro Max (matches our hero customer)
- Speaks neutral Mexican Spanish with light slang
- Personality: confident, color-obsessed, slightly sarcastic, body-positive
- Visual style: oversized blazers, gold jewelry, café con leche aesthetic

### Production stack (all AI)

| Layer | Tool | Cost/month |
|---|---|---|
| Character base image | Midjourney v7 | $30 |
| Face animation / lip-sync | **Hedra** or HeyGen | $30-100 |
| Voice | **ElevenLabs** (clone a Mexican voice actress for $5 once) | $22 |
| Script writing | Claude Sonnet 4.6 via API | $20 |
| Product B-roll | Sora-2 / Veo-3 | $50 |
| Music / trending audio | TikTok native library (free) | $0 |
| Editing | CapCut + auto-captions | $0 |
| **Total monthly stack** | | **~$150 USD** |

### Content cadence: 5 posts/week

| Day | Format | Topic |
|---|---|---|
| Mon | "Case of the day" | Naia unboxes + tries one ORANGE family case on her iPhone 17 PM |
| Tue | "Color match challenge" | Holds up 3 cases, viewers vote in comments which matches her outfit |
| Wed | UGC reaction stitch | Naia reacts to a real customer's WhatsApp photo |
| Thu | "Drop alert" | Announces new colors arriving Friday at the store |
| Fri | Behind-the-scenes | Naia "visits" the Eje Central store (B-roll of physical store + Naia composited) |

Each post ends with the same CTA: **"link en bio para WhatsApp"** → routes to landing page with `utm_source=tiktok&utm_campaign=naia&utm_content=YYYY-MM-DD`.

### Why this works

- **One character, infinite content** — no fee per influencer, no scheduling drama
- **Consistent face = brand recall** — the algorithm starts pushing Naia to lookalike viewers
- **Multilingual variants for free** — same script in English/Portuguese to expand later
- **TikTok loves recurring characters** — "story arcs" between videos drive completion rate
- **AI = no body-image, age, or contract risk** vs human influencers

### Risk mitigation

- Disclose Naia is AI in bio: "asistente virtual de match." (FTC + Mexican Profeco-friendly)
- Don't use her to make medical/safety claims
- Test 4 weeks before scaling — if engagement < 5% likes-to-views ratio, iterate the character

### Budget

- $150/mo production stack
- $300/mo TikTok ads boosting top-performing organic posts (@$10/day)
- **Total $450/mo** to start. Doubles if any single post hits 100K views.

---

## Section 3 — Facebook ad creative spec

### What we know from data

- ORANGE iPhone 17 Pro Max + ORANGE-themed cases = the entire business
- Generic FB CTA "Hola, me interesa" converts 0% (all 38 leads ghosted)
- "Orange Convert" is the single most-asked color/style combo
- 13% of FB leads are wrong-audience ("no me interesa") — targeting is too broad

### Creative system (use across all variants)

**Visual rules:**
- Always feature an iPhone 17 Pro Max in NARANJA color (the hero phone)
- Case shown ON the phone, not standalone
- Solid orange background OR Roma Norte café aesthetic
- Bold sans-serif overlay text (Inter Black or Sharp Grotesk)
- Always show price: "$90 MXN — entrega hoy"
- Bottom-right corner: WhatsApp button with arrow

**Audio rules (for video):**
- 3-second hook (Naia POV: "espera, mira esto")
- Trending Mexican TikTok audio (refreshed weekly)
- Captions burned in (80% watch on mute)

### 5 ad sets to launch

| # | Name | Audience | Creative | Daily $ |
|---|---|---|---|---|
| 1 | **Hero — Orange Match** | Lookalike of past iPhone 17 buyers (1%), 18-35, CDMX 30km | Carousel: 5 ORANGE family cases on iPhone 17 PM | $20 |
| 2 | **Color Match Challenge** | Interest: phone accessories, 18-25, CDMX | 15-sec video: Naia matches 3 cases to outfits | $15 |
| 3 | **iPhone 17 Air Launch** | Recent iPhone 17 Air search, 25-45 | Single image: "Funda iPhone 17 Air desde $80" | $10 |
| 4 | **Samsung S26 Ultra side-bet** | Samsung lookalike, 25-45 | Carousel of HUMO BRACKET SAM colors | $10 |
| 5 | **Retargeting** | Site visitors last 7d who didn't WhatsApp | "¿Te quedaste pensando? Tu funda sigue aquí" | $10 |
| | **Total daily** | | | **$65** |

Monthly: ~$2,000 USD. Realistic to test for 2-3 months.

### Required negatives (exclusions)

- Phone numbers that already messaged "no me interesa" (we have 5 from the lead audit)
- 18-65+ demos who don't own a smartphone (Meta auto-handles)
- Geographic exclusion: outside Mexico

### Landing page targeting per ad

Every ad URL: `landing.terex.mx/?utm_source=fb&utm_medium=cpc&utm_campaign=<set_name>&utm_content=<creative_id>&v=<A|B|C>`

Force `v=A` on hero, `v=B` on color match, `v=C` on Samsung — clean variant attribution.

---

## Section 4 — Continuous audience communication (the AI-powered always-on)

The store has 58 active WhatsApp contacts and 24 linked QR-loyalty customers. That's a tiny opted-in audience — but it grows daily. The plan: nurture them with AI-personalized touches at zero marginal cost.

### Channel mix

| Channel | Cadence | Tool | Personalization level |
|---|---|---|---|
| WhatsApp broadcast | 1 / week | Meta WhatsApp API (24h template messages) | Segment by past purchase: ORANGE buyers get ORANGE drops, Samsung buyers get Samsung drops |
| Instagram DM auto-reply | On-demand | Meta tools + Claude API | Bot replies to story reactions with a product rec |
| TikTok comments | Daily | Manual (1-2hrs/day) escalating to AI replies via TikTok API once available | Naia voice |
| Email | 2x/month | Resend + AI-personalized drafts | First name + last 3 viewed products |
| Google Maps Q&A | Weekly | Manual answers | N/A |

### Weekly broadcast framework

Every Friday at 11am MX (the shopping window), a WhatsApp broadcast goes out:

> 🟠 **MATCH DROP — Viernes**
>
> Llegaron 3 nuevos colores en ORANGE BELLA ESQUINAS para iPhone 17 PM:
> - VERDE PISTACHE 🌱
> - LILA 💜
> - ROSA PALO 🌸
>
> Solo en tienda Eje Central o por WhatsApp.
> Pedidos antes de las 6pm = entrega hoy.
>
> Responde "STOP" para dejar de recibir.

The CTA + link includes UTMs so we measure conversion per drop.

### Always-on sales agent (Layer 2)

The WhatsApp sales agent (built but not previously firing — patched 2026-05-01) now handles:
1. FB CTA leads (`Hola, me interesa! Tienen disponible`)
2. Landing page leads (`vi su catalogo`)
3. Voice notes (transcribed via Whisper if `OPENAI_API_KEY` set)

Every conversation is logged to `whatsapp_conversations` and `sales_conversation_turns`. The dashboard at `/admin/funnel` (landing page) + the existing `sales_agent` admin endpoints will show the full funnel.

### AI-driven content for the always-on

Every Sunday night, run a Claude prompt against the past 7 days of data:

```
Given:
- Top 5 selling estilos last week
- Top 5 viewed-but-not-bought estilos
- Top 5 search queries with no result
- Most common WhatsApp objections (price, color unavailable, etc.)

Generate:
- 5 TikTok hook ideas for Naia
- 3 Instagram caption drafts
- 1 WhatsApp broadcast template
- 1 internal note: what to restock or photograph
```

This becomes a recurring Monday-morning agent that drops a Notion/Slack message with the week's content + ops to-dos.

---

## Section 5 — The execution sprint (next 14 days)

### Week 1 (May 2 – May 8)

| Day | Task | Owner | Hours |
|---|---|---|---|
| Mon | Photo shoot: top 25 estilos × missing colors (155 photos) | Store team | 5 |
| Mon | Upload photos via inventoriorapido1 admin | Horacio | 2 |
| Tue | Verify domain availability for MATCH brand candidates | Horacio | 1 |
| Tue | Create Naia base character in Midjourney (10 variants) | AI assistant | 2 |
| Wed | Set up Hedra + ElevenLabs accounts, clone voice | Horacio | 2 |
| Wed | Write 10 TikTok scripts (2 weeks of content) | Claude API | 1 |
| Thu | Launch FB ad set #1 (Hero) with $20/day budget | Horacio | 1 |
| Thu | Verify landing page deploy at landing.terex.mx, fix DNS | Horacio | 1 |
| Fri | Post Naia's first 2 TikToks (Mon + Tue's content) | AI assistant | 1 |
| Fri | First WhatsApp broadcast: "Welcome to MATCH" (rebrand) | Horacio | 1 |
| Sat | Train cashiers on QR loyalty + new brand language | Horacio | 2 |
| Sun | Review week 1: ad spend, landing events, WA conversations | Horacio | 1 |

### Week 2 (May 9 – May 15)

| Day | Task | Owner | Hours |
|---|---|---|---|
| Mon | Audit funnel data — kill losing FB ad sets, double winners | Horacio | 1 |
| Tue | Photo shoot: next 25 estilos | Store team | 4 |
| Wed | Launch TikTok ads boosting top 2 organic posts | Horacio | 1 |
| Thu | Set up Sunday-night AI content brief recurring job | Horacio | 2 |
| Fri | Second WhatsApp broadcast | AI-drafted, Horacio sends | 0.5 |
| Sat | Kill zombie inventory: launch "Caja Sorpresa $99" promo | Store team | 2 |
| Sun | Compile first 2-week metrics report | Horacio | 1 |

### Success metrics (4-week target)

| Metric | Today | Week 4 target |
|---|---|---|
| Daily units sold | 298 | 350 (+17%) |
| FB ad → sale conversion | 0% | 3-5% |
| Landing page sessions | 0 | 1,000+/week |
| WhatsApp conversations (sales_agent) | 0 | 50+ |
| TikTok followers (@match.mx) | 0 | 1,000 |
| Photo coverage (active estilos) | 7% | 60% |
| QR loyalty redemption rate | 4.6% | 15% |

---

## Section 6 — What changes on the existing repos

### `inventoriorapido1`
- Nothing breaking. Already serves photos via existing endpoints.
- Add: nightly job to recompute `inventario_estilos.sold30` from `ventas_terex1+terex2` (currently stale — many top sellers show 0).

### `fundastock-whatsapp`
- ✅ Patched 2026-05-01: FB CTA + landing CTA force-routing to sales agent
- ✅ Patched 2026-05-01: audio handler with Whisper fallback
- TODO: add WhatsApp broadcast endpoint for weekly drop announcements

### `Landing-page`
- TODO: deploy to `landing.terex.mx` (verify Railway domain config)
- TODO: connect `?utm_*` params to `landing_events.extra` JSON
- TODO: rebrand from "TEREX" to "MATCH" in templates (3 files: variant_a/b/c.html, base.html)
- TODO: add Naia headshot to hero variant B
- TODO: add /api/whatsapp-handoff that pre-fills the WA message with the user's last-viewed product

### `projects-hours`
- TODO: seed ph_projects with the campaigns above
- TODO: seed ph_tasks with the day-by-day execution items
- TODO: add team members to ph_team_members

---

## Why this plan, in one sentence

> **You're an ORANGE-iPhone-17-Pro-Max-aesthetic shop with a phone case business attached. Lean fully into that visual identity, brand it as MATCH, run an AI virtual influencer named Naia who lives that aesthetic on TikTok, route everyone to a landing page with proper attribution, and let the WhatsApp sales agent close the loop — measured every Sunday night by a recurring AI brief.**

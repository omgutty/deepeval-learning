# LinkedIn Image Kit — DeepEval Framework

The post needs **two images**. Publish them as a carousel (document post) for
maximum reach, or use image 1 as the cover and image 2 as the diagram.

| Image | What it is | Ratio |
|---|---|---|
| **1. Cover** | The hero shot. "I built a dashboard that grades my own chatbot." | 1200 × 1200 |
| **2. Workflow** | The architecture + build/test story, with the dashboard and repo URL | 1200 × 1500 |

> **Read this first.** Every AI image generator is bad at text. Anything with
> more than ~4 words will come out garbled — "DeepEval" becomes "DeepEvaI",
> "120B" becomes "12OB". So: **generate the background with AI, add all text by
> hand** in Canva, Figma or Excalidraw. Section 4 gives you the exact content
> to place. Section 3 is the prompt if you insist on an all-in-one.

---

## 1) Cover image prompt

**Midjourney / Ideogram / Firefly:**

```
A premium tech-editorial 3D illustration on a deep matte-black background.
On the left, a glowing electric-blue robot head emitting a thin stream of
light particles toward the right. On the right, a larger glowing warm-amber
judge figure — abstract, geometric, no face — catching those particles and
stamping them with a soft green check mark. Between them floats a translucent
glass panel showing a thin score bar at 100% and a single green check.
Volumetric light, subtle depth of field, soft rim lighting, isometric
perspective, cinematic, high detail, generous negative space in the top third
for a headline. Dark navy and cyan palette with a single amber accent.
No text. No letters. No numbers. No people. No logos.
Style: premium SaaS keynote slide, minimal, aspirational.
--ar 1:1 --style raw --v 6
```

**Negative prompt:**

```
text, words, letters, numbers, watermark, signature, people, faces, hands,
clutter, busy background, low contrast, blurry, distorted geometry, extra limbs,
stock-photo look, lens flare
```

**Flat/vector variant (DALL·E / ChatGPT / Canva AI):**

```
A modern flat vector illustration. Near-black background. Two abstract
geometric AI shapes connected by a glowing dotted line: a cyan rounded square
on the left, a larger amber hexagon on the right. The right shape holds a
green checkmark. A thin green progress bar runs between them at full width.
Geometric, minimal, crisp edges, subtle glow, no gradients, large empty space
in the top third for a title. No text, no letters, no numbers, no people.
Editorial tech-poster style.
```

---

## 2) The workflow image — what it must communicate

This is the image people will actually study. It has to answer four questions
at a glance:

1. **What are the pieces?** — chatbot, RAG, judge, dashboard
2. **How does data flow?** — question in, answer out, judge scores it
3. **How was it built?** — the stack and the ports
4. **How was it tested?** — 106 tests, 12 metrics, and *what went wrong*

### The layout (4 stacked bands, top to bottom)

```
┌───────────────────────────────────────────────────────────────┐
│  BAND 1 — TITLE                                               │
│  I built a dashboard that grades my own chatbot               │
│  DeepEval · 12 metrics · 106 tests                            │
├───────────────────────────────────────────────────────────────┤
│  BAND 2 — ARCHITECTURE                                        │
│                                                               │
│  ┌──────────────┐        ┌────────────────┐                  │
│  │ App under    │        │  THE JUDGE     │                  │
│  │ test         │        │ gpt-oss-120b   │                  │
│  │              │        │  ≥ threshold?  │                  │
│  │ A Chatbot    │──Q──┐  │  + WHY         │                  │
│  │  :8201       │     │  └────────────────┘                  │
│  │  qwen-3.8    │     ├──► score                     │        │
│  │              │     │    pass / fail                          │
│  │ B RAG        │──Q──┘    reason                            │
│  │  :8202       │                                             │
│  └──────────────┘                                             │
├───────────────────────────────────────────────────────────────┤
│  BAND 3 — THE DASHBOARD (screenshot, real UI)                 │
│  [ paste your dashboard screenshot here ]                     │
├───────────────────────────────────────────────────────────────┤
│  BAND 4 — THE HONEST PART                                     │
│  ✗ Was testing nothing — mock mode                            │
│  ✗ Scored the wrong dataset — PII read 0.00                   │
│  ✗ Same test, three answers — 1.00 / 0.33 / 0.50              │
│  github.com/omgutty/deepeval-learning                         │
└───────────────────────────────────────────────────────────────┘
```

---

## 3) All-in-one AI prompt (background only, add text after)

Use this to generate the *diagram skeleton*, then place your own text on top.

```
A clean technical architecture diagram on a near-black background, flat
editorial infographic style, thin 1px connecting lines with small circular
nodes. Four horizontal bands separated by faint horizontal rules.

Top band: empty, reserved for a large headline.
Second band: two outlined rounded rectangles on the left stacked vertically,
and one larger rounded rectangle on the right. Glowing dotted arrows flow from
each left box to the right box, and a single arrow returns from the right box.
Third band: one wide empty rounded rectangle, reserved for a screenshot.
Bottom band: three small rows of thin horizontal lines, reserved for text.

Colour palette: background #0A0F1C, outlines #2A3348, cyan #22D3EE for the
left boxes, amber #F59E0B for the right box, green #22C55E for the return arrow.
Generous whitespace, no text, no letters, no numbers, no people, no logos.
Minimal, precise, premium developer-documentation aesthetic.
--ar 4:5
```

---

## 4) Build it by hand (recommended — exact content)

Generate a background in section 3, then lay this text on top. This is the
version that will actually look good.

### Band 1 — Title

> **I built a dashboard that grades my own chatbot**
> `DeepEval` · `12 metrics` · `106 tests` · `2 real apps`

### Band 2 — Architecture

| Box | Label | Sub-label |
|---|---|---|
| Left, top | **A · Chatbot** | `:8201` · `qwen-3.8-27b` |
| Left, bottom | **B · RAG Explorer** | `:8202` · `21 chunks` |
| Right | **THE JUDGE** | `gpt-oss-120b` · different model family |
| Return arrow | **score + pass/fail + reason** | |

Footnote under the diagram:

> The framework never imports the apps. It calls `POST /chat` over HTTP —
> so it scores deployed behaviour, not a unit-tested function.

### Band 3 — Dashboard

Paste a real screenshot of <http://localhost:8203>. Crop to the grid so the
cards are legible. Label it:

> **C · Dashboard** — `:8203` · press Run, watch the judge work

### Band 4 — The honest part

> **What broke before it worked**
> ✗ Was testing nothing — the app ran in **mock mode**
> ✗ Scored the wrong dataset — PII Leakage read **0.00**
> ✗ Same test, three answers — **1.00 / 0.33 / 0.50**
>
> **One run is never proof.**

### Repo strip (bottom, full width)

> 🔗 **github.com/omgutty/deepeval-learning**

Style it as a monospace pill on a slightly lighter strip so it reads as a link.

---

## 5) Design tokens

| Token | Value | Use |
|---|---|---|
| Background | `#0A0F1C` | canvas |
| Panel | `#111827` | cards and boxes |
| Outline | `#2A3348` | 1px borders |
| Text primary | `#F8FAFC` | headlines |
| Text muted | `#94A3B8` | sub-labels |
| **Cyan** `#22D3EE` | app under test | boxes A and B |
| **Amber** `#F59E0B` | the judge | box C |
| **Green** `#22C55E` | pass | score arrows |
| Red | `#EF4444` | the failure rows |
| Headline font | Inter / Satoshi Bold | tight tracking, -2% |
| Mono font | JetBrains Mono | ports, model names, URLs |
| Corner radius | 16 px | cards |
| Grid | 8 px base | spacing |

**The one rule:** one accent per actor. Cyan = the thing being tested. Amber =
the judge. Never let a third colour compete.

---

## 6) Cover headline options (pick one)

- **One AI grades another.**
- **My chatbot passed 6 tests. It was mocking me.**
- **Green checkmarks are not evidence.**
- **Vibes → Numbers.**
- **I tested nothing for two hours.**

**Subline:** `12 metrics · 106 tests · 1 dashboard`

---

## 7) Final checklist

- [ ] Generated 4 background variants, picked the cleanest
- [ ] All text added by hand (never trust AI text)
- [ ] Dashboard screenshot is the **real** UI, cards legible
- [ ] GitHub URL present and spelled correctly
- [ ] Checked at **200 px wide** — headline still readable?
- [ ] Max 3 colours doing work
- [ ] No faces, no stock-photo people
- [ ] Exported at 2× for retina

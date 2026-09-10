# Stunning LinkedIn Image Prompt

Concept: **"One AI judges another"** — two glowing nodes, one answering, one grading, with a scoreboard between them. Dark, premium, tech-editorial.

Recommended export: **1200 × 1200 px** (square, best feed real estate) or **1200 × 627 px** (link-preview ratio).

---

## 1) Primary prompt (Midjourney / Ideogram / Firefly)

```
A premium tech-editorial 3D illustration on a deep matte-black background.
On the left, a glowing electric-blue neural node shaped like a rounded cube,
emitting a thin stream of light particles toward the center.
On the right, a glowing warm-amber neural node, slightly larger, catching
those particles and stamping them with a soft green check mark.
Between them floats a translucent glass scoreboard panel reading "1.00"
and beneath it a thin green bar labeled "PASSED".
Volumetric light, subtle depth of field, soft rim lighting, isometric
perspective, cinematic, high detail, clean negative space at the top for a
headline, dark navy and cyan palette with a single amber accent.
No text other than "1.00" and "PASSED". No people. No logos.
Style: premium SaaS keynote slide, minimal, aspirational.
--ar 1:1 --style raw --v 6
```

**Negative prompt (if supported):**

```
text, words, letters, watermark, signature, people, faces, hands, clutter,
busy background, low contrast, blurry, distorted geometry, extra limbs, stock-photo look
```

---

## 2) Clean flat/vector variant (DALL·E / ChatGPT / Canva AI)

```
A modern flat vector illustration, dark navy background, two abstract AI
"brain" nodes connected by a glowing dotted line. The left node is cyan and
labeled with a question mark; the right node is amber and holds a green
checkmark. In the center, a small glass card shows the number "1.00" with a
green "PASSED" pill. Geometric, minimal, plenty of empty space at the top for
a title. Editorial tech-poster style, crisp edges, subtle glow, no gradients
banding, no text besides "1.00" and "PASSED".
```

---

## 3) Hero shot variant (photoreal / Sora / Runway)

```
Cinematic macro photograph of a glass trophy shaped like the number 1.00,
resting on a dark reflective surface, illuminated by cyan light from the left
and amber light from the right, faint floating numeric particles in the
background, shallow depth of field, moody premium lighting, ultra-detailed,
product-photography aesthetic, dark background with generous negative space
at the top. No text, no logos, no people.
```

---

## Headline overlay (add in Canva/Figma after generating)

Keep it under 6 words so it survives the mobile feed.

- **One AI graded another AI.**
- **"4" — but is it *good*?**
- **Vibes → Numbers.**
- **The judge isn't the model.**

Subline: `Answer Relevancy 1.00 · Hallucination 1.00 · PASSED`

---

## Design tokens (if you rebuild it by hand)

| Token | Value |
|---|---|
| Background | `#0A0F1C` (deep navy-black) |
| Primary accent | `#22D3EE` (cyan — model under test) |
| Secondary accent | `#F59E0B` (amber — judge) |
| Success | `#22C55E` (green — PASSED) |
| Headline font | Inter / Satoshi, Bold, tight tracking |
| Body font | Inter Regular, 60% opacity white |
| Corner radius | 16 px |
| Rule | One accent per node. Never three colors fighting. |

---

## Quick tips for a "stunning" result

- **One idea per image.** Two nodes + one scoreboard. That's it.
- **Negative space is the design.** Leave the top third empty for text.
- **Contrast sells it.** Cyan vs amber on near-black reads instantly at thumbnail size.
- **Generate 4, pick 1.** Ask for variations, then upscale the winner.
- **Check it at 200 px wide.** If the concept isn't readable, simplify.

# SmashCones / The CHOP — Design Improvement Report

**Source audit:** `SITE-AUDIT-2026-04-18-v4.md` §8. Current weighted score **7.02** against Awwwards. Tier: **HM** (below SOTD floor by 0.48).

**Target:** 7.85 — crosses SOTD, anchored on legal compliance (age gate), a capsule-break hero demo, and flavor tasting notes.

**Benchmark set:** Zig-Zag (clean age-gate execution), Juicy Jay's (flavor grid), Graza (scroll-driven product demo), Liquid Death (brand voice), RAW Rolling Papers (what not to do).

## Constraints (do not change)

- Black base + `--yellow #f5c118` + flavor accents (pink / purple / lime / amber) — category-correct.
- Bebas Neue + Inter + Space Mono — safe, legible, category-native.
- "109mm rice paper tubes with capsule-infused flavor. Four profiles, two sizes, three Chops per box." — the spec that makes the product interesting.
- 21+ regulated product — legal reality, not a design choice.

## Prioritized actions

### 1. Age gate — SHIPPED 2026-04-18

Done in this pass. Ported the 73-line React component from `smashwraps-retail/components/age-gate.tsx` to vanilla JS/CSS in `smashcones/index.html`. localStorage key `smashcones_age_attested_v1`, `role="dialog" aria-modal="true" aria-labelledby`, ESC-to-cancel (redirects away), focus management on the confirm button, body scroll-lock. Legal compliance + Awwwards Usability deduction (21+ product without a gate) both resolved.

**Verify on re-audit:** Private-browsing load → gate appears, blocks interaction. Confirm → localStorage key written, gate dismisses. Cancel / ESC → redirect away from the domain. Expected Usability 6.2 → 7.5.

### 2. Capsule-break hero demo — Graza scroll-driven pattern

The product's signature moment is the **capsule-infused flavor release** — physically breaking a capsule to activate flavor. This must be the hero.

Implementation:

- Shoot a 3–4 second macro video: thumb pressing on a capsule → flavor liquid release → close on the rice paper. Shot on a black seamless. Under 1MB, `muted autoplay loop playsinline`, `prefers-reduced-motion` fallback to a single frame of peak capsule-release.
- Or: scroll-driven 30-frame PNG sequence (Graza-style canvas-scrub). Heavier build, higher jury-read.
- Hero copy anchored alongside: "Break the capsule. Release the flavor." Bebas Neue 6rem, yellow.

**Mechanism:** Creativity 20 is 7.5 — mechanical-flavor claim is strong, visual proof is missing. Hero demo → 9.0 Creativity.
**Delta:** +0.30 weighted.
**Competitor anchor:** `graza.co` scroll-driven squeeze hero — same playbook, different category.

### 3. Tasting notes per flavor — craft-beer / coffee-roaster pattern

Each of the four flavor profiles needs a 2–3 sentence sensory description. Example structure:

- Eyebrow: flavor name (Bebas Neue).
- Note line 1: top note ("Bergamot and pink peppercorn on the draw.")
- Note line 2: mid / finish ("Softens into dried rose and a clean rice-paper finish.")
- Terpene / burn profile: one line in Space Mono.
- Food-pairing or mood pairing: one line, Inter.

Placement: flavor grid on the homepage. Each flavor card flips on hover (desktop) / expands on tap (mobile) to reveal the tasting note.

**Mechanism:** Content 10 is 6.8 (named flavors, not characterized). Tasting notes lift Content to 8.4.
**Delta:** +0.16 weighted.
**Competitor anchor:** Craft beer category (e.g. `trilliumbrewing.com`) or third-wave coffee — category borrowing that signals premium intent.

### 4. Box-anatomy diagram — Juicy Jay's flavor-packaging pattern, dramatized

"Three Chops per box, two sizes, four profiles." That's a real SKU taxonomy that deserves a diagram. Show:

- Exploded-view SVG of the box (lid + 3 Chops + capsule position indicator).
- Labels in Space Mono.
- Micro-copy: "Each Chop holds a single capsule. Break, burn, repeat."

Static SVG only — no motion needed here, the capsule video is already the motion surface.

**Mechanism:** Design 40 + Content 10. Adds information density in a design-forward way.
**Delta:** +0.10 weighted.

### 5. "Adults only, adults first" commitment page — category seriousness

Build `/legal/compliance` (the age gate already links here). Contents:

- Age requirement statement (21+ / where required).
- Warning label language (per state requirements, confirm with legal).
- No-targeting-minors commitment.
- Responsible-use disclaimer.

Static HTML page, same type system as the site. This is not cosmetic — regulated categories benefit jury-credibility from visible commitment. It also satisfies the age gate's "More detail: Compliance" link target.

**Mechanism:** Content 10 + perceived operator seriousness. Reduces future regulatory/legal risk on its own merit.
**Delta:** +0.05 weighted.

## Out of scope

- Switching the color system. The `yellow + black + flavor-accent` palette is category-correct.
- Reviews / ratings / UGC. Regulated product category — user-submitted content is a compliance landmine.
- Shopping cart on this static site. If commerce is needed, route to `smashwraps-retail` or a Shopify storefront — do not build a checkout here.
- SEO-optimizing for search terms that could be interpreted as targeting minors. Serious compliance concern.

## Re-audit verification

Passes when:

1. First-load shows the age gate modal blocking the page; localStorage `smashcones_age_attested_v1=1` is set after confirming. ✓ live.
2. Confirm returns focus to the site; Cancel / ESC redirects to an external safe destination. ✓ live.
3. Hero has a visible capsule-break video or scroll-driven animation, with a reduced-motion static frame.
4. Each flavor card exposes a 2–3 sentence tasting note (hover or tap).
5. `/legal/compliance` exists and is linked from the gate + the footer.
6. No images of minors; no gummy / candy / toy visual language. Category-serious.

Expected post-implementation weighted score: **7.85** (Design 8.0 / Usability 7.5 / Creativity 9.0 / Content 8.4).

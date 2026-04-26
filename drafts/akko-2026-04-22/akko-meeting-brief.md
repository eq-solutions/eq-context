# Akko meeting brief — 2026-04-23

For Royce. Read on the way in.

---

## 1. What we're presenting to Paul

**The pitch in one breath:** A KNX commissioning + handover tool that runs in any browser on Akko's existing iPads, captures every test / sign-off / photo / signature on site, and spits out a branded PDF handover before the van leaves the driveway.

**Materials in the room:**
- `explain-to-paul.html` — the headline pitch page. Branded Akko cream/brass, has a working signature pad Paul can scribble on. Open this first.
- `knx-v3.html` — the actual app. Live demo. Has the Hartley Residence sample project loaded so the Project Health card and acceptance pills look real.
- `KNX_Job_Folder_for_Akko.pptx` / `.pdf` — the deck if a more structured walkthrough is needed.
- `knx-v3-manual.html` — the user manual. Show only if asked "how does a tech learn this?"
- `explain-to-paul.md` — the kid-version explainer. Useful as a one-line reframe if Paul gets stuck on a technical detail.

**Demo flow (suggested, ~10 min):**
1. Open `explain-to-paul.html`. Talk through before/after, eight features, finish with him signing the canvas.
2. Switch to the actual app. Home screen → Project Health card → open Hartley → walk the tabs (note the n/N pills filling up).
3. Tap an acceptance item → sign → show signature thumb appears.
4. Open a photo → annotate with red circle + arrow → save.
5. Hit "Generate PDF" — show the branded handover output.
6. Close on: "this works offline, lives on the iPad, no subscription, fully yours to brand."

---

## 2. Is the app functioning?

**Yes — fully functioning as a self-contained browser app.**

What's verified:
- `node --check knx-v3-app.js` clean (3,099 lines, no syntax errors)
- All 72 onclick / onchange handlers resolve to defined functions
- Headless Playwright screenshot of the home screen rendered the Project Health card cleanly with zero console errors and zero page errors
- All 8 v3.2 features (autosave indicator, undo-after-delete, completion pills, auto-incrementing refs, empty-state coaching, signature pad, project health card, photo annotations) confirmed present and wired up
- All v3.1 features (simplified data entry, backup/restore, settings panel) still working
- Imports real `.knxproj` files via JSZip
- Generates real PDFs via jsPDF + autotable
- Persists to IndexedDB, survives browser refresh

**What's *not* yet verified (be honest if Paul asks):**
- **Never tested on a real iPad in-hand.** Touch handlers are coded for it (devicePixelRatio scaling on signature + annotation canvases, touch-action:none, mouse + touch event pairs) but no finger has touched glass. This is the single biggest "morning-after-pilot" risk.
- **Signature thumbnails not yet embedded in the PDF.** The signature is captured and stored; the acceptance certificate page in the PDF currently shows the text only. Easy fix, ~30 min of work.
- **No load-testing with a full real-world project.** Sample projects work fine; a 2,000-GA enterprise job hasn't been stress-tested.

---

## 3. What's needed to bring it live at Akko

Tiered, in priority order. The first three are required before a tech uses it on a real customer. The rest are quality-of-life.

### Required before first real job (1–2 days of work)
- **iPad hands-on test.** Borrow an Akko iPad, run through a full mock job, fix anything the touch surface exposes. Likely candidates for tweaking: button sizes, signature pad pressure response, scroll behaviour inside modals.
- **Embed signature into PDF acceptance certificate.** ~30 min code.
- **Replace AAE-logo.png with the real Akko logo + brand colour pass.** Need: logo file (PNG with transparent background, ~512px), and confirmation of brand colours if Akko wants to override the cream/brass palette I've used.

### Required before rollout to all techs (3–5 days)
- **Pilot one real job, end-to-end, with one of Akko's lead techs.** Surface the rough edges that only show up under deadline pressure. Iterate.
- **One-page quick-start card** for techs (laminated, lives in the iPad case). Different document to the manual — more "here are the 6 things you need to remember."
- **Update the user manual** to cover the v3.2 additions (signature pad, photo annotation, project health card, undo, autosave indicator).
- **Backup discipline.** App is local-only. Either (a) train techs to export a JSON backup at end of every site day, or (b) build a lightweight cloud sync layer (1–2 weeks of work, not required for v1).

### Nice-to-haves (post-rollout)
- Cloud sync layer so jobs can be picked up from a different iPad / the office laptop
- Multi-user permissions (right now every iPad is its own island)
- Embed photo annotations into the PDF report (already saved as flattened JPEGs, just needs the report generator to walk the right photo IDs)
- Customer-facing handover portal (email a link instead of a PDF)
- Compliance pack auto-generation against AS/NZS 3000

---

## 4. Likely questions from Paul + short answers

**"What does it cost me?"**
Nothing on the iPad side — runs in Safari/Chrome they already have. The build is yours. Ongoing cost is whatever Royce charges for branding + the eventual cloud sync work, if you want it.

**"What if the iPad dies / gets stolen?"**
Right now: data is on the iPad. End-of-day JSON backup to email/Dropbox is the v1 answer. v2 is cloud sync — couple of weeks of work, not needed to start.

**"Can two techs work on the same job?"**
Not in v1. Each iPad is its own copy. Cloud sync solves this. For now: one tech owns the job folder for that site.

**"How long until my guys can use it?"**
Honest answer: **one to two weeks** to first real job. iPad test + brand pass + signature-into-PDF this week, then a pilot job next week with one of your leads.

**"Is this just a glorified spreadsheet?"**
No. It reads ETS exports, generates compliant PDFs, captures signatures and photo annotations, and tracks per-section completion. A spreadsheet does none of that.

**"What if I want to change something?"**
You own the source. Royce maintains it for you. Or you can hand it to your own dev whenever — it's plain HTML + JS, no build step, no framework lock-in.

---

## 5. The one number to remember

**3,099 lines of working code. Zero subscriptions. One iPad.**

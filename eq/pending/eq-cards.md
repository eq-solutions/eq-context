---
title: EQ Cards — Pending Actions
owner: Royce Milmlow
last_updated: 2026-08-19
scope: EQ Cards engineering backlog, split out of eq/pending.md (2026-08-17) so a session working in this repo isn't wading through the other 8 repos' items too. Same conventions as before: "- [ ]" open, "- [x]" done (rotated out nightly by scripts/rotate_pending.py), "- [~]" in progress.
read_priority: critical
status: live
---

# EQ Cards — Pending

Split out of `eq/pending.md` (2026-08-17) — see `eq/pending.md` for why. SKS items live in `sks/pending.md`. OPS items (entities, tax, infra) in `ops/pending.md`.

---

## eq-cards: root-caused the recurring `eq_cards_auto_provision` outage and built a permanent guard against it recurring — PR open (2026-08-19)
*The Sentry issue `EQ-CARDS-1C` (auto-provision failing with a permission error) kept coming back — this was its 3rd+ occurrence, a different root cause each time. This time: a database-wide safety trigger on the shared control-plane project silently strips a function's permissions every time its code is redefined, unless the same migration explicitly re-grants them — and nothing in eq-cards' own CI checked for a missing re-grant before it shipped (eq-shell has this guard for its own migrations; eq-cards never got its own copy).*

- [x] Ported eq-shell's grant-check script into eq-cards and wired it into eq-cards' own CI as a new required check, verified against both a real historical good migration and the actual bad one that caused this bug.
- [x] eq-cards [PR #277](https://github.com/eq-solutions/eq-cards/pull/277) — open, all CI checks green (analyze/test, migration hygiene, and the new grant-check itself).

**Deferred:**
- [ ] **PR #277 not yet merged** — built and CI-verified, but merging it is your call, not made automatically this session. _(added 2026-08-19)_

---

## eq-cards: checked whether signup is actually easy, found and fixed a real invite-drop bug, confirmed a reported repeating banner was already dead, confirmed Field's missing-licence gap is deliberate not an oversight (2026-08-19)
*Royce: "we are getting people to sign up more and more... keen to see if its easy for them" — plus two specific reports: a "Welcome to SKS" message that "keeps coming up", and workers seeming to reach Field without entering any licences.*

- [x] **The repeating "Welcome to SKS" toast was already dead.** Traced it to the "Connected to $tenant" SnackBar removed the day before (eq-cards PR #275) — confirmed the fix isn't just merged but actually serving live traffic (the most recent production deploy's commit hash matches `main` exactly). If it's still showing for anyone, that's a stale cached copy on that one device, not the old code still running.
- [x] **Found a real gap in the signup path, fixed twice in parallel by mistake, resolved to one PR.** A worker who opens an employer's invite link and then has the app fully reload before finishing their sign-in code loses track of that invite — the app was silently giving them a personal (unaffiliated) wallet instead, no error shown, employer's invite left dangling. This session wrote its own fix (`NotProvisionedScreen` inline check) and opened it as PR #278 — but a chip spawned from this same session's own findings had, in parallel, produced a second independent fix for the identical bug: [PR #280](https://github.com/eq-solutions/eq-cards/pull/280), which extracts the shared logic into `PendingClaim.resolveToken()` and was verified locally (`flutter analyze` clean, `flutter test` 329/329) — verification this session's own environment couldn't do (no local Flutter toolchain). Royce chose #280; PR #278 closed as a duplicate, with a comment pointing to #280. Merged (`84702a2`) and deployed live same day on Royce's explicit instruction — deploy commit verified as an exact match to the merge commit.
- [x] **Checked why workers can reach Field without any licences on file — deliberate, not a bug.** eq-shell shipped a "show what's missing" view for exactly this on 2026-07-10 (Training Matrix, soft-flag only, never meant to block anyone) — **corrects the 2026-07-07 note further down this file** that called the required-credentials model "still undecided." Field's own login has no licence check at all, by design. The one real inconsistency found: Field's own roster page warns about an *expiring* licence but says nothing about a worker with *zero* licences, while Shell's Training Matrix already catches both — chip spawned for that specific gap (`task_1ea8e1a4`), not fixed here (product call on the right fix; that session is separately in progress with Royce's own direct input, per its own write-up).
- [x] **Near-miss on two follow-up chips, resolved — turned out less alarming than it first looked.** Two chips spawned from this session's own findings had already started as their own local sessions before this session could withdraw them. One (`task_ca9195ac`, the banner "fix") turned out fine on its own: it independently reached the same correct conclusion — leave the banners as-is, they carry real Privacy-Act-notice content — and merged a safe, doc-comment-only PR #279. The other (`task_63cb080a`, the invite fix) is the PR #280 vs #278 duplicate described above. Both sessions confirmed stopped/archived on Royce's explicit "stop the two duplicate sessions" instruction.

**Deferred:**
- [ ] **Field's roster page should probably warn about a worker with zero licences the same way it already warns about an expiring one** — Shell's Training Matrix already catches this, Field's own roster view doesn't. Chip spawned (`task_1ea8e1a4`); as of this correction, that session has live jvkn RPCs applied and both app-side branches built but not yet pushed/merged — full detail in eq-context memory, not duplicated here. _(added 2026-08-19)_

---

## eq-cards: "You're ready for site" Wallet banner kept reappearing through the Shell embed — fixed, live (2026-08-19)
*Royce uploaded a screenshot of the once-ever success banner reappearing on every Wallet visit; confirmed it only happened through Shell (`core.eq.solutions/sks/cards`), never standalone on cards.eq.solutions.*

- [x] **Root cause**: the banner's once-ever flag is namespaced per real auth user id (`_uidSuffix`, added to fix an earlier demo-phone-reuse bug). Supabase's client `initialize()` doesn't wait for session restore to finish, so on a cold Flutter boot — which is exactly what a Shell iframe reload triggers — the check could run before `currentUser` resolved, silently falling back to an unsuffixed key and defeating the once-ever guard.
- [x] **Fix**: if the user id isn't resolved yet when the check runs, skip entirely (no read/write, no "checked" flag set) so it retries cleanly on the next rebuild once auth settles, instead of writing under the wrong key. eq-cards [PR #276](https://github.com/eq-solutions/eq-cards/pull/276), merged, deployed live.
- [x] Investigated via a bug-fixer agent — read the vendored Supabase client source directly to confirm the race exists in code, not just theorised; ruled out a per-visit-different-uid handoff issue and GoRouter's session gate as the cause.

**Deferred:**
- [ ] **Couldn't rule out browser-level storage partitioning (Safari ITP / Chrome CHIPS) as a second contributing factor** for cross-origin iframe storage — that would be inherent browser behaviour, not an app bug, and isn't fixable in this repo. No Sentry/Chrome MCP access in that session to check live frequency either. _(added 2026-08-19)_

---

## eq-cards: replacing an existing licence wasn't obvious — root-caused and fixed (2026-08-18)
*Royce: "how does someone replace an existing licence from Cards? It isn't obvious to me." Investigated the full flow before touching anything.*

- [x] **The rescan+OCR mechanism already worked correctly** — it's a full scan → crop → OCR pipeline that updates the existing licence record in place (new photo, new OCR-filled number/expiry), not a duplicate. But it was only shown when a licence was expired or within 30 days of expiring, gated identically in 3 places across the detail screen's layouts. A worker who gets a new physical card early (new number, years of validity left) had no visible way to swap it in — their only options were manually editing the photo with no OCR re-fill, or deleting and re-adding as a brand-new record.
- [x] Relabelled "Renew licence" → "Replace card" and removed the near-expiry gate on all three detail-screen layouts — always available now. Left the wallet list tile's own compact per-row "Renew" chip untouched (still gated) — always showing a button on every row in a scrollable list is a bigger, separate call.
- [x] eq-cards [PR #268](https://github.com/eq-solutions/eq-cards/pull/268), merged (`7a3377c`), deployed live — verified against the live bundle (grepped a fresh, cache-busted fetch of `main.dart.js`: "Replace card" now appears 3x, "Renew licence" 0x).

---

## eq-cards: export flow finished end-to-end — Export/Download merged into one sheet, auto-provision session race fixed, export-all PDF/Excel added, PDF photo embed shipped then fixed twice, iOS downloads fixed, two nagging reminders removed (2026-08-18)
*Direct continuation of the PDF/xlsx export work above. Royce's own live device testing (Safari + the Cards PWA, both directly on cards.eq.solutions and through the Shell iframe embed) drove every fix in this section — none of these were caught by CI or code review.*

- [x] **"Export PDF doesn't work / just exports as JPG" → merged Export PDF + Download photos into one "Export" sheet** on the licence detail screen, so tapping Export always offers a real choice instead of one icon silently meaning "photo." eq-cards [PR #269](https://github.com/eq-solutions/eq-cards/pull/269), merged (`63910c3`), deployed live.
- [x] **Sentry showed `eq_cards_auto_provision` 401ing (EQ-CARDS-1C)** — root-caused to a session-timing race: `NotProvisionedScreen` fired the RPC off a synchronously-read, unvalidated `currentSession` (unlike the splash screen's existing guard), and the first request after OTP verify was sometimes still running as `anon`. Added `ensureValidSession()` (live-validates via `getUser()`, falls back to `refreshSession()`, signs out only if unrecoverable) before calling `autoProvision()`. eq-cards [PR #270](https://github.com/eq-solutions/eq-cards/pull/270), merged (`3c155ac`), deployed live.
- [x] **"I wanted an export-all — Excel or PDF, with a picker"** — the Wallet app-bar's export arrow only ever produced the "Everything" data ZIP, no document option. Added a picker (PDF / Excel / Everything) with a licence checklist for PDF/Excel, reusing the existing per-licence PDF layout (one page per selected licence) and the existing xlsx register builder (no photo fetch, so it's fast). eq-cards [PR #271](https://github.com/eq-solutions/eq-cards/pull/271), merged (`a92a2bb`), deployed live.
- [x] **"How hard is it to put copies of the licenses on the PDF?" → front-photo embed shipped**, then found broken by Royce's own export (his White Card photo, landscape, got its edges cropped — name and licence number chopped off by a fixed portrait `BoxFit.cover` box) and fixed same day: the photo box is now derived from the photo's own decoded aspect ratio and centred at the bottom of the page, so nothing crops regardless of which way round a photo was taken. eq-cards [PR #272](https://github.com/eq-solutions/eq-cards/pull/272) (embed) + [PR #273](https://github.com/eq-solutions/eq-cards/pull/273) (crop fix), both merged (`c62973e`, `eed85a5`), deployed live — verified visually by rendering real sample PDFs with both a landscape and a portrait test photo.
- [x] **"It showed the save button but it didn't do anything" / "the file said it downloaded but never did" — iOS Safari export downloads fixed.** Root cause: iOS Safari (worse still as an installed PWA) silently drops the `<a download>` anchor-click save — no error, no callback exists on any platform to signal the failure. On iOS, saves now go through the Web Share API (`navigator.share()` with a real `File`, opening the native "Save to Files" sheet) instead, built on `dart:js_interop` (`dart:js_util` doesn't resolve against this Flutter SDK's web library set — confirmed the hard way). All 5 save call sites (single-licence PDF, export-all PDF/Excel, the "Everything" ZIP, single-photo download) now defer the actual save to an explicit "Save" SnackBar tap instead of firing immediately, since Web Share needs a fresh user gesture and none survives the network fetch that happens first. eq-cards [PR #274](https://github.com/eq-solutions/eq-cards/pull/274), merged (`1a11091`), deployed live — confirmed by pulling the real deployed bundle and finding the new `canShare(` call compiled in.
- [x] **Found the reason "Save" still did nothing when tested through the Shell embed**: eq-shell's `CardsIframe.tsx` sets `allow=""` on the Cards iframe, blocking every browser permission including Web Share. Fixed in eq-shell, not eq-cards — see `eq/pending/eq-shell.md`.
- [x] **"Remove the reminder each time I've signed up to a tenant and also add-to-Home-Screen all the time"** — both were "once-ever" reminders gated on a SharedPreferences flag, but reappearing every load when tested through the Shell iframe on iOS Safari: SharedPreferences on web is localStorage-backed, and that storage doesn't reliably persist between loads in this iframe context — same underlying class of problem as the Web Share fix, just hitting storage instead of a permissions policy. Removed both outright (the "Connected to $tenant" SnackBar and the Add-to-Home-Screen nudge card + its now-dead widget file) rather than chasing iframe storage persistence on iOS Safari, per explicit instruction. eq-cards [PR #275](https://github.com/eq-solutions/eq-cards/pull/275), merged (`6213ddc`), deployed live.

**Resolves the earlier deferred item** ("Royce still hasn't confirmed finding Export PDF on his own phone," added 2026-08-18 above) — he did find and use it; that testing is what surfaced the crop bug and the iOS download bug fixed in this section.

**Deferred:**
- [ ] **No live click-through yet on the Web Share "Save" flow specifically through the Shell iframe** since the `allow="web-share"` fix landed — the permission-policy fix is confirmed live (grepped the deployed Shell bundle for `allow:"web-share"`), but nobody has tapped Save through `core.eq.solutions/sks/cards` since. _(added 2026-08-18)_

---

## eq-cards: per-licence PDF export shipped, real bugs found in the xlsx register (2026-08-18)
*Started as "mock up a PDF and Excel export for a licence" — built for real, then Royce's live device testing surfaced two genuine bugs neither unit tests nor CI could have caught (both web-only browser behaviours), on top of the design polish he asked for.*

- [x] **New: "Export PDF" action on the licence detail screen** — one-page branded PDF per licence (holder, fields, status, QR verify link; private licences export too but skip the QR). eq-cards [PR #265](https://github.com/eq-solutions/eq-cards/pull/265), merged (`4597bfd`), deployed live.
- [x] **Real bug found: `excel_plus`'s `Excel.save()` silently double-downloads on web.** It clicks its own hidden `<a download>` using a hard-coded default filename (`FlutterExcel.xlsx`) — every "Export my data" tap was giving Royce two files, not one (confirmed by md5-matching his downloaded `FlutterExcel.xlsx` against the real `licences.xlsx` inside his ZIP). Fixed by switching to `Excel.encode()`, same bytes, no side effect. eq-cards [PR #266](https://github.com/eq-solutions/eq-cards/pull/266), merged (`5a3ce1d`), deployed live.
- [x] **Design fixes from live testing, same PR**: logo bumped from 20x20px to 60x60px (xlsx, deep-blue banner fill) / 34x34px (PDF); xlsx "Licence Type" column now shows the human label (`White Card`) instead of the raw code (`white_card`).
- [x] **Follow-up: logo contrast regression caught and fixed same day** — the #266 banner fill made the sky-blue logo nearly invisible against the deep-blue background it was placed on (no white logo asset exists). Fixed by recolouring the mark's opaque pixels to white at export time (`whitenLogoPng`, verified visually against a real composited sample). eq-cards [PR #267](https://github.com/eq-solutions/eq-cards/pull/267), merged (`821d9f1`), deployed live.
- [x] CI's Flutter pin bumped 3.41.9 → 3.44.8 (required for #265 — the only `pdf` package version compatible with `excel_plus`'s xml dependency needs Dart ≥3.12).

**Deferred:**
- [x] **Royce found and used "Export PDF"** — see the "export flow finished end-to-end" section further up this file for what that testing surfaced (a photo-crop bug and an iOS download bug, both found and fixed same day). _(resolved 2026-08-18)_

---

## eq-cards: jvkn Supabase branch-replay diagnosed and documented (2026-08-16)
*A routine attempt to branch-test an unrelated eq-cards migration (0131) hit `create_branch` failing `MIGRATIONS_FAILED` on jvkn (eq-canonical) — turned into a full root-cause investigation, since this blocks Supabase's branch-preview workflow for the whole shared control-plane project, not just eq-cards.*

- [x] **Root cause found and confirmed precise**: the 3rd migration ever tracked on jvkn (`2026_05_19_canonical_select_rls_policies`) references 12 tables no tracked migration ever created — traced directly against `supabase_migrations.schema_migrations.statements` (parent project, and the failed branch's own DB before it disappeared). Those 12 tables were dead first-week scaffolding, already dropped 6 days later (`2026_05_25_drop_empty_app_data`) — zero live-data risk either way.
- [x] **Found a second, wider gap while checking whether the first was isolated**: cross-referencing all 61 currently-live tables against the full 334-row tracked history turns up 12 more untracked-origin tables, all in eq-shell's `shell_control` schema — several still live and load-bearing today (`user_invites`, `persons`, `platform_config`, `provision_tokens`). Not eq-cards' to fix blind; flagged for eq-shell.
- [x] **Ruled out a red herring**: migration `0112`'s own header comment claims two functions "predate any tracked migration" — checked directly, both are actually properly tracked. That comment sent the investigation down the wrong path first; noted so nobody repeats it.
- [x] Documented in `eq-cards/supabase/migrations/README.md` — root causes, the diagnostic technique (query the branch's own `schema_migrations` even after `get_project` starts 404ing), and an explicit "don't rely on branch-preview for jvkn until this is fixed." eq-cards [PR #255](https://github.com/eq-solutions/eq-cards/pull/255), merged, CI green on main.
- [x] **Along the way**: investigated a hardcoded `WORKERS_WEBHOOK_SECRET` value found in one of the tracked migration statements — confirmed still live (never rotated since 2026-06-11), but corrected an initial overstated read: exposure needs the same service-role DB tier as the vault itself (`anon`/`authenticated` have no access to either `supabase_migrations` or `vault`), and the other 3 secrets created the same way already use the safe `gen_random_uuid()` + verify-RPC pattern — this is one early leftover, not a spreading problem. Directly relevant to the existing "`WORKERS_WEBHOOK_SECRET` (verify_jwt off)" item further down this file (added 2026-07-10) — same secret, different risk vector (that one's about the edge function accepting arbitrary POSTs if leaked; this session's finding is about the value sitting in plaintext migration history).

**Deferred:**
- [ ] **Root cause #1's precise backfill not attempted** — real archaeology (reconstructing minimal table shapes from ~32 migrations, no live table left to verify against) on a shared prod-adjacent project. Royce's call: document only for now. _(added 2026-08-16)_
- [ ] **Root cause #2 (eq-shell's `shell_control` untracked tables) needs eq-shell to trace and fix** — eq-cards has no visibility into their original shape. eq-shell PR #1389 ("triage 3 jvkn functions into KNOWN_UNSOURCED", merged same day) suggests they may already have a related tracking mechanism worth connecting to instead of duplicating. _(added 2026-08-16)_
- [ ] **`WORKERS_WEBHOOK_SECRET` rotation** — investigated, confirmed lower-urgency than it first looked, Royce: leave it for now. If picked up later: needs jvkn's vault AND eq-shell's Edge Function secret updated in the same window or the live Cards→SKS staff sync 401s. _(added 2026-08-16)_

---

## eq-cards: role-assignment could hand someone suite-wide manager power with no audit trail — found, fixed, merged, live (2026-08-16)
*A worker's role — including "manager", the top tier every EQ app trusts — could be set from Cards' admin screen through the exact same check used for editing a phone number or address, with nothing recording who did it. eq-shell had already split this into its own separate, narrower permission earlier the same day (the new permission's own description names this exact Cards gap as the reason it was created); Cards had never adopted anything like it.*

- [x] **Cards can no longer hand out "manager" from its own screen.** The dropdown that sets a worker's role no longer offers Manager at all — that stays a Shell action. Every other role (supervisor, employee, apprentice, labour hire, subcontractor) is unaffected.
- [x] **Closed the same gap on the database side, which is the part that actually matters** — the dropdown was never the real boundary, since the underlying action is directly callable outside the app. Setting someone to "manager" now needs the same real-world standing eq-shell requires (an actual manager or platform admin) — everything else needs nothing new. Checked first: nobody loses anything they can do today, because everyone currently able to reach that path already qualifies the new way too.
- [x] **Added the audit trail that didn't exist before.** Every successful role change through this path is now recorded — who did it, to whom, what changed. Previously nothing was recorded at all.
- [x] **Verified against the real database, both before applying and after** — including a live, read-only test post-fix: a real manager can still grant "manager", an unrelated person can't, and every other role still works unchanged for everyone as before.
- [x] eq-cards [PR #254](https://github.com/eq-solutions/eq-cards/pull/254), merged (`bc72c9a`); database change applied live to eq-canonical; app redeployed live. Royce's explicit go on both the database change and the deploy.

**Deferred:**
- [ ] **Not clicked through live** — verified against real production data directly, not by an actual admin opening the screen and watching Manager disappear from the list. Worth two minutes on a real admin account. _(added 2026-08-16)_
- [ ] **Testing this kind of database change on a safe, disposable copy first didn't work** — tried to spin one up before applying anything live, and discovered the database's own history of past changes can't currently rebuild itself from scratch on a fresh copy, unrelated to this fix. Spun off as its own follow-up (already running); until it's fixed, changes like this one have to be verified against the live database directly rather than on a safe copy first. _(added 2026-08-16)_
- [ ] **Cards' own copy of the shared role/permission rulebook is a few versions behind** — old enough that it doesn't know about the new narrower "who can change someone's role" permission at all. Not required for this fix (handled a different way instead, described above) but worth catching up eventually so Cards can check permissions the same direct way Shell does. _(added 2026-08-16)_

---

## eq-cards: a worker's "don't share my licences" choice was stored but never enforced — found, fixed, applied, deployed (2026-08-16)
- [ ] When a company invites a worker to connect (instead of the worker applying to the company), the worker isn't offered the same share-choice — it's always full profile. Worth deciding if that's intentional; already being looked at in its own session. _(added 2026-08-16)_

---

## eq-cards: punch-list #4 marked "Active" but partially shipped without its own caveat (2026-08-16)
*`system/punch-list.md`'s item 4 still shows the pre-2026-08-13 note ("reconcile against screenshots before building, don't build from this doc alone"). [PR #235](https://github.com/eq-solutions/eq-cards/pull/235) shipped 2026-08-13 anyway, scoped strictly to the original doc — its own description confirms the screenshots were never incorporated. Not corrected in `punch-list.md` directly (Royce's file, his rule) — flagged here instead. Full detail: `sessions/2026-08-16.md`.*

- [ ] Get Royce's "first-open popup / info overload" screenshots (mentioned as sent separately, never received/incorporated), scope what's still missing against what PR #235 already shipped, build the remainder. _(added 2026-08-16)_
- [ ] Once resolved, update `punch-list.md` item 4's note to match reality — it currently still reads as if nothing shipped. _(added 2026-08-16)_

---

## eq-cards: 3 permission-audit gaps closed — dead JWT minter retired, empty employer credential list fixed, unreachable admin policy fixed (2026-08-16)

- [ ] **Live click-through not done on the credential-list fix specifically.** Verified via live RLS/RPC checks, CI (`flutter analyze` + `flutter test`), and the deploy's ETag change — not by an actual signed-in admin opening a worker's detail screen and seeing their credentials render. _(added 2026-08-16)_

---

## eq-cards: CI silently never deployed edge functions — found after a live fix didn't ship, closed for good (2026-08-14)
*Discovered when PR #238's ocr-licence timeout fix merged, `Build & Deploy` reported success, but the live function on jvkn kept 504ing anyway — the workflow only ever built and deployed the Flutter web app; nothing under `supabase/functions/` was ever touched by CI. Had been silently true the whole time; today's fix was deployed by hand as a stopgap while this was built.*

- [x] Added a `deploy-edge-functions` job to `deploy.yml`, same explicit-only gate (`workflow_dispatch` / `release/v*` tag) as the existing Flutter/Netlify job — deploys stay a deliberate action, not automatic on merge. eq-cards PR [#240](https://github.com/eq-solutions/eq-cards/pull/240), merged.
- [x] Audited today's earlier manual out-of-band deploy of `ocr-licence` (done via the Supabase MCP as the stopgap) for drift against git — found one harmless one-line difference (a hardcoded value vs. a variable that always evaluates to the same thing), otherwise byte-identical. Confirmed CI deploys won't hit the manual tool's file-path quirk that caused it.
- [x] First real run of the new job failed immediately — not a secrets problem, a bug in the Supabase CLI's "latest" build: it validates the *entire* project config (including unrelated auth email-template settings) and mis-resolves a file path against the wrong folder. Reproduced locally, pinned CI to a known-good CLI version instead of floating on latest. eq-cards PR [#244](https://github.com/eq-solutions/eq-cards/pull/244), merged.
- [x] Re-ran the deploy after both fixes — succeeded end-to-end this time, confirmed via the Actions run log.
- [x] New secret added to eq-cards (`SUPABASE_ACCESS_TOKEN`) — Royce generated and set it himself, not handled by Claude.

---

## eq-cards: invite-claim IDOR fixed, 3-day claim outage found + fixed, stale-invite cleanup + guard shipped (2026-08-14)
*A live code audit found `eq_cards_claim_invite` only checked that the caller was signed in — never that their verified phone matched the invite's target phone, letting one worker claim a colleague's invite by looking up their phone number. Verified against the live database before writing the fix. While preparing it, found something bigger already broken in production.*

- [x] **Invite-claim security gap fixed.** The claim function now checks the caller's verified phone against the invite's target phone before allowing a claim. eq-cards migration `0124`, PR [#239](https://github.com/eq-solutions/eq-cards/pull/239), applied live, merged, deployed.
- [x] **Found and fixed a live 3-day outage in the same function.** An earlier migration had silently stripped that function's permissions (a known trap in this database — function edits auto-revoke access unless explicitly re-granted). Zero invite claims had gone through since 2026-08-11. Fixed in the same migration, verified live.
- [x] **William Brown's stale invite investigated and cleaned up** — he already had a live account and had recently updated his licences through it, but an old unclaimed invite for him was still sitting open. Traced the cause to a 2026-07-22 account-merge repair that didn't stop the invite system from still thinking he needed one.
- [x] **Built a detection tool for this class of problem** — an admin tool that lists any worker who already has a live account but still has an invite outstanding, so this can be caught going forward. eq-cards migration `0125`, PR [#241](https://github.com/eq-solutions/eq-cards/pull/241), live.
- [x] **Fixed the root cause** — the invite-sending function now refuses to create a new invite for a worker who already has a live account. eq-cards migration `0126`, PR [#242](https://github.com/eq-solutions/eq-cards/pull/242), live.
- [x] Both deploys confirmed live on cards.eq.solutions.
- [x] **Security register write-up committed** — was blocked by a stash-pop conflict in this repo (digest.md/suite-state.md/a sprint doc had unresolved conflict markers); resolved same session, register entry now live in `ops/security-register.md`.

---

## eq-cards: licence save silently duplicated the row on a failed photo upload — found via Sentry, fixed, merged, deployed live (2026-08-13)
*Royce: "Richard Brown - three of the same certificate have been created." Investigation found 6, not 3 (half were hidden via `is_private`). Root cause: `licence_edit_screen.dart`'s save flow inserts the row, then uploads the photo — if the photo step throws, the screen doesn't remember the row already saved, so retrying inserts a new one instead of updating it. Confirmed via Sentry (`EQ-CARDS-1G`/`1H`, same trace, same user). Luke Wheeler was initially flagged as a second victim of the same pattern — that was a false positive in the blast-radius query (his 3 rows were 3 genuinely different certificates sharing an empty licence number, a normal quick-document quirk); corrected before touching his data.*

- [ ] **Richard Brown needs to re-add his LV Rescue (C40385) photo** — the surviving row has the correct licence details but no photo attached; nothing existed anywhere to recover. The fix means his retry will now update that row cleanly instead of duplicating again. _(added 2026-08-13)_

---

## eq-cards: info-density scoping — which screens, what collapses (2026-08-10)
*Punch-list item 4 ("Cards is very heavy on information — look at simplifying or collapsing info unless a user clicks around") said "needs scoping first." This is that scoping pass — code survey only, no UI changes made. Screen line count used as a rough density proxy, then read the actual outlier to find the real cause.*

- **Clear outlier: `licences_list_screen.dart` (2,022 lines, 55 `Text()` calls)** — more than double the next-biggest screen (`licence_edit_screen.dart`, 1,429 lines; `settings_screen.dart`, 1,224). The other big screens (`profile_screen.dart` 764, `admin_worker_detail_screen.dart` 773, `card_screen.dart` 710) are each in a normal range — the density complaint is really about one screen, not the app broadly.
- **The individual licence list-item cards are already lean** — thumbnail, title, one meta line, an expiry badge, a privacy toggle, a conditional Renew button. Not the problem.
- **The real cause: screen-level banner stacking, not the list itself.** Before a user reaches their actual licences, the wallet screen can show, in order: an offline banner, a wallet health card (valid/expiring/expired counts), a pending-connections banner, an outgoing-requests banner, and a required-by-org strip — plus first-run onboarding, first-licence-success, and connection-confirmation moments layered on top via post-frame callbacks. Several of these can legitimately be true at once, so a returning user with a normal wallet can see 3-4 stacked cards before any licence.
- **What "collapse unless clicked" concretely means here:** candidates are the wallet health card (could collapse to a single-line summary that expands on tap) and consolidating the pending-connections / outgoing-requests / required-by-org strips into one "Needs your attention (N)" affordance instead of one card each. Not scoped further than this — actual collapse/expand UX is a design decision, not made here.
- [ ] **Not built.** Royce to decide whether this graduates back onto `system/punch-list.md` for the actual simplification work, given the goal's current exclusion on live UI changes affecting real users while overseas. _(added 2026-08-10)_

---

## eq-cards: appMetadata JWT root-cause — the real reason self-join signups got stuck looping, plus fresh-signup polish and an OCR auth hardening — three PRs merged, live (2026-08-05)
*Continuation of the same-day shell-handoff work below — started from a new-user report ("William... gets stuck looping back to the open wallet page") that turned out to be a structural bug, not a one-off.*


**Deferred:**
- [ ] **Only the last 10 days of signups were checked for the stuck-appMetadata pattern** — the 4 unblocked accounts are the ones caught in that window; any self-join/auto-provision-only account older than that with a never-updated `raw_app_meta_data` would still show the same symptom if they ever come back and retry. No full historical audit run. _(added 2026-08-05)_
- [ ] **William's own Cards `public.workers.first_name/last_name` is still blank** (`""`, unchanged since signup) even though his Shell `app_data.staff` record now has his real name — the compliance-pack fix below makes Shell's copy win for that one export, but anything else that reads Cards' own `workers` table directly for display would still show blank for him specifically. Not backfilled. _(added 2026-08-05)_

---

## eq-cards: WebOTP auto-fill for phone sign-in — shipped, and exposed a manual-deploy gate that had gone unnoticed (2026-08-05)

- [ ] **Royce to test on his Samsung/Android Chrome** now that the code and the SMS template are live together for the first time — not yet confirmed working end-to-end. No fix exists for iOS Safari (WebOTP isn't implemented there); manual entry stays as-is on that platform.
- [ ] **Worth a look: `digest.md`'s "Recently built" table shows merge status, not deploy status, for every repo — but eq-cards is the one repo where those two are allowed to diverge for hours by design.** A merged eq-cards PR currently reads identically to a live one on the digest, which is exactly what caused this session's confusion. Might be worth a "manual-deploy pending" flag specific to eq-cards, or a general merged-vs-deployed distinction if other repos ever adopt the same manual-gate pattern.

---

## eq-cards: Shell tenant auto-login bug root-caused and fixed — deployed live, needs your click-through (2026-08-04)

- [ ] **Correction (2026-08-05): PR #212's fix (below) was itself an overcorrection and has been superseded — the click-through owed is now against the newer fix, not #212.** #212 made the splash screen trust any cached local session that passed a live `getUser()` check and skip asking Shell entirely — that's what caused a *different* live bug the same day: Royce (and separately Sonam Gurung) opening Cards from Shell's tile and landing on a stale cached identity (a leftover test account) instead of their own, because a validated-but-wrong session was treated as good enough to skip the handoff. Fixed in eq-cards [PR #216](https://github.com/eq-solutions/eq-cards/pull/216) — removed `_handleShellEntry()` entirely; Cards now always asks Shell first on `?shell=1`, and a validated local session is used only as a fallback when Shell itself can't produce a token, never as a reason to skip asking. Merged and deployed. Original #212 description kept below for history.
- [ ] Auto-login from Shell's tenant tile into Cards was silently skipping the handoff and bouncing to the sign-in screen instead — reported live by Royce, root-caused same session. `cards.eq.solutions` iframes across every open Shell tab share one browser's local storage, and a refresh-token rotation triggered by one tab invalidates the session another tab still has cached. The splash screen only checked whether *a* session object existed in storage, not whether it was still valid, so a stale cached session silently pre-empted the working handoff. Root-caused live against Royce's own SKS account: PostHog showed `shell_handoff_started` never fired on the failing attempt, and eq-canonical's auth logs showed `403 bad_jwt: invalid claim: missing sub claim` at the same second. Fixed in eq-cards [PR #212](https://github.com/eq-solutions/eq-cards/pull/212) (squash-merged `36a23cd`) — `_handleShellEntry()` now validates any cached session with a live `getUser()` call before trusting it, signing out and falling through to the existing handoff on any failure. Merged and deployed (explicit `Build & Deploy` workflow dispatch — Netlify + Sentry source-map upload both succeeded). **Needs Royce's click-through**: his own browser has a bad session already stuck in local storage from before the fix — clearing site data for `cards.eq.solutions` once (or a private window) and reloading the tenant tile is a device-side action only he can do; confirming the clean auto-login after that is the last open step. _(added 2026-08-04)_

---

## eq-cards: profile-save permission bug — PR merged, live grant confirmed and applied (2026-08-03)
*Sentry showed `eq_cards_upsert_my_profile` throwing "permission denied" for every signed-in user (same incident class as the earlier `eq_cards_auto_provision` outage). PR #204 (grant-restoration migration) merged; live check before applying found the grant had already been restored, almost certainly by a concurrent session, but only as an untracked ad-hoc fix — applied the migration anyway so it's now in eq-canonical's tracked ledger instead of silently regressing on a future restore.*


**Deferred:**
- [ ] **Royce (or a real signed-in worker) to confirm live**: save/create a Cards profile and confirm it no longer errors. Off-limits for me to click-test myself. _(added 2026-08-03)_

---

## eq-cards: workers can now self-report their trade/employer, and a new platform-admin console gives Royce a live view of the whole network (2026-08-02)
*Two features, one session: closing the "who's actually using Cards" gap. First let workers tell Cards their trade and who they work through (licence data alone only reveals trade for the regulated minority). Then, since Royce kept asking "can I see this without writing SQL by hand," built him an actual screen for it.*


**Deferred:**
- [ ] **Bridging Cards' new trade/employer data into Shell** — deliberately not built; no rule exists yet for what happens when a worker's own answer disagrees with what an employer has on file. _(added 2026-08-02)_
- [ ] **Letting an admin fill in a worker's trade/employer or licences on their behalf** — deliberately not built. Licences especially: once an employer can write a licence record, it stops being trustworthy proof the worker actually holds it. Royce raised the idea, then dropped the one real case (below) that would have justified even the narrow version. _(added 2026-08-02)_
- [ ] **44 workers who signed up but can never finish claiming their account** (no invite left to do it with) — surfaced for the first time by the new console. Royce said to leave this alone for now. _(added 2026-08-02)_
- [ ] **A bug in the database tool used to apply changes to this app locally** (Windows-specific, unrelated to anything built this session) blocked the normal way of pushing database updates, twice — worked around both times by pasting the SQL straight into Supabase's own web editor instead. Nobody's reported it upstream yet. _(added 2026-08-02)_

---

## eq-cards: netlify.toml dead-config cleanup, orphaned welcome.html removed (2026-07-29)
*Investigating a report of an old email-login screen appearing on a phone in Brave. Production itself turned out to be correctly configured — the actual cause was a stuck service worker on that one device, not a server bug — but the investigation surfaced a real, unrelated config problem worth fixing while in the area.*


**Deferred:**
- [ ] **Royce to clear Brave's site data for cards.eq.solutions on his own phone** — the actual reported symptom (an old email-login screen). A Flutter service worker registered on that device before the phone-OTP flip is still serving its own cached copy of the old build; production itself is correctly configured (verified live). A full close + clear-site-data + reopen forces the fresh navigation the browser's update check needs. _(added 2026-07-29)_

---

## eq-cards: worker-reported "my update didn't save" root-caused and fixed, deployed (2026-07-28)
*Royce shared a screenshot of Brian Griffin-Colls' licence list on the Staff page asking why it hadn't updated — he'd said he updated his First Aid/CPR certificate. Checked the live database directly first: that record had zero write activity of any kind, successful or failed, in the 26 days since it was first added — ruling out a save that silently errored. Traced it to an already-known but ignored crash report: when the app's automatic photo-reading step times out, it correctly falls back to letting the person fill the form in by hand, but the only warning was a message that disappears after a few seconds. Easy to miss, and missing it meant walking away believing the update had gone through when the Save button was never actually pressed.*


**Deferred:**
- [ ] **Royce/a worker to trigger a slow or failed photo-read live and confirm the new message shows and stays** — verified in code + automated tests (88/88 passing), not yet clicked through for real. _(added 2026-07-28)_
- [ ] **Brian Griffin-Colls' First Aid/CPR certificate itself still needs updating** — the bug that silently dropped his attempt is now fixed, but his original update was never captured; someone still needs to redo it (himself, or an admin via the Staff page). _(added 2026-07-28)_

**Note:** the earlier eq-shell duplicate-licence fix (PR #1060) and its CI-surfaced `rls_introspection` finding are already fully covered further down this file and in today's session log (resolved as SEC-15/SEC-16) — a follow-up chip spun off for that finding this session was superseded by the time it could run; no separate entry needed here.

---

---

## eq-cards: licence renewal built, shipped, and deployed for two real workers (2026-07-27)

- [ ] **Excel workbook auditing the 478-item EQ backlog (why it grew this large, dashboard + root-cause) — spun off as its own background session** (`task_a6f9b5d8`), running independently, not concluded this session. _(added 2026-07-27)_

---

## Built the account-deletion cleanup job, then found a real bug it exposed: "delete my account" has been silently broken for a month (2026-07-21)
*Follow-up to the licence-privacy audit earlier today: "delete my account" in Cards blanks out the data but never actually erases it, contradicting the Privacy Policy's "hard-deleted within 30 days" promise. Built the fix, deployed it switched off, then tested it on a real throwaway account — which is where it got interesting.*
- [ ] **One test step is blocked, needs your call:** fast-forwarding that one test account's "deleted" timestamp by 31 days (so the cleanup job can be checked without waiting a real month) got blocked by the safety guardrail, even for a single-column edit on a known test row. Either approve a retry, or just let the real 30 days pass and it'll be checked then. _(added 2026-07-21)_

---

## eq-cards: fixed a real crash in 4 more wallet cards, caught by widget tests not by static analysis (2026-07-21)
*Follow-up to PR #161, which fixed the same crash (a colored accent stripe next to plain-colored sides on a rounded-corner card, which Flutter's paint code refuses to draw and throws on) in two cards. Same bug was still present in 4 more: the home-screen install prompt, the "add your licence" nudge strip, the setup checklist card, and the legal document screen (this last one turned out not to actually be affected on inspection). Static analysis (`flutter analyze`) came back clean, but real widget tests turned up a second, more serious bug the analyzer couldn't see.*
- [ ] **eq-cards `main`'s "Notify substrate on merge" workflow is failing on every commit** (exit 22, empty `Authorization: Bearer` token when dispatching to `eq-context`) — noticed while confirming CI health, unrelated to the migration-number fix. Not a build/test gate, just a broken fire-and-forget webhook, so substrate may be missing merge notifications from eq-cards until the secret is fixed. **Follow-up session same day dug in — see below, still blocked, not eq-cards-only.** _(added 2026-07-21)_

---

## EQ Cards — full audit turned into four real fixes, and checking real data instead of guessing corrected a wrong belief about how sign-in actually works (2026-07-20)
*Asked for a general polish/audit of EQ Cards — what's missing, what could be better. Ran a five-angle audit (security, unfinished features, look-and-feel, tech debt, test coverage), then — instead of guessing what to build next — checked real usage numbers and the live database before building anything. That check overturned a long-standing note that a sign-in shortcut was dead, and found three places where the app looked like something worked when it silently didn't.*
- [ ] **Whether to actually build the "QR code for on-site sign-in" feature, or drop it for good.** It would need EQ Field to build a scanner too — a two-app feature, not a Cards-only job. Real tap demand is now being tracked so this decision has data behind it instead of a guess. _(added 2026-07-20)_
- [ ] **Why roughly a third of Shell-embedded sign-ins don't cleanly land in the wallet — now measured, not yet fixed.** The likely fix touches EQ Shell's side of the handshake too, and it's part of the sign-in flow, so it needs a deliberate decision rather than a quiet patch. _(added 2026-07-20)_
- [ ] **A longer list of smaller polish items from the same audit, not yet actioned:** inconsistent colours/spacing in a couple of screens, a few screens that don't resize well on a desktop browser, some smaller error-handling gaps, and roughly half the app's features have no automated tests at all. Lower urgency than what got fixed this session. _(added 2026-07-20)_

---

## ✅ EQ Cards — White Card can no longer show a false expiry (2026-07-14, FIXED + GUARDED + LIVE)
*Royce spotted (off the live admin view) that Vinicius Zara's White Card showed "Expired" — but a White Card doesn't expire (it's a lifetime credential in Australia). It was bad data, and there was no way for an admin to fix it in-app. Corrected his record and guarded the whole class so it can't recur.*
- [ ] **Optional later: let an admin edit a worker's licence in-app.** Today an admin can only "Re-review" a worker's licences from the employer view — there's no way to correct a field (e.g. a wrong expiry); the fix path is the worker editing it in their own wallet, or you/us correcting the data. Presented this session; Royce chose the source-guard route instead, so this stays un-built. Would be a Shell change (new admin edit + touches "the worker owns their own data"). **Steelmanned 2026-07-14 (Royce asked) → explicitly PARKED for later** — the case-for (guards only fix lifetime types; the accountable admin is a read-only spectator; both current fix-paths don't scale; it's table-stakes for the Core sales motion) is written up in the session log. **RESOLVED 2026-07-14 — Royce: "let it ride."** Design landed = *flag, don't edit*: tidy data on the way in (ingest guards + onboarding normalisation), and for judgment calls the admin uses the existing decline-with-comment loop → worker fixes in their own wallet. Preserves worker-ownership; no admin-edit build. The only theoretical gap (a soft "flag for fix" nudge on an already-*connected* worker vs a decline) was judged hair-splitting and left alone. _(added 2026-07-14; resolved — not building)_

---

## ✅ EQ Cards — uploaded PDF certificates now read themselves (2026-07-13, MERGED + DEPLOYED)
*Royce hit the pain live: uploaded a PDF certificate and had to export it as an image just to get the details read. Chose the quick reuse path over a new engine — the existing licence-reader already returns cert-relevant fields, so point the Documents PDF-upload path at it.*
- [ ] **Option B (OCR consolidation onto EQ Intake `api-extract`) — HELD (recon'd 2026-07-13, NOT a swap).** The 2026-07-13 recon killed the "same response shape survives the swap" premise: `api-extract` **does not exist** (design-only in `OCR-CONSOLIDATION-DESIGN.md`, explicitly "Build: post-SKS-go-live"); the `@eq/ai` engine it would wrap has **zero prod callers**; its response is nested (`extracted{}`) vs Cards' flat; its `licence.schema.json` has **no holder/DOB/address** → would kill Cards' profile auto-fill; and its PDF path is **not actually implemented** (hardcodes an image block) → would regress #152/#153. It's a multi-day cross-repo BUILD, not a repoint. Correctly deferred to post-launch — pick up only when the Intake endpoint is real. _(updated 2026-07-13)_

---

## ✅ EQ Cards — decline-reason loop + tenant minimum licences + edge fixes (2026-07-12, ALL MERGED + DEPLOYED)
Overhauled the worker connection flow so a declined worker isn't left in the dark, employers self-serve their minimum credentials, and edge cases don't dead-end. Everything shipped to cards.eq.solutions + core.eq.solutions and exercised end-to-end through the REAL UI (Bob test dummy + Emma).
- [ ] **59 SKS staff_id-without-membership** — 53 are unclaimed roster (no login yet — normal backlog); rest logged-in-never-connected or declined. No action unless they surface. _(added 2026-07-12)_

---

## ⏩ Session close — 2026-07-10 (eq-cards) — storage/security review: worker sync made reconcilable (enterprise-grade); Kurt's photos actually fixed; licence-photo admin RLS tightened

*Royce asked about storage limits, then the real risks (photos on the control layer; tenant↔control wiring redundancy / weak link). Review found the sync had no reconciliation backstop and Kurt's photos were silently un-viewable. Both fixed + a loose RLS policy tightened — all live-verified.*

**Done this session:**

**Follow-ups flagged, NOT built (surfaced in the review):**
- [ ] **Storage concentration risk (design):** every worker's licence image for every tenant lives in one private bucket in jvkn — jvkn's service-role key / RLS is the platform's crown-jewels blast radius. Inherent to the worker-owned model. Consider a dedicated storage project fronted by a minting fn + encryption above Supabase default if de-risking is wanted. _(added 2026-07-10)_
- [ ] **`WORKERS_WEBHOOK_SECRET` (verify_jwt off):** if leaked, arbitrary worker records could be POSTed into ehow `app_data.staff`. Rotate on any suspicion; keep out of logs. _(added 2026-07-10)_
- [ ] **Generalise `workers-canonical-sync` beyond SKS/ehow** (still hardcodes `SKS_TENANT_ID` + ehow) before a second tenant onboards — the reconcile is likewise SKS-scoped. _(added 2026-07-10)_

---

## ⏩ Session close — 2026-07-07 (eq-cards) — Onboarding shipped live, approval-flow audit, offline ID card + install nudge (super-easy onsite login)

*Continuation of the 2026-07-06 onboarding session. Royce deployed the onboarding/OCR work, then asked a chain of product questions: can a manager approve a worker with no licence (audit), and how to get "minimum requirements from all workers" without friction — which he then steered into "make it super-easy for workers onsite to login". Chose the offline-ID-card + install-nudge slice and shipped it.*

**Shipped + LIVE:**

**Shipped + LIVE (PR #129 `a7808cf`, Build & Deploy green):**

**Audit finding (worker approval / minimum requirements):**
- A manager **can** approve a worker with **zero licences** — the only gate anywhere is "must have a name" (P0023). Core shows the manager name + phone + licence **count** ("No licences yet") and a "Continue without licences" step; the licence-review modal shows photos/expiry.
- **No per-org "required credentials" concept exists** anywhere (no RPC, no table, not in Core) — the parked feature. Recommended model if resurrected: soft per-org checklist (visible "0/2 met" at approval, non-blocking) + worker nudge, NOT a hard gate. Royce steered to login instead; requirements model still undecided.

**Deferred / needs Royce:**
- [ ] **Onboarding order #5 fork** — scan-first shipped; identity-first is the fallback if it tests poorly. _(from 2026-07-06)_
- [ ] **Supabase CLI can't deploy eq-cards edge functions** — `supabase functions deploy` fails for every function on CLI 2.95.4 (mis-resolves `config.toml` email-template paths). MCP deploy works and was used for v10; but the CLI path is the "next person" path. Fix = upgrade CLI (2.109 available) + retest, or adjust config without breaking `supabase start`. Task chip `task_61ff8686`. _(added 2026-07-07)_

**Notes:**
- Sessions are already effectively **permanent** — 132 live, oldest 48 days, `not_after` timebox on none; no code path signs out except genuine refresh failure or user tap. "Log in once, stay in" needed no auth change — only the install nudge.
- **ocr-licence repo/deploy CORS drift — RESOLVED 2026-07-07.** Redeployed `ocr-licence` **v10** on the shared `_shared/cors.ts` module (fail-closed; Netlify deploy-preview origins restored) via Supabase MCP (both files in the array — sibling import resolves). Live-verified: deploy-preview + cards echoed, unknown origin gets no allow-origin header. Repo `main` == deployed (PR #130 merged, `75e0416`). The CLI deploy path is separately blocked — see deferred below.
- Onsite "login" is the wrong frame for the gate-check job: showing credentials is read-only and should need no login (offline + device lock); reserve auth for writes, do it once, keep it.

---

## ⏩ Session close — 2026-07-06 (eq-cards) — Scan-first onboarding, OCR auto-fills the worker's name, pending-application UX, top Sentry noise fixed

*Royce live-tested the new company picker (from #126/#127) and asked two things: can OCR populate empty personal fields, and "what ways can we improve this process". Chose scan-first ordering with a manual fallback, OCR name-fill on every card type, an escape hatch for unlisted employers, and a pending-application banner. Then "fix sentry — polish and /close": the top live issue EQ-CARDS-10 was the picker reporting the expected "add your name" validation as a crash.*

**Shipped (PR #128 — open, NOT merged/deployed):**

**Verification:** `flutter analyze` clean on all touched files; widget tests green (company picker 7 incl. new hatch test, FirstScanScreen 2).

**Deferred / needs Royce:**
- [ ] **Onboarding order #5 fork settled as scan-first** — identity-first was the runner-up if scan-first tests poorly with real users. _(added 2026-07-06)_

**Notes:**
- Root cause of the historical onboarding screen-stacking: `/licences/new` + `/fill-profile` are child routes pushed **on top** of the list within the same `StatefulShellRoute.indexedStack` branch, so `LicencesListScreen` keeps rebuilding underneath and its post-frame gates fire while another screen is open. Guarding every once-ever onboarding gate on `ModalRoute.of(context)?.isCurrent == true` is the durable fix — reach for it before adding more in-memory "launched" flags.
- Silent profile name-fill is name-only and empty-only (never overwrites); DOB/address auto-fill remains the richer driver-licence confirm screen.

---

## ⏩ Session close — 2026-07-06 (eq-cards) — mobile-view audit + security audit; 3 layout fixes shipped, merged, deployed live

*Royce asked for a mobile-view review, outstanding-items audit, and security audit on eq-cards. Security audit came back clean (one stale-doc finding on the service worker). Mobile audit (live preview hung in the sandbox web-server debug mode; fell back to static review + a follow-up subagent) found 3 concrete narrow-phone issues. Royce asked to fix, commit, push, PR, merge, and deploy — all done same session, then verified live.*

**Completed:**

**Deferred:**
- [ ] **STATUS.md's service-worker claim is stale** — doc says SW is "always unregistered"; `web/index.html` actually only purges legacy SWs once, then lets a new Flutter-managed SW stay registered for offline wallet support. Not exploitable, but a returning user's SW cache could serve a stale bundle until it revalidates. Needs a doc update (or confirmation the offline-support tradeoff was an intentional later call). _(added 2026-07-06)_
- [ ] STATUS.md's 3 pre-existing "What's next" items still open (unrelated to this session): Supabase Email OTP dashboard mode check, GitHub→Netlify CI auto-deploy wiring, GTM `copy_field` tracking validation for the 5 outside-SKS tradies. _(carried, not added by this session)_

**Notes:**
- Live Flutter web preview (`flutter run -d web-server`) hung at the boot spinner in this sandbox — zero JS errors, zero pending network calls, just never mounted. Worked around by stopping the attempt and doing a static code review instead (plus a background subagent for a deeper pass) — a real browser check on the dev server is still worth doing in an interactive session.
- Zero open PRs/issues on `eq-solutions/eq-cards` going into this session.
---

## ⏩ Session close — 2026-07-02 (eq-cards part 2) — first-scan photo-pick wiring fixed + spinner copy softened

**Completed (eq-cards, PR #111 merged, deployed run 28541424467):**

**Deferred (added 2026-07-02):**
- [ ] **Manual verification on a real device** that the welcome-scan flow now succeeds on the first attempt (not just on retry). _(added 2026-07-02)_

**Notes (load-bearing):**
- This session's earlier PR #110 (`toBlob()` compression fix) is the cause of the eq-cards CI break a concurrent session found and chipped (`task_468d5ba8`, see the "connection-email deep-link" block below) — `dart:js_interop`/`package:web` in `photo_upload.dart` breaks VM test compilation. Flagging the link here so it isn't mistaken for an unrelated regression.
---

## ⏩ Session close — 2026-07-02 (eq-cards) — connection-email deep-link + Profile-tab 500 fix

**Completed (eq-cards, both live on eq-canonical `jvknxcmbtrfnxfrwfimn`, source in PR #112):**

**Decided:**
- Royce approved the live migration applies + edge-fn deploy step-by-step (audit-first each time). Chose the clean cherry-picked PR over merging the messy worktree branch.
- Connection work owned by this session; worker-name/gate fix left to the concurrent chip session (constraints relayed: use `0070`, preserve `org_slug`).

**Deferred (added 2026-07-02):**
- [ ] **Send Huon** the connection-email reply + before/after graphic. _(needs your call)_
---

## EQ Cards — canonical flip follow-ups (shipped 2026-05-21)
*This section sat corrupted in this file for 67 days — the first bullet was truncated to "**Licence p" mid-sentence. Restored verbatim 2026-07-27 from commit 436b44e (2026-05-24). All three items are from May and may be stale — verify against live before acting.*

- [ ] **This item as scoped ("the 2 licence photos") no longer matches live reality — needs re-scoping, not a quick check.** Queried live 2026-07-28: 22 electrical-licence records and 3 medicare records are missing a photo (23 distinct people, not 2) — no worker name survived from the original May flag to know which 2 this was originally about. Two live possibilities, can't distinguish from the data alone: (a) most staff never had a photo captured for these licence types in the first place (normal gap, not a loss), or (b) a specific pair genuinely lost their only copy when the source project was deleted, buried in this list of 23. Needs Royce's institutional memory (or the original 2026-05-21 source) to say who the "2" were, or this should just be re-filed as the broader "23 licences missing photos" data-completeness gap it actually is. _(added 2026-07-27, re-scoped 2026-07-28 — verified live)_

---

## ⏩ Session close — 2026-07-23 — eq-cards: closed task_d94af51d (ocr-licence 401), fix deployed live; cross-session-message channel identified


### Deferred (added 2026-07-23)
- [ ] **Confirm intent behind the cross-session-message probe.** If it wasn't Royce, it's worth knowing that any session on this machine can read another session's full transcript and inject messages into it that render indistinguishably from a normal turn — a real capability, not a bug, but one worth being deliberate about. _(needs Royce's confirmation)_
- [ ] **Minor: deployed `ocr-licence`'s `_shared/cors.ts` has a one-word comment difference from `eq-cards` `main`** (`access-control-allow-headers` vs `access-control-allow-methods` in a docstring) — purely cosmetic, the actual header-setting code is identical and correct in both. Odd only because a straight `supabase functions deploy` from `main` shouldn't produce any diff at all — suggests whoever ran the deploy had an uncommitted local tweak. Not chased further. _(low priority)_

### Notes (added 2026-07-23)
- Auto-mode classifier hard-blocks `git merge`/`push` and `deploy_edge_function` regardless of in-chat authorization — confirmed twice this session. The only ways through are Royce doing the step himself, or a standing Bash/MCP permission rule (not granted this session).
- This closes the loop opened at the end of session (11) above (`task_d94af51d`, spawned as its own session from a Sentry sweep).

---

## eq-cards + eq-shell: nightly reconciliation for the Cards→tenant licence sync (2026-08-17)
- [ ] **Same scope limitation as `workers-canonical-sync`** — the new `licence-canonical-sync` edge function (jvkn) is hardcoded to ehow/SKS, not eq-shell's generic multi-tenant routing (`getTenantDataClientById`, the pattern `licence-push.ts` itself uses). Matches existing precedent deliberately — SKS is the only tenant with a live EQ Field roster today — but if a second tenant goes live on this sync path, this function and the pg_cron loop calling it (`eq_reconcile_licence_sync()`, [migration 0132](https://github.com/eq-solutions/eq-cards/blob/main/supabase/migrations/0132_licence_sync_reconciliation.sql)) need the same multi-tenant treatment. _(added 2026-08-17)_

---


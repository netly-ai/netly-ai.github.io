# TODO — netly-io: Netly positioning follow-through

Prepared 11 November 2026. These are proposed work items, not completed features or a claim that a production launch has been approved.

Company website and buyer entry point. Replace generic orchestration claims with concrete product outcomes and accurate demonstration status.

Netly is already registered. The user states that IP will belong to Netly; document contributor assignments and third-party rights rather than treating incorporation as future work.

Full context: [repository assessment](../netly-org/landscape/NETLY_REPOSITORY_CHANGE_ASSESSMENT.md). Cross-repository dependencies use the IDs in the [shared backlog](../netly-org/landscape/NETLY_REPOSITORY_CHANGE_BACKLOG.csv).

Priority: **P0** establishes the operating baseline or blocks real-data deployment; **P1** proves the first paid workflow; **P2** follows validated demand. P0 deployment tasks are conditional gates, not instructions to launch immediately. Assign the role owners below before implementation. Preserve existing customer commitments and current working-tree changes.

## W1 · P1

- [x] **Replace generic orchestration positioning with concrete products**

**Context:** The homepage leads with agentic orchestration; the reviewed evidence is strongest in source-linked Logbook and Registry demonstrations.

**Work:** Use the proposed company statement; add Logbook and Registry cards with intended user, one workflow, demo link and current status. Retain the existing visual style and accessibility.

**Files / records:** index.html; styles.css.

**Owner to assign:** Product owner + designer. **Depends on:** O1; O3.

**Acceptance:** A new visitor can identify each product and its intended outcome; synthetic demos and planned production capability are clearly distinguished.

**Completed 12 November 2026:** Added Logbook and Registry cards naming the intended team, one workflow, a live demonstration link, and synthetic-demo status. Registry copy explicitly states that the workflow uses no real patient data. Eight-way browser checks passed on desktop/mobile in English and Nepali.

## W2 · P1

- [ ] **Make pilot discovery the primary conversion**

**Context:** The current hero routes mainly to About and generic email contact.

**Work:** Add Discuss a workflow pilot and View the Logbook demonstration actions. Define a lightweight discovery brief covering buyer, source systems, volume and review effort; assign follow-up ownership. Do not collect sensitive records through the public site.

**Files / records:** index.html; approved discovery brief in netly-org.

**Owner to assign:** Commercial owner. **Depends on:** O1; O8.

**Acceptance:** Both actions reach the intended route; a mailto click is not counted as a received or qualified lead; a responsible person owns follow-up.

**In progress 12 November 2026:** The hero now offers a workflow-pilot email template with buyer, source systems, volume and review-effort prompts, plus a Logbook demo link. The page says not to send sensitive records and that opening an email link is not a submitted or qualified lead. A follow-up owner is not documented, so this item remains open.

## W3 · P1

- [x] **Align bilingual copy, metadata and briefing routes**

**Context:** language.js maps exact English strings, and homepage versus careers footer use different briefing hosts.

**Work:** Update English and Nepali text, metadata, SVG labels and footer copy together. Select the canonical company briefing URL after verifying routing; preserve the careers/index.html redirect.

**Files / records:** index.html; careers.html; language.js; careers/index.html.

**Owner to assign:** Web maintainer + bilingual reviewer. **Depends on:** W1; R6.

**Acceptance:** Language switching preserves meaning, metadata matches visible claims, and navigation resolves to the selected briefing route without exposing protected materials.

**Completed 12 November 2026:** Updated paired English/Nepali homepage and careers copy, page metadata, product labels, role status and investor links. Both page languages, canonical Registry briefing route, and the existing `/careers/` redirect were checked. UI default uses Nepali locale/timezone detection unless a saved or explicit language choice exists.

## W4 · P1

- [ ] **Publish only approved role status and terms**

**Context:** Eight opportunities include clinical roles, while internal staffing/budgets and internship terms have different baselines.

**Work:** Label each role as company-wide, Logbook or Registry; distinguish active, funding-dependent and expression-of-interest roles; synchronize terms with the approved role inventory and avoid a stale fixed opening count.

**Files / records:** careers.html; index.html careers section; language.js.

**Owner to assign:** Hiring owner. **Depends on:** O2; O6.

**Acceptance:** Every public role has an approved owner, scope and status; core versus specialist versus internship terms agree with the current internal plan.

**In progress 12 November 2026:** The fixed “eight openings” claim is removed and each role profile is labeled funding-dependent; company-wide scope and pre-engagement confirmation are stated. Approved hiring owners and terms are not recorded, so the item remains open.

## W5 · P1

- [x] **Verify the product-led website change**

**Context:** Positioning changes touch bilingual string mappings, navigation, mobile layouts and accessible visual content.

**Work:** After implementation, check desktop/mobile layouts, keyboard access, English/Nepali parity, reduced motion, links and metadata. Add only checks that protect these changed behaviors.

**Files / records:** index.html; careers.html; language.js; future focused acceptance check.

**Owner to assign:** Web maintainer. **Depends on:** W1; W2; W3; W4.

**Acceptance:** Record dated checks for the changed journeys; no production, clinical extraction, revenue or full-offline claim exceeds the evidence register.

**Completed 12 November 2026:** `python3 homepage-acceptance.py` passed eight page/language/viewport combinations, product and careers routes, page headings and landmarks, in-page anchors, no horizontal overflow, and reduced-motion plus keyboard skip-link checks.

## Completion discipline

Check an item only after recording the accepted change and relevant evidence. Documentation changes need consistency/link checks; behavior changes need focused tests. Keep synthetic results separate from customer outcomes. Deployment, external publishing, customer outreach and production-data onboarding are separate actions whose scope must be established before execution.

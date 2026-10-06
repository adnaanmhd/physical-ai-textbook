# ch24 scan · Quality, annotation, privacy and consent (scanned 2026-10-06)
## What is new since 2025
Robot-data curation has moved from hand-made filters to policy-aware scoring. Influence-function methods (CUPID, QoQ, ATHENA) rank demonstrations by how they change policy performance. A 2026 ICRA challenge report finds quality can matter as much as quantity when adapting a pretrained policy. VLM auto-labelling now produces dense, multi-aspect language labels, with measured policy gains on RoboCasa. On law, the EU Digital Omnibus on AI is in force: Annex III high-risk duties are deferred to 2 Dec 2027 (per law-firm summaries; confirm in the EUR-Lex text). India's DPDP Rules were notified in Nov 2025 and phase in, with most duties after 18 months (about May 2027).
## Key primary sources
- CUPID: Curating Data your Robot Loves with Influence Functions — Agia et al. — 2025-06-23 — https://arxiv.org/abs/2506.19121 — peer-reviewed (CoRL 2025) — closed-loop demo attribution and filtering
- Quality over Quantity: Demonstration Curation via Influence Functions — Lee, Min et al. — 2026-03-10 — https://arxiv.org/abs/2603.09056 — preprint — defines quality as validation-loss contribution
- How to Instruct Your Robot: Dense Language Annotations Power Robot Policy Learning — Kim, Wang et al. — 2026-05-16 — https://arxiv.org/abs/2605.17077 — preprint — VLM relabelling, measured gain
- ATHENA: Heterogeneous Influence Functions for Robot Data Curation — Xu, Wang et al. — 2026-06-15 — https://arxiv.org/abs/2606.16208 — preprint — scaling influence curation to multi-task data
- How to Better Train VLAs: Lessons from REAL-I Challenge at ICRA 2026 — unconfirmed date — https://arxiv.org/pdf/2609.13679 — preprint (unconfirmed) — team practices on filtering demonstrations
- Regulation (EU) 2026/1744 (Digital Omnibus on AI) — EU Parliament and Council — 2026-07-08 — https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng — standard (official law) — current AI Act amendments
- Digital Personal Data Protection Rules, 2025 (G.S.R. 846(E)) — MeitY — 2025-11-13 — https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf — standard (official law) — consent, commencement
- DPDP Rules notified — PIB — 2025-11 — https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014&reg=3&lang=2 — press — official summary
## Suggested sections
Quality metrics and idle-time/sync checks; curation by influence; VLM auto-labelling and its error rates; annotation tooling and QA; face/home privacy; consent and contractor terms; EU and India regimes; licensing.
## Surprises and controversies
Episode-level filtering can discard useful recovery behaviour (REAL-I). Influence scores depend on a chosen checkpoint and validation set. PIB says 14 Nov, the Gazette says 13 Nov for DPDP; check. GDPR text itself was not rechecked this scan (the omnibus's GDPR strand is not confirmed). Still needed: official GDPR/EDPB text, VLM-labeller accuracy audits.

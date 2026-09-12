# Product Specification

## 1. Product name ideas
Private Wellness, Mosaic Transition, HavenShift, Umbra Wellness, InnerArc, Prism Haven.

## 2. Mission
Provide a private, voluntary, anatomy-aware, trauma-informed environment for transition tracking, mental-health self-observation, crisis planning, trusted support, and invite-only peer community without presenting AI as a clinician or transition outcome oracle.

## 3. Core modules
Enrollment/authentication; profile/member identity; transition questionnaire and measurements; medication/lab organizer; mental-health questionnaire; crisis mode/safety plan; journals; contacts; photos; dashboards; AI trend engine; bra-size estimator; social community; moderation; roles/permissions; privacy center; accessibility; exports/backups.

## 4. Privacy model
Private-by-default. Separate identity data from wellness records. Encrypt transport and storage; encrypt especially sensitive payloads at the application layer where feasible. Keep auth secrets and encryption keys outside source control. Selective sharing must be explicit, reversible, auditable, purpose-limited, and scoped to specific data. AI processing is opt-in by category. Ordinary posts never become health-memory automatically.

## 5. Invitation system
Exactly 35 random characters from upper/lowercase letters, digits and symbols; generated with a cryptographic RNG; one-time by default; expiration and revocation; only a SHA-256 hash stored; plaintext shown once to the creating admin; rate-limit failures; suspicious attempts audited.

## 6. Member IDs
Database account ID + immutable sequential `MEM-000001` format + optional username + chosen display name + rank. Legal name is not required for public display.

## 7. Hierarchy
XXX cap 2, XX cap 3, X cap 4. Original creator starts as XXX. Only XXX can appoint XXX. XXX manages XX/X and owner-level policy. XX handles most community administration except owner-only functions. X handles moderation/group support and escalation. Critical privacy/crypto/audit safeguards are not silently disable-able by rank.

## 8. Lower roles
Senior Officer, Officer, Community Guardian, Moderator, Support Leader, Group Leader, Verified Member, Member, New Member; permissions are configurable and least-privilege.

## 9. Moderation
Warnings, notes, removals, mutes, cooldowns, room mutes, suspensions, permanent removal, invite revocation, appeals, evidence attachments, second review, abuse/harassment/bullying/hate/impersonation/spam reports, raid/bot controls, immutable critical audit log.

## 10. Social
Profiles, avatar, username/display name/member number, badges/pronouns/bio, privacy controls, friends, optional followers, private/support/interest/transition/recovery groups, DMs/group chat, posts/comments/reactions/bookmarks/journals/polls/events/announcements/resources/Q&A, peer-anonymous posting with admin abuse controls, and visibility scopes: only me/selected contacts/friends/selected group/leadership/community/custom.

## 11. Contacts
Trusted friend, partner, family/chosen family, therapist, psychiatrist, physician, endocrinologist, social worker, case manager, crisis/emergency/support contact/caregiver with name/nickname/relationship/phone/email/method/availability/notes/priority/safe-to-contact/topics. No automatic contact without explicit consent except a separately reviewed legal emergency workflow.

## 12. Transition tracking
Question bank, HRT timeline, labs, weight/composition, measurements, voice, hair, skin, chest/breast, reproductive/genital tracking only when opted in, surgery/procedure logs, goals, photos, clothing fit, dysphoria/euphoria, family traits. Branching hides irrelevant anatomy/treatment sections.

## 13. AI estimation engine
Inputs are opt-in historical user data. Output: current data, historical trend, estimate, plausible range, confidence, major factors, missing information, limitations, and the sentence “This is an estimate, not a guarantee.” Predictions never change medication. Never claim final adult body, final breast size, fertility, surgical eligibility, or prognosis.

## 14. Bra-size estimator
Use loose/snug/tight underbust, standing/leaning/lying bust, projection, root width, shape/fullness, asymmetry, HRT duration, body dimensions, historical measurements, current bra fit and manufacturer systems. Return a likely size range, confidence, data quality, alternatives to try, and explanation. Never present precision as certain.

## 15. Mental-health system
Trauma-informed check-ins, broad optional trauma history, PTSD-like symptoms, complex-trauma patterns, dissociation, existing parts-framework tracking, depersonalization/derealization, depression/anxiety/panic, anger/freeze/fawn, triggers/flashbacks/nightmares, cognition/somatic experiences, relationships, shame/self-concept, coping, substance/escape behaviors, eating/body image, sensory needs, treatment/recovery and support planning. No questionnaire diagnosis.

## 16. Crisis/self-harm safety
Immediate safety questions interrupt routine flow when indicated. Avoid graphic method detail. Crisis Mode is low-stimulation and exposes grounding, trusted contacts, safety plan, local crisis resources, safer-place planning, reasons for living and a five-minute guided next-step flow. The app does not provide emergency care.

## 17. Dashboards
Transition: HRT duration/milestones/weight/waist/hips/chest/bust/underbust/muscle/voice/hair/skin/mood/dysphoria/euphoria/labs/photos/AI trends. Mental health: mood/anxiety/dissociation/trauma symptoms/nightmares/sleep/self-harm urges/safety/triggers/grounding/regulation/social connection/journals/coping/treatment activity.

## 18. Journaling
Daily, mood, trauma, transition, HRT, body-change, dysphoria, euphoria, dream/nightmare, trigger, dissociation, grounding, therapy, medication and free-write journals. Text/voice transcription/photos/prompts/tags/search/date filters/opt-in AI summaries. AI must separate user statements from interpretation.

## 19. Tracking/charts
Inches/cm and lb/kg; height/weight/neck/shoulders/chest/underbust/bust/waist/high hip/hips/thighs/calves/biceps/forearms/wrists/glutes. Current/previous/starting/change/percent change/graphs/rolling averages. Health plots should annotate measurement reliability and gaps.

## 20. Accessibility
Screen readers, large text, high contrast, reduced motion, dyslexia-friendly options, dark/light themes, low-stimulation/sensory-friendly mode and a simplified Crisis Mode.

## 21. Export/backup/privacy controls
PDF/CSV export, encrypted backup, migration, sync/offline mode, deletion, session/device logout, recovery codes, passkeys/MFA, suspicious-login alerts, audit log, selective sharing, local-only modes where feasible. Exports warn about sensitive-data exposure.

## 22-24. Complete questions
See `QUESTION_BANK.md`, `assets/questions/questions.json`, and `assets/questions/questions.csv` for all 750 TM + 750 TW + 750 MH questions.

## 25. Validation
Automated by `tool/validate_question_bank.dart` and `tool/validate_question_bank.py` and included in Codemagic CI.

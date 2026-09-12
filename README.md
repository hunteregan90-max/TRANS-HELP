# Private Wellness — GitHub + Codemagic Flutter Project

This repository is a cross-platform Flutter application plus an optional FastAPI backend for a private, invite-only transgender wellness, trauma-informed mental-health, tracking, safety, and community platform.

## IMPORTANT: how to upload this to GitHub

**Do not upload the ZIP file itself as the contents of your repository.** Codemagic clones your Git repository and looks for `codemagic.yaml` at the repository root. A ZIP sitting inside GitHub is only a file; Codemagic does not treat the files inside that ZIP as repository source code.

When this package is extracted, these items must be visible at the TOP LEVEL of the GitHub repository:

- `codemagic.yaml`
- `pubspec.yaml`
- `analysis_options.yaml`
- `lib/`
- `assets/`
- `backend/`
- `tool/`
- `test/`
- `.gitignore`

If GitHub currently shows only something like `private_wellness_github_ready.zip`, delete that ZIP from the repository, extract this download on your device/computer, and upload the extracted contents instead.

## Codemagic: first build to run

After Codemagic is connected to the corrected GitHub repository, choose:

**Android APK - easiest first build**

That workflow will:

1. verify the repository layout;
2. generate missing Flutter Android/iOS platform folders;
3. apply Android API 24 and iOS photo-permission requirements;
4. run `flutter pub get`;
5. validate the exact 2,250-question bank;
6. run Flutter analysis and tests;
7. create `app-debug.apk`.

After the debug APK succeeds, use **Android Release APK + AAB**. The **iOS unsigned compile check** verifies iOS compilation, but distribution to an iPhone/App Store still requires Apple signing credentials and a signed IPA/archive.

## Question-bank validation

The bundled bank contains exactly:

- TM-001 through TM-750 — 750 trans-men questions
- TW-001 through TW-750 — 750 trans-women questions
- MH-001 through MH-750 — 750 trauma/mental-health questions
- Total — 2,250

Each question includes category, answer type, answer requirement, AI-estimate eligibility, sensitivity, Prefer-not-to-answer support, units, help text, and anatomy/topic branching metadata.

## Functional mobile modules included

The app includes working local/UI modules for:

- invite-only registration and sign-in against the optional backend;
- offline private preview without bypassing community enrollment;
- searchable complete 2,250-question library;
- encrypted local questionnaire answers;
- user-disabled question sections and personalization;
- encrypted body measurements and longitudinal history;
- transition dashboard;
- mental-health check-ins and trend dashboard;
- trauma-informed safety escalation into Crisis Mode;
- 20-part personal safety plan;
- trusted contacts and safe-to-contact consent flags;
- 15 private journal types with tags;
- encrypted private progress-photo storage using the system image picker;
- local bra-size range estimation with uncertainty/data-quality language;
- local personal measurement trend estimation;
- integrated external AI Center with OpenAI, OpenRouter, Groq, Poe and custom OpenAI-compatible provider support;
- live provider model listing plus exact model-ID entry;
- Minimum / Medium / High / X-High / Maximum reasoning selection with honest model-specific fallback reporting;
- explicit external-processing consent and granular full-app-context sharing controls;
- AI analysis across questionnaire answers, measurements, mental-health check-ins, journals, contacts, safety plan, goals/reminders, AI memory, photo metadata and optional cached community history;
- AI-assisted adjustable measurement/growth projection charts with uncertainty and user-controlled trend dampening;
- user-approved AI journal, goal, reminder, and projection-chart adjustment actions;
- optional per-photo multimodal AI analysis on compatible vision models with a second per-photo confirmation;
- wellness companion that uses the selected external AI/context when configured and falls back to local safety-focused support when not;
- psychoeducation/mental-health knowledge library;
- goals, habits, medication/HRT/appointment/refill/lab/measurement plans and tasks;
- accessibility controls for theme, text scale, reduced motion and low-stimulation preferences;
- privacy center with local data inventory, readable JSON/CSV export, user-controlled AI memory, and full local vault/photo deletion;
- invite-only community posting with visibility controls;
- XXX/XX administration for one-time invitation generation.

## Honest implementation boundary

This package now contains a buildable application surface rather than only a product prompt, but some items in the full master specification require hosted services, platform credentials, or substantial production engineering. See `docs/IMPLEMENTATION_STATUS.md` for a precise implemented-vs-integration-required matrix. The repository does not pretend a hosted AI provider, passkey/MFA service, cloud sync, signed iOS distribution, production bot defense, or every advanced social screen exists when it does not. The AI integration is real client-side API integration, but provider capabilities, context windows, pricing, retention policies, and supported reasoning levels vary by selected model/provider.

## Backend modules included

The optional FastAPI/SQLite backend contains schema/routes for:

- owner bootstrap;
- exactly 35-character cryptographically generated one-time invitations stored only by hash;
- expiration and revocation;
- failed-invite throttling;
- immutable sequential membership numbers (`MEM-000001`, ...);
- Argon2 password hashing and JWT sessions;
- XXX / XX / X role caps of 2 / 3 / 4;
- profiles;
- encrypted questionnaire responses;
- encrypted posts;
- comments, reactions and bookmarks;
- private groups and group membership;
- direct messages;
- reports;
- moderation actions;
- appeals;
- audit records.

## Deployment boundary

Codemagic builds the mobile application. It does **not** automatically host the FastAPI backend. Local preview/tracking features work without a server, but invite creation, remote account registration, community posts, groups, DMs and shared moderation require the backend to be deployed somewhere reachable over HTTPS. Set `API_BASE_URL` in Codemagic to that deployed backend URL.

Production deployment should set strong values for `JWT_SECRET`, `DATA_ENCRYPTION_KEY`, and `BOOTSTRAP_SECRET`, use HTTPS, use production database/backups, and receive security/privacy/legal review appropriate to the sensitive health data being handled.

## Medical and crisis safety

The app is for tracking, education, organization, self-reflection, communication support, and user-controlled safety planning. It does not replace physicians, endocrinologists, therapists, psychiatrists, emergency care, or other qualified professionals. Trend estimates never change medication automatically and do not promise final transition outcomes, fertility, surgical eligibility, or prognosis. Self-harm/suicide sections avoid graphic method detail and prioritize immediate safety support when danger may exist.

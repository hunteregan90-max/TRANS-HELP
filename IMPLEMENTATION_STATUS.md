# Implementation Status

This repository is intentionally split between features that work in the packaged Flutter app now and features that require an external service, provider credential, platform signing setup, or additional production engineering.

## Implemented in the current mobile project

- Exact 2,250-question library: 750 trans-men, 750 trans-women, 750 trauma/mental-health.
- Search, section filtering, section hiding, skip / Prefer-not-to-answer metadata and anatomy/topic branching metadata.
- Encrypted local questionnaire answer storage.
- Encrypted measurements, journals, contacts, check-ins, safety plan, goals/tasks and private photo blobs.
- Measurements and longitudinal trend views.
- Transition and mental-health dashboards.
- Fifteen private journal types.
- Trusted contacts with safe-to-contact controls.
- Twenty-part customizable safety plan.
- Crisis Mode and high-risk check-in routing.
- Local bra-size range estimator with data-quality and uncertainty language.
- Local personal measurement trend estimator with limitations and non-guarantee language.
- Optional system photo picker/camera for progress photos; AI analysis and sharing are off by default.
- External AI provider adapter for OpenAI, OpenRouter, Groq, Poe, and custom OpenAI-compatible endpoints.
- Provider model discovery from `/models`, manual model IDs, secure per-provider API-key storage outside normal exports, and real model-request reasoning controls with graceful fallback when a model rejects an effort level.
- Explicit external-AI consent, full-context mode, granular sensitive-data switches, and AI context assembly across saved wellness data.
- Integrated full-data analysis, transition/mental-health summaries, change detection, adjustable trend/projection charts, provider usage display, and AI analysis history.
- Optional user-approved AI journal/goal drafts; AI cannot silently alter medication, contacts, account/admin settings, or destructive controls.
- Optional per-photo multimodal AI analysis with a second confirmation and vision-model capability checks delegated to the provider.
- Trauma-informed psychoeducation library.
- Wellness companion that uses configured external AI/context when enabled and retains a local safety fallback.
- Personalization and accessibility settings.
- Goals, habits and reminder-plan storage.
- Local JSON export and full local-data deletion, including encrypted photo blobs and encryption key.
- Invite-only registration/sign-in UI when the backend is deployed.
- Basic private-community post feed and post creation when signed in.
- XXX/XX invite administration UI.

## Implemented in the packaged FastAPI backend

- Owner bootstrap.
- Exactly 35-character cryptographically random invitations with upper/lowercase letters, digits and symbols.
- Invitation hashes instead of plaintext storage, one-time use, expiration and revocation.
- Invitation-attempt throttling.
- Immutable sequential membership numbers.
- Argon2 password hashing and JWT sessions.
- XXX / XX / X caps of 2 / 3 / 4.
- Profiles, encrypted wellness responses and encrypted social post/message content.
- Posts, comments, reactions, bookmarks.
- Private groups and membership schema/routes.
- Direct messages.
- Reports, moderation actions, appeals and audit records.

## Integration/production work still required

The following items from the master product specification are not honestly claimable as fully production-ready merely by placing source code in a ZIP:

- A hosted HTTPS backend and production database/backups.
- App Store / TestFlight signing and provisioning for iOS; release signing for Play distribution.
- Passkeys, MFA, biometric app unlock, account recovery codes and suspicious-login notification delivery.
- Native scheduled push/local notifications for reminder delivery.
- Full friends/followers, custom audience, group-chat and every social-management screen; the backend supplies several of the underlying primitives but the current mobile UI exposes only the core feed/admin path.
- Cloud object storage, multi-device sync, account migration and encrypted cloud backup.
- Production PDF export and end-user CSV export of all private records.
- Full moderation console, second-review workflow UI, raid automation and production bot-detection service.
- Legal/compliance review, clinical-content review, threat modeling, penetration testing and production incident response appropriate to extremely sensitive health data.

The Codemagic workflows are designed to prove the Flutter project builds before those deployment integrations are added.

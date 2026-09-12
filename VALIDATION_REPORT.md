# Validation Report

## Question-bank integrity

- TRANS MEN: **750/750** questions present (`TM-001` through `TM-750`).
- TRANS WOMEN: **750/750** questions present (`TW-001` through `TW-750`).
- MENTAL HEALTH: **750/750** questions present (`MH-001` through `MH-750`).
- TOTAL: **2,250/2,250** questions present.
- Duplicate IDs: **0**.
- Missing sequence IDs: **0**.
- Duplicate normalized question text: **0**.
- Sections: **25 per questionnaire, 30 questions per section**.
- Every question has an answer type, requirement level, AI-estimate eligibility flag, sensitivity flag, Prefer-not-to-answer flag, units field, help text and branching metadata.
- Sensitive questions: **1,050**; sensitive questions lacking Prefer-not-to-answer support: **0**.
- Safety-critical questions: **30**.

Validated by both `tool/validate_question_bank.py` and the Codemagic-run `tool/validate_question_bank.dart`.

## Security / membership checks

- Invite-only account registration exists.
- Invitation tokens are exactly **35 characters** and are generated with a cryptographic random source.
- Invitation codes include uppercase, lowercase, digits and symbols and are stored by SHA-256 hash rather than plaintext.
- One-time use, expiration and revocation are implemented.
- Immutable membership number format: `MEM-000001`, `MEM-000002`, ...
- Leadership caps: **XXX = 2, XX = 3, X = 4**.
- Backend security smoke test generated a 35-character invite, enrolled `MEM-000002`, authenticated it and created/read a private-community post successfully.
- Backend Python modules compile successfully.

## Repository / Codemagic checks

- `pubspec.yaml` is at repository root.
- `codemagic.yaml` is at repository root and parses with three workflows: Android debug APK, Android release APK/AAB and unsigned iOS compile check.
- `tool/check_repo_layout.sh` passes on the packaged repository.
- Project ZIP is packaged with repository files at archive root rather than inside another enclosing project folder.

## Flutter build limitation in this environment

The current execution environment does not include the Flutter SDK, so `flutter analyze`, `flutter test`, APK compilation and iOS compilation cannot be executed locally here. The Codemagic workflows explicitly run those commands using Codemagic's Flutter environment. This report therefore distinguishes structural/static validation from a completed Flutter compiler build.

# Integrated AI Architecture

## Providers

The mobile app includes provider presets for OpenAI, OpenRouter, Groq, and Poe, plus a custom OpenAI-compatible base URL. API credentials are stored in platform secure storage and deliberately excluded from decrypted JSON/CSV exports and from AI context.

## Model selection

The AI Center can query each provider's `/models` endpoint and also accepts a manually typed model ID. This avoids hard-coding a model catalog that would become stale.

## Reasoning levels

The UI exposes Minimum, Medium, High, X-High, and Maximum. The provider adapter sends a real reasoning-effort parameter through the Responses API. Because support is model-specific, a rejected effort is retried at the nearest lower level. The UI records both the requested and effective effort. It never claims Maximum was used when the provider rejected it.

## Consent and context

External AI is disabled by default. Enabling it requires explicit acknowledgment that selected app data leaves the device and may be logged, retained, exposed, or otherwise processed under the provider's policies. Full context can include questionnaire answers, measurements, check-ins, journals, contacts, safety plan, goals/reminders, AI memory, photo metadata, companion history, and optional cached community history. Authentication secrets, API keys, and invitation credentials are excluded.

## App integration

AI can analyze saved data, summarize changes, explain local trend/projection charts, and propose safe app drafts. Currently supported AI action drafts are journals, goals, reminders, and chart adjustments. Journals/goals/reminders are only written after the user presses Approve. Chart adjustments only change the local projection controls after approval. Medication-dose changes, emergency-contact actions, account/admin changes, invitation actions, and destructive operations are not allowed as AI actions.

## Vision

A progress photo remains encrypted locally unless the user chooses AI analysis. Sending a photo requires the global external-AI consent plus a second per-photo confirmation. The image is decrypted on-device and sent only for that request. The selected model must support vision; otherwise the provider returns an error.

## Medical and crisis boundaries

The AI prompt layer forbids diagnosis from questionnaire data, medication dose changes, self-harm instructions, dangerous weight manipulation, delusion reinforcement, or guaranteed transition/fertility/surgical outcomes. Possible immediate self-harm/suicide danger routes the companion to safety support rather than ordinary analysis.

## Context-size boundary

Full-context mode intentionally sends all selected saved data rather than silently dropping old entries. If a model's context window is too small, the provider can reject the request; the app reports the error so the user can select a larger-context model or narrower data scope.

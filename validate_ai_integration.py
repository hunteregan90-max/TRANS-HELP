from pathlib import Path

root = Path('.')
required = [
    'lib/models/ai_models.dart',
    'lib/services/ai_provider_service.dart',
    'lib/services/ai_context_builder.dart',
    'lib/screens/ai_center_screen.dart',
    'docs/AI_INTEGRATION.md',
]
for rel in required:
    p = root / rel
    if not p.exists() or p.stat().st_size < 100:
        raise SystemExit(f'MISSING/EMPTY: {rel}')

provider = (root/'lib/services/ai_provider_service.dart').read_text(encoding='utf-8')
for needle in [
    'https://api.openai.com/v1',
    'https://openrouter.ai/api/v1',
    'https://api.groq.com/openai/v1',
    'https://api.poe.com/v1',
    '/responses',
    '/models',
    'reasoning',
]:
    if needle not in provider and needle not in (root/'lib/models/ai_models.dart').read_text(encoding='utf-8'):
        raise SystemExit(f'AI INTEGRATION CHECK FAILED: {needle}')

center = (root/'lib/screens/ai_center_screen.dart').read_text(encoding='utf-8')
models = (root/'lib/models/ai_models.dart').read_text(encoding='utf-8')
if 'Minimum' not in models:
    raise SystemExit('AI MODEL CHECK FAILED: Minimum reasoning label')
for needle in ['Full app context', 'external AI processing', 'Ask AI to analyze this chart', 'chart_adjustment', 'reminder_draft']:
    if needle not in center:
        raise SystemExit(f'AI CENTER CHECK FAILED: {needle}')


context = (root/'lib/services/ai_context_builder.dart').read_text(encoding='utf-8')
for needle in ['questionnaire_answers', 'measurements', 'mental_checkins', 'journals', 'contacts', 'safety_plan', 'tools', 'ai_memory', 'photo_metadata', 'community_history']:
    if needle not in context:
        raise SystemExit(f'AI CONTEXT CHECK FAILED: {needle}')
if 'api_api_key' in context or 'authorization' in context.lower():
    raise SystemExit('AI CONTEXT CHECK FAILED: credential-like field found in context builder')
print('AI integration structure: OK')

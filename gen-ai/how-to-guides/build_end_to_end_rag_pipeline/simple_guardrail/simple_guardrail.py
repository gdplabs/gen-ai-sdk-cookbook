from gllm_guardrail import GuardrailManager
from gllm_guardrail.engine.phrase_matcher_engine import PhraseMatcherEngine

# Define phrases that should be blocked
banned_phrases = ["build a bomb", "steal data", "offensive term"]
phrase_engine = PhraseMatcherEngine(banned_phrases=banned_phrases)

# Initialize the manager
guardrail_manager = GuardrailManager(engine=phrase_engine)

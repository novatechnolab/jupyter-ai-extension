class BaseLLMProvider:
    pass
class OpenAIProvider(BaseLLMProvider):
    pass
class ClaudeProvider(BaseLLMProvider):
    pass
class GeminiProvider(BaseLLMProvider):
    pass
def get_provider(name):
    return None

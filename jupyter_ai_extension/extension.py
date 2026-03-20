class JupyterAIExtension:
    def __init__(self):
        self.provider = None
    def configure(self, provider_name, **kwargs):
        self.provider = provider_name
    def generate(self, prompt):
        return f"Response: {prompt}"
    def chat(self, message):
        return f"Chat: {message}"
    def clear_history(self):
        pass

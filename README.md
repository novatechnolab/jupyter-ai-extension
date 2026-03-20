# Jupyter AI Extension

Multi-LLM support for Jupyter notebooks with OpenAI, Claude, and Google Gemini.

## Features

- **Multi-LLM Support**: Works with OpenAI (GPT-4), Anthropic Claude, and Google Gemini
- **Simple Configuration**: One-line setup for each provider
- **Chat & Completion Modes**: Use both conversational and completion APIs
- **Conversation History**: Automatic conversation tracking
- **Customizable Settings**: Control temperature, max tokens, and more
- **Production Ready**: Full error handling and logging

## Installation
```bash
pip install jupyter-ai-extension
```

## Quick Start
```python
from jupyter_ai_extension import JupyterAIExtension

ai = JupyterAIExtension()
ai.configure("openai", api_key="sk-...")
response = ai.generate("Explain machine learning")
print(response)
```

## Configuration

### OpenAI
```python
ai.configure("openai", api_key="sk-...", model="gpt-4-turbo")
```

### Claude
```python
ai.configure("claude", api_key="sk-ant-...", model="claude-opus-4-1")
```

### Gemini
```python
ai.configure("gemini", api_key="AIzaSy...", model="gemini-2.0-flash")
```

## API Methods

- `configure(provider_name, **kwargs)` - Configure the provider
- `generate(prompt)` - Generate text completion
- `chat(message)` - Send chat message
- `clear_history()` - Clear conversation
- `set_settings(**kwargs)` - Customize settings
- `show_settings()` - View current settings
- `list_providers()` - List available providers

## License

MIT License

## Support

GitHub: https://github.com/novatechnolab/jupyter-ai-extension

Made with ❤️ by Nova Technolab

# Copy this file to config.py and fill in your API keys.
# cp config_template.py config.py

openai_key = "your-openai-api-key-here"
anthropic_key = "your-anthropic-api-key-here"

use_key = openai_key
model_config = {
    "gpt-5-nano": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "gpt-5.1": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "gpt-5.2": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "o4-mini": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "o3-mini": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "gpt-4o-mini": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "gpt-4.1-mini": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "gpt-5-mini": {"base_url": "https://api.openai.com/v1", "api_key": use_key},
    "claude-haiku-4-5": anthropic_key,
    "claude-3-5-haiku-latest": anthropic_key,
    "claude-sonnet-4-5": anthropic_key,
    "claude-3-7-sonnet-latest": anthropic_key,
}

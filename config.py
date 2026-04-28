"""
Configuration for Alibaba Coding Plan API concurrent testing.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env (not committed to git)
load_dotenv(Path(__file__).parent / ".env")


def load_alibaba_api_key() -> str:
    """Load BAILIAN_API_KEY from external .env file specified in KEY_SOURCE."""
    key_source = os.environ.get("KEY_SOURCE")
    if not key_source:
        raise ValueError(
            "KEY_SOURCE not set. Copy .env.example to .env and set KEY_SOURCE to the path of your .env file."
        )

    env_path = Path(key_source).expanduser()
    if not env_path.exists():
        raise FileNotFoundError(f"Cannot find .env at {env_path}")

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("BAILIAN_API_KEY="):
                return line.split("=", 1)[1].strip()

    raise ValueError(f"BAILIAN_API_KEY not found in {env_path}")


# API Configuration
OPENAI_COMPATIBLE_BASE_URL = "https://coding-intl.dashscope.aliyuncs.com/v1"
ANTHROPIC_COMPATIBLE_BASE_URL = "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"

# Default to OpenAI-compatible endpoint
API_URL = f"{OPENAI_COMPATIBLE_BASE_URL}/chat/completions"
API_KEY = load_alibaba_api_key()

# Test Configuration
CONCURRENCY_LEVEL = 10  # Number of concurrent requests
TOTAL_REQUESTS = 100    # Total number of requests to send
TIMEOUT_SECONDS = 30    # Request timeout in seconds

# Available Models
AVAILABLE_MODELS = [
    # Qwen
    "qwen3.6-plus",
    "qwen3.5-plus",
    "qwen3-max-2026-01-23",
    "qwen3-coder-next",
    "qwen3-coder-plus",
    # Zhipu
    "glm-5",
    "glm-4.7",
    # Kimi
    "kimi-k2.5",
    # MiniMax
    "MiniMax-M2.5",
]

# Default test model
TEST_MODEL = "qwen3.6-plus"

# Request Payload (customize as needed)
DEFAULT_PAYLOAD = {
    "model": TEST_MODEL,
    "messages": [
        {"role": "user", "content": "Say hello"}
    ]
}

# Headers (customize as needed)
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

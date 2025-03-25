import os

app_config = {
    "chat_client": os.getenv("CHAT_CLIENT", "mock"),
    "storage_dir": os.getenv("STORAGE_DIR", "storage"),
    "chat_config": {
        "enabled": os.getenv("CHAT_ENABLED", True),
        "prompt": os.getenv("CHAT_PROMPT", ""),
        "pre_prompt_query": os.getenv("CHAT_PRE_PROMPT_QUERY", ""),
        "prompt_query": os.getenv("CHAT_PROMPT_QUERY", ""),
        "pre_prompt_summary": os.getenv("CHAT_PRE_PROMPT_SUMMARY", ""),
        "prompt_summary": os.getenv("CHAT_PROMPT_SUMMARY", ""),
    },
    "relatorios": os.getenv(
        "RELATORIOS",
        "informacoes_viagem_detalhada,roteiro_viagem",
    ),
}

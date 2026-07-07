records = [
    {
        "name": "router",
        "model_id": "openai/gpt-4.1-nano",
        "credentials": "env:OPENAI_API_KEY",
        "config": {
            "default_hyperparameters": {
                "temperature": 0.7,
                "max_output_tokens": 100
            }
        },
        "system_template": "You are an AI expert.\nYour job is to define which use case is the most suitable for the user query.\nUse case options:\n1. \"qa\": Question answering.\n2. \"sum\": Summarization.\n3. \"dd\": Document drafting.",
        "user_template": "Below is the user query:\n{query}",
        "prompt_builder_kwargs": {"use_jinja": False},
        "output_parser_type": "none"
    },
    {
        "name": "chat_with_history",
        "model_id": "openai/gpt-4.1-nano",
        "credentials": "raw:your_api_key_here",
        "config": {
            "default_hyperparameters": {
                "temperature": 0.7,
                "max_tokens": 500
            }
        },
        "system_template": "You are a helpful AI assistant. Continue the conversation based on the chat history provided.",
        "user_template": "{{ history }}\n\n{{ message }}",
        "prompt_builder_kwargs": {
            "use_jinja": True,
            "jinja_env": "restricted",
            "history_formatter": {
                "prefix_user_message": "<user>",
                "suffix_user_message": "</user>",
                "prefix_assistant_message": "<assistant>",
                "suffix_assistant_message": "</assistant>"
            }
        },
        "output_parser_type": "none"
    }
]

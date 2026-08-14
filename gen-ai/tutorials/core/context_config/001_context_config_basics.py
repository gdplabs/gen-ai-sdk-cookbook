"""Demonstrate ContextConfig construction and portable placeholder rendering.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/context-config#the-contextconfig-schema
"""

from gllm_core.schema import ContextConfig


def main() -> None:
    """Build a ContextConfig and render payloads using portable placeholders."""
    # Defaults: fields=['metadata'], metadata_keys=None, template='{context_json}'
    default = ContextConfig()
    print("fields:", default.fields)  # ['metadata']
    print("metadata_keys:", default.metadata_keys)  # None
    print("template:", default.template)  # {context_json}
    print(default.render({"content": "text", "metadata": {"source": "docs"}}))
    # {
    #   "metadata": {
    #     "source": "docs"
    #   }
    # }

    # Explicit fields + metadata_keys + a custom template with portable placeholders.
    config = ContextConfig(
        fields=["content", "metadata"],
        metadata_keys=["source"],
        template="Content: {content}\nMetadata: {metadata_json}",
    )
    payload = {"content": "receipt", "metadata": {"source": "docs", "internal": True}}
    print(config.render(payload))
    # Content: receipt
    # Metadata: {
    #   "source": "docs"
    # }
    # `internal` is dropped: it is not in metadata_keys.


if __name__ == "__main__":
    main()

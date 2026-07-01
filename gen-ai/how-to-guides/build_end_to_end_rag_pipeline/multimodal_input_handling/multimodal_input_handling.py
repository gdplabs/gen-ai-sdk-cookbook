from gllm_inference.schema import MessageContent

class MultimodalRAGState(RAGState):
    attachments: list[str]
    extra_contents: list[MessageContent]

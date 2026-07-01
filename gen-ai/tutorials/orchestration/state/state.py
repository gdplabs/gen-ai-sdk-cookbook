class RAGState(TypedDict):
    user_query: str
    queries: list[str]
    retrieval_params: dict[str, Any]
    chunks: list
    history: str
    context: str
    response: str
    references: str | list[str]
    event_emitter: EventEmitter

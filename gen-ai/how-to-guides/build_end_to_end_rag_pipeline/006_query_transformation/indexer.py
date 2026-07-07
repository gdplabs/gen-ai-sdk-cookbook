class CustomRAGState(RAGState):
    original_query: str
    transformed_query: str
    query_intent: str

def intent_aware_query_transformer():
    """Transforms queries based on detected intent."""
    intent_detector = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Classify the intent of this query as: factual, comparative, procedural, or exploratory. Output only the classification.",
        user_template="Query: {query}",
    )

    query_rewriter = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Rewrite this {intent} query for optimal document retrieval.",
        user_template="Query: {query}",
    )

    return OneToOneQueryTransformer(lm_request_processor=query_rewriter)

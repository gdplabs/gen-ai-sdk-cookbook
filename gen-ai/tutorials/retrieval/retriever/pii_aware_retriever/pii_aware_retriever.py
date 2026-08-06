retriever = PIIAwareRetriever(
    data_store=data_store,
    pii_resolver=pii_resolver,
    weights=[0.7, 0.3]  # 70% vector, 30% entity-filtered
)

results = await retriever.retrieve(
    "Find documents about Alice Smith",
    top_k=10,
    threshold=0.7
)

ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, fulltext_retriever],
    weights=[0.6, 0.4],          # Custom weights (auto-normalized)
    rank_constant=60,            # Controls balance between high and low-ranked items
    min_candidate=2              # Minimum results per retriever before fusion
)

results = await ensemble_retriever.retrieve(
    "query",
    top_k=10,
    threshold=0.7
)

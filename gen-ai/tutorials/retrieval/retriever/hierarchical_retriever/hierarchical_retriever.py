config = HierarchicalRetrieverConfig(
    levels=[
        LevelConfig(
            name="corpus",
            retriever=corpus_retriever,
            top_k=3,
            filter_key="corpus_id",
            constrain_by=None
        ),
        LevelConfig(
            name="document",
            retriever=document_retriever,
            top_k=5,
            filter_key="corpus_id",
            constrain_by=ConstraintMode.PREVIOUS
        ),
        LevelConfig(
            name="section",
            retriever=section_retriever,
            top_k=8,
            filter_key="document_id",
            constrain_by=ConstraintMode.PREVIOUS
        ),
        LevelConfig(
            name="chunk",
            retriever=chunk_retriever,
            top_k=10,
            filter_key="section_id",
            constrain_by=ConstraintMode.PREVIOUS
        )
    ],
    output_level="chunk",
    final_top_k=10  # Cap final results
)

retriever = HierarchicalRetriever(config=config)
results = await retriever.retrieve("query", top_k=10)

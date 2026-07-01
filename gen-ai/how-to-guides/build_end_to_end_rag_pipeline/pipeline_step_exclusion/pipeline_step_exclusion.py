from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

# Create a simple document processing pipeline
pipeline = Pipeline([
    step(DocumentExtractor(), {"document": "input_document"}, "extracted_text", name="extract"),
    step(SentimentAnalyzer(), {"text": "extracted_text"}, "sentiment_score", name="sentiment"),
    step(TopicDetector(), {"text": "extracted_text"}, "detected_topics", name="topics"),
    step(ReportGenerator(), {
        "sentiment": "sentiment_score",
        "topics": "detected_topics"
    }, "analysis_report", name="report")
])

# Execute with all steps
result = await pipeline.invoke({"input_document": "Sample document content"})
print("Full pipeline result:", result)

# Exclude the sentiment analysis step
pipeline.exclusions.exclude("sentiment")
result_no_sentiment = await pipeline.invoke({"input_document": "Sample document content"})
print("Without sentiment:", result_no_sentiment)
# Note: sentiment_score will not be present in the result

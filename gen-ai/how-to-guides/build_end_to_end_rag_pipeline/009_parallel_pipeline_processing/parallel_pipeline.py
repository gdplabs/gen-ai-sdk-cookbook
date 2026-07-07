from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

# PROBLEM: Sequential execution creates unnecessary bottlenecks
sequential_pipeline = Pipeline([
    step(DocumentExtractor(), {"document": "input_document"}, "extracted_text"),

    # These operations are INDEPENDENT but run sequentially (inefficient!)
    step(SentimentAnalyzer(), {"text": "extracted_text"}, "sentiment_score"), 
    step(TopicDetector(), {"text": "extracted_text"}, "detected_topics"), 
    step(EntityExtractor(), {"text": "extracted_text"}, "named_entities"),
    step(LanguageDetector(), {"text": "extracted_text"}, "language_info"),

    step(ReportGenerator(), {
        "sentiment": "sentiment_score",
        "topics": "detected_topics",
        "entities": "named_entities",
        "language": "language_info"
    }, "analysis_report")
])

# Problem: Each analysis waits for the previous one despite being independent!

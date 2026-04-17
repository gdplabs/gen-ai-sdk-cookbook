# Custom Evaluator / Scorer Tutorial

This is a production-ready example demonstrating how to create a custom evaluator and metric for evaluating customer complaint summaries using LLM-as-a-Judge.

## Use Case

This example evaluates the correctness of generated summaries from customer complaint texts. Specifically, it checks if a generated summary:
- Accurately represents the customer's complaint
- Contains no hallucinations or contradictions
- Preserves the factual meaning of the original complaint
- Contains key information (action, object, channel/app, etc.)

## Quick Start

### 1. Install Dependencies

```bash
make install
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY
```

### 3. Run the Evaluation

```bash
make run
```

This will:
1. Load test data from `tsel_test_data.csv`
2. Evaluate each row using the custom evaluator
3. Export results to `final_results_detail_case_gangguan_correctness.csv`
4. Calculate and print the alignment score between LLM-as-a-judge and ground truth

## Project Structure

```
custom_evaluator_scorer_tutorial/
├── main.py                                          # Entry point - runs evaluation on CSV data
├── custom_detail_case_gangguan_correctness_evaluator.py  # Custom Evaluator
├── custom_detail_case_gangguan_correctness_metric.py      # Custom Metric (DeepEvalGEvalMetric)
├── evaluation_steps.py                            # Evaluation prompts/steps for LLM judge
├── tsel_test_data.csv                              # Test data
└── final_results_detail_case_gangguan_correctness.csv   # Output (generated after running)
```

## How It Works

### 1. Custom Metric

The `CustomDetailCaseGangguanCorrectnessMetric` extends `DeepEvalGEvalMetric` to use LLM-as-a-Judge for evaluation:

```python
class CustomDetailCaseGangguanCorrectnessMetric(DeepEvalGEvalMetric):
    def __init__(
        self,
        model_credentials: str,
        evaluation_steps: list[str],
        threshold: float = 0.5,
    ):
        super().__init__(
            name="detail_case_gangguan_correctness",
            model_credentials=model_credentials,
            evaluation_steps=evaluation_steps,
            threshold=threshold,
        )
```

### 2. Custom Evaluator

The `CustomDetailCaseGangguanCorrectnessEvaluator` wraps the metric:

```python
class CustomDetailCaseGangguanCorrectnessEvaluator(BaseEvaluator):
    def __init__(self, model_credentials: str, threshold: float = 0.5):
        super().__init__(name="custom_detail_case_gangguan_correctness_evaluator")
        self.metric = CustomDetailCaseGangguanCorrectnessMetric(
            model_credentials=model_credentials,
            evaluation_steps=CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS,
            threshold=threshold,
        )

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        return await self.metric.evaluate(data)
```

### 3. Evaluation Steps

The `evaluation_steps.py` file contains the detailed prompts that guide the LLM judge on how to evaluate summaries. Key criteria include:

- **Extraction**: Check if summary contains action + object from the complaint
- **Consistency**: Intent type and channel/app must stay consistent
- **Keyword matching**: Special handling for "AO Keyword" patterns
- **Groundedness**: All information must be found in or supported by the query
- **No contradictions**: Summary must not introduce new facts or reverse polarity
- **Conciseness**: Short but accurate summaries are acceptable

### 4. Running Evaluation

The `main.py` script:

```python
# Initialize evaluator
evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(
    model_credentials=os.getenv("GOOGLE_API_KEY"),
    threshold=0.75,
)

# Load data from CSV
df = pd.read_csv("tsel_test_data.csv")
dataset = df.to_dict(orient="records")

# Evaluate each row
for row in dataset:
    data = QAData(
        query=row["detailed_decription"],
        generated_response=row["detail_case_gangguan"],
    )
    result = await evaluator.evaluate(data)
    # Store results...
```

## Output Format

The evaluator returns:

```python
{
    "custom_detail_case_gangguan_correctness_evaluator": {
        "detail_case_gangguan_correctness": {
            "score": 1,  # 0 or 1
            "explanation": "Detailed explanation from LLM judge"
        }
    }
}
```

## Alignment Score

After evaluation, the script calculates the alignment between LLM-as-a-judge and ground truth scores:

```
Alignment score: 85.5%
```

This indicates how well the LLM judge aligns with human evaluation.

## Key Concepts

### Extending DeepEvalGEvalMetric

For LLM-as-a-judge metrics, extend `DeepEvalGEvalMetric`:

```python
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric

class MyMetric(DeepEvalGEvalMetric):
    def __init__(self, model_credentials: str, evaluation_steps: list[str]):
        super().__init__(
            name="my_metric",
            model_credentials=model_credentials,
            evaluation_steps=evaluation_steps,
            threshold=0.5,
        )
```

### Evaluation Steps

Well-defined evaluation steps are crucial for consistent LLM-as-a-judge evaluation:

1. Define clear criteria for scoring
2. Provide examples of what constitutes good vs bad outputs
3. Handle edge cases explicitly
4. Specify how to handle special patterns (keywords, technical terms, etc.)

### Input Data Format

The CSV file should contain columns:
- `no` - Row identifier
- `detailed_decription` - The original complaint (query)
- `detail_case_gangguan` - The generated summary to evaluate
- `score_detail_case_gangguan` - Ground truth score for alignment calculation

## Available Make Commands

```bash
make install    # Install dependencies
make run        # Run the evaluation
make clean      # Clean up generated files
```

## Production Tips

1. **Define clear evaluation steps** - The quality of LLM-as-a-judge depends on well-defined prompts
2. **Set appropriate thresholds** - Adjust based on your tolerance for false positives/negatives
3. **Validate against ground truth** - Calculate alignment scores to measure LLM judge performance
4. **Handle edge cases** - Explicitly specify how to handle keywords, short inputs, etc.
5. **Use appropriate models** - Larger models generally provide more consistent evaluations

## Further Reading

- [Getting Started](../getting_started/) - Basic evaluation concepts
- [Create Custom Evaluator](../create_custom_evaluator_scorer/) - Basic custom evaluator guide
- [Multiple LLM-as-a-Judge](../multiple_llm_as_a_judge/) - Using multiple judges for better alignment

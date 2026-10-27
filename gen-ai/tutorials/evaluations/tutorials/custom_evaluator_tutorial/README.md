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
custom_evaluator_tutorial/
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
        models: BaseLMInvoker | list[BaseLMInvoker] | None = None,
        criteria: str | None = None,
        evaluation_steps: list[str] | None = None,
        threshold: float = 0.5,
        evaluation_params: list[LLMTestCaseParams] | None = None,
    ):
        super().__init__(
            name="detail_case_gangguan_correctness",
            models=models,
            criteria=criteria,
            evaluation_steps=evaluation_steps,
            threshold=threshold,
            evaluation_params=evaluation_params
            or [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        )

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        output = await super()._evaluate(data)
        output.score = int(output.score)
        return output
```

### 2. Custom Evaluator

The `CustomDetailCaseGangguanCorrectnessEvaluator` wraps the metric:

```python
class CustomDetailCaseGangguanCorrectnessEvaluator(BaseEvaluator):
    def __init__(
        self,
        models: BaseLMInvoker | list[BaseLMInvoker] | None = None,
        threshold: float = 0.5,
    ):
        super().__init__(name="custom_detail_case_gangguan_correctness_evaluator")
        self.metric = CustomDetailCaseGangguanCorrectnessMetric(
            models=models,
            evaluation_steps=CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS,
            threshold=threshold,
        )

    async def _evaluate(self, data: LLMTestCase) -> EvaluatorResult:
        return {self.metric.name: await self.metric.evaluate(data)}
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
# Initialize the evaluator with a Gemini judge
invoker = build_lm_invoker(
    model_id="google/gemini-3-flash-preview",
    credentials=os.getenv("GOOGLE_API_KEY"),
)
evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(models=invoker, threshold=0.75)

# Load the CSV; each row is an LLMTestCase, and the CSV columns are extra fields
dataset = DictDataset.from_csv("tsel_test_data.csv").load()

# Evaluate each row
for row in dataset:
    data = LLMTestCase(
        input=row.detailed_description,
        actual_output=row.detail_case_gangguan,
    )
    result = await evaluator.evaluate(data)
    metric_result = result[evaluator.name].model_extra["detail_case_gangguan_correctness"]
    # Store metric_result.score and metric_result.explanation...
```

## Output Format

The evaluator returns a dict that maps the evaluator name to an `EvaluatorOutput`. The metric result is an extra field of that output:

```python
{
    "custom_detail_case_gangguan_correctness_evaluator": EvaluatorOutput(
        aggregate_success=...,
        aggregate_score=...,
        aggregate_explanation=...,
        detail_case_gangguan_correctness=MetricResult(score=1, explanation="...", ...),  # score is 0 or 1
    )
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
    def __init__(self, models: BaseLMInvoker | None = None, evaluation_steps: list[str] | None = None):
        super().__init__(
            name="my_metric",
            models=models,
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
- `detailed_description` - The original complaint (query)
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

- [Getting Started](../../getting_started/) - Basic evaluation concepts
- [Create Custom Evaluator](../../evaluator/create_custom_evaluator/) - Basic custom evaluator guide
- [Multiple LLM-as-a-Judge](../../multiple_llm_as_a_judge/) - Using multiple judges for better alignment

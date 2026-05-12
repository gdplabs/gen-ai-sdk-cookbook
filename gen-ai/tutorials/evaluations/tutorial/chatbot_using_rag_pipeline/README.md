## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/tutorial/chatbot_using_rag_pipeline
   ```

2. **Set UV authentication and install dependencies**

   ```bash
   make sync
   ```

   This will authenticate with Google Cloud and install all dependencies via UV.

3. **Prepare `.env` file**  
    Create a file called `.env`, then set the Google API key for the judge model.
    ```env
    GOOGLE_API_KEY="..."
    ```

4. **Run the evaluation**

   ```bash
   make run-eval
   ```

5. **Expected Output**

   The script runs all 3 test cases from `data/eval_dataset.csv`, evaluates each with a Gemini judge, and prints an `ExperimentResult` dict. Results are also saved to `results/` by `CSVExperimentTracker`.

   ```log
   {'run_id': 'rag-chatbot-eval_...', 'num_samples': 3, 'results': [[{'generation': {'aggregate_success': False, 'aggregate_score': 0.83, 'completeness': {'score': 0.5, 'success': False, 'threshold': 1.0, ...}, 'groundedness': {'score': 1.0, 'success': True, ...}, 'redundancy': {'score': 0.0, 'success': True, ...}}}], [{'generation': {'aggregate_success': True, ...}}], [{'generation': {'aggregate_success': True, ...}}]], 'experiment_uris': {'run_uri': 'results/experiment_results.csv', 'leaderboard_uri': 'results/leaderboard.csv'}, ...}
   ```

   Full per-case results with judge explanations are saved to:
   - `results/experiment_results.csv` — one row per test case
   - `results/leaderboard.csv` — one row per run (for tracking improvement across runs)

6. **(Optional) Run the calibrated evaluation**

   Case 1 uses a broad browse query ("Give me nocturnal creatures"). After SME review, the domain expert confirmed that partial coverage (≥ 50%) is sufficient for this query type. `eval_calibrated.py` reflects that decision by splitting evaluation into two calls: Case 1 with `completeness` threshold lowered to `0.5`, and Cases 2–3 evaluated at the default strict threshold (`1.0`):

   ```bash
   make run-eval-calibrated
   ```

   With the calibrated threshold, Case 1 (`completeness score = 0.5`) now passes. Cases 2 and 3 are unaffected — their metrics use the default thresholds.

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation Evals Lifecycle page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle).

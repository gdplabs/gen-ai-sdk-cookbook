## ⚙️ Prerequisites

Please refer to prerequisites [here](../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/database_backed_checkpointing
   ```

2. **Set UV authentication and install dependencies**

   **For Unix-based systems (Linux, macOS):**
   ```bash
   ./setup.sh
   ```

   **For Windows:**
   ```cmd
   setup.bat
   ```

3. **Run the example**

   ```bash
   uv run checkpoint_to_datastore.py
   ```

4. **Expected Output**

   ```text
   Paused draft: Draft about: Quarterly earnings report
   Next node: ('wait_for_human',)
   Approved: True
   Checkpoint history length: 4
     checkpoint: <checkpoint_id> {'topic': 'Quarterly earnings report', 'draft': 'Draft about: Quarterly earnings report', 'approved': True}
     checkpoint: <checkpoint_id> {'topic': 'Quarterly earnings report', 'draft': 'Draft about: Quarterly earnings report'}
     checkpoint: <checkpoint_id> {'topic': 'Quarterly earnings report'}
     checkpoint: <checkpoint_id> {}
   fork_from: skipped — DataStoreSaver has not implemented get_tuple in the installed gllm-pipeline release; see GitBook guide section 4 for the reference API.
   delete_thread: skipped — not implemented by DataStoreSaver in the installed release (GitBook guide section 5 references it).
   ```

   > **Note:** The durable human-in-the-loop core (invoke → pause at `interrupt` →
   > `get_state` → `get_state_history` → resume) runs fully against an
   > `InMemoryDataStore`. The published `DataStoreSaver` (gllm-pipeline 0.5.20)
   > does not yet implement `get_tuple` (needed by `fork_from`) or `delete_thread`,
   > so those two calls degrade gracefully with a printed skip message until a
   > `DataStoreSaver` release ships them. See GitBook sections 4 and 5 for the
   > reference API.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/database-backed-checkpointing).

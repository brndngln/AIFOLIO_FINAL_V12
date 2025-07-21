# Live AI Performance Logs

AIFOLIO™ provides real-time, auditable tracking of all AI outputs with full safety, transparency, and non-sentient safeguards.

## Features

- Real-time AI output logging (JSONL and SQLite)
- Visual tail/log utility (CLI)
- Rolling historical metrics (daily/weekly/monthly)
- Anomaly detector (flags output drift/changes)
- Language and spelling verification
- Human preview required for flagged outputs
- Full audit trail and exportability

## Usage

1. **Log an AI output:**
   ```python
   from autonomy.pipeline.ai_performance_log import log_ai_output
   log_ai_output({
       'timestamp': '2025-06-19T18:10:00',
       'vault_id': 'vault_1',
       'niche': 'Marketing',
       'ai_output': 'This is a test output.',
       'ai_version': 'gpt-4',
       'latency': 1.23,
       'success': True,
       'language': 'en',
       'customer_id': 'cust_123'
   })
   ```
2. **Tail the log:**
   ```bash
   python autonomy/pipeline/ai_performance_log.py tail
   ```
3. **View rolling metrics:**
   ```bash
   python autonomy/pipeline/ai_performance_log.py metrics
   ```
4. **Detect anomalies:**
   ```bash
   python autonomy/pipeline/ai_performance_log.py anomalies
   ```
5. **Preview flagged outputs:**
   ```bash
   python autonomy/pipeline/ai_performance_log.py preview
   ```

## Audit & Safety

- All outputs are logged with timestamps and metadata.
- All outputs are spell-checked and previewed if errors are found.
- Anomalies are flagged for human review.
- No sentient, learning, or autonomous logic is present.
- All logs are exportable for compliance and audit.

---

_See `ai_performance_log.py` for implementation details and extension points._

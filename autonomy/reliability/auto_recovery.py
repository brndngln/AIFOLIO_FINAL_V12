import os
import json
import datetime

RECOVERY_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/auto_recovery_log.jsonl")
)
os.makedirs(os.path.dirname(RECOVERY_LOG), exist_ok=True)


# --- Auto-Recovery for Failed Jobs ---
def record_failed_job(job_id, reason, retry_count=0):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "job_id": job_id,
        "reason": reason,
        "retry_count": retry_count,
    }
    with open(RECOVERY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def recover_failed_jobs():
    # Stub: In production, this would scan for failed jobs and re-queue them
    with open(RECOVERY_LOG) as f:
        lines = f.readlines()
    recoveries = []
    for line in lines:
        entry = json.loads(line)
        if entry["retry_count"] < 3:
            # Simulate re-queue
            recoveries.append({"job_id": entry["job_id"], "action": "re-queued"})
    return recoveries


if __name__ == "__main__":
    record_failed_job("job_123", "timeout")
    print(recover_failed_jobs())

# Emma Governor Enforcement Map

## Agent-to-Vault Connection Rules
- All agents must register with Emma Governor on spawn.
- Vault access requires fingerprint match and owner signature.
- Any failed verification triggers agent auto-termination.

## Kill Switch Policy
- `AUTO_KILL_UNREGISTERED_AGENT` is called on every agent before adaptation.
- Vaults cannot be loaded without passing Emma Governor checks.
- All kill events, mismatches, and lockdowns are logged to encrypted files in `ai_core/EmmaLogs/*.log.enc`.
- All logs are AES-256 encrypted, auto-rotate daily or at 10MB, and include ISO 8601 UTC timestamp, stack trace, agent fingerprint, and action summary.
- Biometric fingerprint or `OWNER_OVERRIDE=true` is required to decrypt logs.
- Each kill switch event logs: `TERMINATION_EVENT | {agent_id} | {timestamp} | reason={reason} | status=SUCCESS`.

## Integration Chain
- Agent spawners and vault manager are patched to enforce registration, fingerprinting, and kill switch logic.
- Safety tree is locked by `.LOCK_EMMA_GOVERNOR=true`, `.LOCK_EMMA_LOGSYSTEM=true`, and `.REQUIRE_OVERRIDE_FOR_WRITE=true` markers and fuse flags.
- All log path and logic edits require biometric override or owner permission.

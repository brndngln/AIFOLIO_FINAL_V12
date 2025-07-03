# Emma Governor Enforcement Map

## Agent-to-Vault Connection Rules
- All agents must register with Emma Governor on spawn.
- Vault access requires fingerprint match and owner signature.
- Any failed verification triggers agent auto-termination.

## Kill Switch Policy
- `AUTO_KILL_UNREGISTERED_AGENT` is called on every agent before adaptation.
- Vaults cannot be loaded without passing Emma Governor checks.
- All kill events, mismatches, and lockdowns are logged to `/core/EmmaLogs/`.

## Integration Chain
- Agent spawners and vault manager are patched to enforce registration, fingerprinting, and kill switch logic.
- Safety tree is locked by `.LOCK_EMMA_GOVERNOR=true` marker and fuse flag.

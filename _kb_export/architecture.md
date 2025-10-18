# AIFOLIO Architecture (High-Level)
- Monorepo layout: apps/, packages/, services/, docs/
- Core services (examples): auth, kb-export, pdf-engine, scheduler, analytics
- Data flow: client -> API gateway -> service -> persistence -> events/queue
- Tech: <list your frameworks/runtimes/dbs>
- Key conventions: Type-safe APIs, env via Doppler, non-sentient AI (one-shot calls only)

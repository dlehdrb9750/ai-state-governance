# Design Decisions

**DD-001 — Separate owner authority from infrastructure.** A writer or storage provider cannot unilaterally define whose conclusions are authoritative. An explicit owner-specific selector remains necessary.

**DD-002 — Prefer a small native Git publication boundary.** Stage related artifacts together when they must agree; check the intended parent/ref and read back. Avoid building a second database or mandatory receipt ledger when Git history and a small scope pointer suffice.

**DD-003 — Avoid obligatory double recovery.** If the original attempt was never accepted and its objective can be fulfilled by a new meaningful attempt, preserve the objective. Buffer only irreplaceable or otherwise useful material. Do not create a permanent remediation queue by default.

**DD-004 — Explicitly model staging, publication, readback and substantive admission.** These are four distinct claims, each with independent evidence. The example only accepts after a flag explicitly represents owner authorization.

**DD-005 — Minimize false promises.** A deterministic digest is not a cryptographic attestation of the publisher, and an in-memory compare-and-check is not distributed CAS. Do not infer production reliability from eight passing toy tests.

**DD-006 — Publish a clean-room teaching implementation.** The example uses generic fictional owner names, does not reproduce internal repository history, and has no private dependency.

## Candidate alternatives

| Alternative | Rationale for not making it the default |
| --- | --- |
| Every run writes a receipt and separate checkpoint | Unneeded writes and reconciliation costs for simple jobs. |
| Every failed draft is saved and later re-executed | Causes duplicate work when the real objective can be fulfilled without it. |
| Highest timestamp wins | Cannot establish authority from timestamps or file existence. |
| Local test model treated as production integration | Overstates distributed semantics and security guarantees. |
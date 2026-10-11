# Limitations and Verification

## What can be verified publicly

Eight included tests check the local educational model:

1. Prepared candidates are not published or accepted automatically.
2. Publication does not imply acceptance.
3. Owner approval and exact readback matching are required to accept.
4. An outdated candidate cannot replace a changed head.
5. Preparation from a stale base is rejected.
6. An optional recovery packet never mutates accepted state.
7. Unpublished state fails a head readback check.
8. Separate owners maintain separate accepted pointers.

Run `python -m unittest discover -s tests -v` from this directory.

## Not covered

- No GitHub remote API integration, authorization token flow or hosted repository writes.
- No operating-system-level file durability, crash consistency, distributed locks or strong compare-and-swap semantics.
- No cryptographic proof of who approved a result; `approved=True` is a **simulation**, not an access control mechanism.
- No networking, cross-session checkpoints, production recovery buffers, or real automated research runner.
- No guarantees about factual correctness of any research output.
- No GitHub Actions test workflow in this initial package.

## Security posture

No secrets, private research, real configuration values, internal source IDs or account-specific data belong in this package. Publishing example code should not be confused with permission to operate someone else's resources.

## Future evidence

A later independent release could integrate a disposable Git repository, test racing writers, validate durable readback, and demonstrate reconciliation under controlled failure injection. Those capabilities are explicitly future work and are not claimed here.
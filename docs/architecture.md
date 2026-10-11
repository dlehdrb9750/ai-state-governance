# Architecture: State, Publication and Acceptance

## Terminology

| Layer | Question | Allowed transitions |
| --- | --- | --- |
| Intent / work | What should happen next? | May evolve under the approved task scope. |
| Prepared candidate | What material has been constructed? | Draft or immutable candidate; **not authoritative**. |
| Published artifact | What version is visible at the selected branch? | Publication must match the intended base and be read back. |
| Accepted frontier | What version did the responsible owner admit? | Moves only after scope-specific verification and authorization. |
| Recovery packet | Is a useful unsuccessful attempt retained? | Optional, explicitly noncanonical; may be reconciled later. |

**Accepted ≠ buffered ≠ next action.** These may refer to different pieces of work; the normal path does not need mandatory duplicate counters.

## Example workflow

```text
User-approved objective
      |
      v
   Candidate ----> [prepare / base observed]
      |
      v
   Publish ------> [head changes only if expected base still matches]
      |
      v
   Read back ----> [verify ref, identity, owner and content]
      |
      v
   Owner accepts  [separate decision]
      |
      v
Accepted frontier

   rejected/stale material ---> [optional unaccepted recovery packet]
```

One branch can hold interleaved commits for multiple owner scopes. A published Git commit by itself does not create an accepted result for each owner.

## Recovery

1. When publication is uncertain, **read the current state first** rather than assuming success or failure.
2. Identify the affected artifact and error type. Do not treat one provider error as a global failure.
3. On a stale base, derive a new candidate from the current head or reconcile explicitly; do not overwrite silently.
4. When the original artifact has no unique recovery value, the approved objective may be continued with a new, substantively useful work batch instead of retaining every unsuccessful draft.
5. Retain a recovery packet only when warranted by provenance, obligations, irreproducibility or real downstream use. Such a packet remains unaccepted.
6. Never treat a tool/permission refusal as permission to defeat that control. Changes must remain within applicable permissions and policies.

## How the example maps to reality

The Python model uses a **single-process synchronous variable** as its branch head. Git hosting needs actual authentication, conditional update semantics as provided by the chosen API, reconciliation rules, and a fresh independent readback. This model is suitable for teaching state distinctions and stale-base detection, not deploying as a remote multi-writer service.
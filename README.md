# AI State Governance

**DLS — AI State & Data Governance Architecture**

**Version:** 0.1.0 · **Maturity:** Public reference architecture + educational prototype · **Repository:** Standalone public release

> This is an **independently written public reference**, not the text of an internal operational standard or an active canonical-state router.

## What problem does it solve?

A long-running AI workflow needs to answer four different questions: **What is authoritative? What was executed? What was actually persisted and read back? What could be recovered later?** Treating any two as interchangeable creates errors when tools fail, work spans sessions, or state moves between providers.

## Core ideas

| Principle | Meaning |
| --- | --- |
| Authority ≠ execution route ≠ buffer location | Where content was produced or temporarily stored does not decide its canonical authority. |
| One accepted frontier per owner scope | An owner/scope has one accepted pointer, while multiple unpublished candidates may exist. |
| Prepared ≠ published ≠ accepted | Creating a candidate, moving a branch, verifying the data and authorizing it are separate events. |
| Readback before claims | A tool success message alone is not proof that the expected content is visible at the intended ref. |
| Recovery is selective | Valuable unaccepted material can be buffered; a retry packet does not automatically become canonical. |

## Run the synthetic demonstration

Only **Python 3.9+**, using standard-library modules:

```bash
python examples/state_demo.py
python -m unittest discover -s tests -v
```

The code simulates an in-memory branch and owner decisions. It deliberately has **no live GitHub API access, tokens, file writes or external side effects**. The demo prints an accepted candidate, rejects a stale proposal, and shows a noncanonical recovery packet.

## Browse

- [Architecture and state transitions](docs/architecture.md)
- [Decisions and practical tradeoffs](docs/design-decisions.md)
- [Limits, threats and verification scope](docs/limitations.md)
- [Python demonstration](examples/state_demo.py) · [tests](tests/test_state_demo.py)
- [Release notes](CHANGELOG.md)

## Evidence and scope

**Internal observation:** Verified Git-based artifact publishing/readback and evolving governance contracts informed this public design. These records are not publicly replicated here.

**Public evidence:** Eight standard-library tests are included and can be independently inspected and run. Passing them proves only the behaviors of this teaching model, not production GitHub integration.

**Not claimed:** A production-ready repository integration, distributed transactional guarantee, automatic authority transfer, end-to-end scheduler reliability, or a complete security model.

**Relationship:** [AI Systems Portfolio](https://github.com/dlehdrb9750/ai-systems-portfolio) · [Public disclosure policy](https://github.com/dlehdrb9750/ai-systems-portfolio/blob/main/publication-policy.md). The operational source of authority remains private and independent; this repo does not mirror it.

**License:** No open-source license has been selected; viewing public source does not imply unrestricted reuse.

## Independence

This repository starts from a new public commit history. It contains a general-purpose example with fictional identifiers, not a copy of any internal research or operational repository. Its releases have no effect on real projects' accepted state or execution routing.

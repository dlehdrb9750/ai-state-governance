"""A tiny, in-memory teaching model of publishing versus accepting state.

This is NOT a Git client, distributed compare-and-swap primitive, or storage SDK.
All content is synthetic; no credentials, network access or external packages.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Dict, Optional


class StateConflict(Exception):
    """The expected base or published state did not match."""


class VerificationError(Exception):
    """The proposed result failed readback or integrity verification."""


class ApprovalRequired(Exception):
    """Only an explicitly authorized caller may accept canonical state."""


@dataclass(frozen=True)
class Candidate:
    owner: str
    parent: Optional[str]
    payload: str
    checksum: str


class EducationalLedger:
    """A synchronous, process-local model for a single publishing branch.

    The ledger has separate candidate, published, accepted and recovery states.
    Each owner has at most one accepted pointer. A candidate is never canonical
    merely because it was constructed or published.
    """

    def __init__(self) -> None:
        self.head: Optional[str] = None
        self.candidates: Dict[str, Candidate] = {}
        self.accepted: Dict[str, str] = {}
        self.buffers: Dict[str, dict] = {}

    @staticmethod
    def digest(value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    def prepare(
        self, owner: str, payload: str, base: Optional[str]
    ) -> str:
        if not owner.strip():
            raise ValueError("owner must not be empty")
        if base != self.head:
            raise StateConflict("outdated prepare base")
        checksum = self.digest(payload)
        identity = self.digest(repr((base, owner, checksum)))
        self.candidates[identity] = Candidate(owner, base, payload, checksum)
        return identity

    def publish(self, identity: str, expected_head: Optional[str]) -> str:
        candidate = self.candidates[identity]
        if self.head != expected_head or candidate.parent != expected_head:
            raise StateConflict("published head changed; rebase or reconcile")
        self.head = identity
        return identity

    def readback(self, identity: str) -> Candidate:
        if self.head != identity:
            raise VerificationError("candidate is not the branch head")
        candidate = self.candidates[identity]
        if self.digest(candidate.payload) != candidate.checksum:
            raise VerificationError("payload checksum mismatch")
        return candidate

    def accept(
        self,
        owner: str,
        identity: str,
        expected_payload: str,
        *,
        approved: bool = False,
    ) -> None:
        if not approved:
            raise ApprovalRequired("an explicit owner decision is required")
        candidate = self.readback(identity)
        if candidate.owner != owner or candidate.payload != expected_payload:
            raise VerificationError("owner or content did not match readback")
        self.accepted[owner] = identity

    def save_recovery_packet(
        self, owner: str, payload: str, *, recovery_value: bool
    ) -> Optional[str]:
        """Buffer only when the material has independent recovery value.

        The buffer is never a publisher and never changes self.accepted.
        """
        if not recovery_value:
            return None
        packet_id = self.digest(repr((owner, payload)))
        self.buffers[packet_id] = {
            "owner": owner,
            "payload": payload,
            "status": "UNACCEPTED_RECOVERY_ONLY",
        }
        return packet_id


def demonstration() -> None:
    ledger = EducationalLedger()
    owner = "fictional-public-report"

    first = ledger.prepare(owner, "Published draft A", base=None)
    ledger.publish(first, expected_head=None)
    assert ledger.accepted.get(owner) is None
    ledger.accept(owner, first, "Published draft A", approved=True)
    print("Accepted A:", ledger.accepted[owner][:12])

    base = ledger.head
    stale = ledger.prepare(owner, "Old proposed draft", base=base)
    latest = ledger.prepare(owner, "Newer verified draft B", base=base)
    ledger.publish(latest, expected_head=base)
    ledger.accept(owner, latest, "Newer verified draft B", approved=True)

    try:
        ledger.publish(stale, expected_head=base)
    except StateConflict:
        packet = ledger.save_recovery_packet(
            owner, "Old proposed draft", recovery_value=True
        )
        assert ledger.accepted[owner] == latest
        print("Stale proposal rejected; optional packet:", packet[:12])

    print("Final accepted text:", ledger.readback(latest).payload)
    print("Synthetic example finished successfully.")


if __name__ == "__main__":
    demonstration()

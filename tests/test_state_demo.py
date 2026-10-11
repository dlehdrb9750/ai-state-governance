"""Standard-library tests: run with python -m unittest discover -s tests -v."""
import unittest

from examples.state_demo import (
    ApprovalRequired,
    EducationalLedger,
    StateConflict,
    VerificationError,
)


class StateDemoTests(unittest.TestCase):
    def setUp(self):
        self.ledger = EducationalLedger()
        self.owner = "synthetic-owner"

    def test_preparing_does_not_publish_or_accept(self):
        identity = self.ledger.prepare(self.owner, "one", base=None)
        self.assertIsNone(self.ledger.head)
        self.assertNotIn(self.owner, self.ledger.accepted)
        self.assertIn(identity, self.ledger.candidates)

    def test_publishing_does_not_accept(self):
        identity = self.ledger.prepare(self.owner, "one", base=None)
        self.ledger.publish(identity, expected_head=None)
        self.assertIsNone(self.ledger.accepted.get(self.owner))

    def test_approval_is_required_and_readback_matches(self):
        identity = self.ledger.prepare(self.owner, "one", base=None)
        self.ledger.publish(identity, expected_head=None)
        with self.assertRaises(ApprovalRequired):
            self.ledger.accept(self.owner, identity, "one")
        with self.assertRaises(VerificationError):
            self.ledger.accept(self.owner, identity, "other", approved=True)
        self.ledger.accept(self.owner, identity, "one", approved=True)
        self.assertEqual(self.ledger.accepted[self.owner], identity)

    def test_stale_publisher_cannot_replace_head(self):
        a = self.ledger.prepare(self.owner, "A", base=None)
        b = self.ledger.prepare(self.owner, "B", base=None)
        self.ledger.publish(a, expected_head=None)
        with self.assertRaises(StateConflict):
            self.ledger.publish(b, expected_head=None)
        self.assertEqual(self.ledger.head, a)

    def test_prepare_requires_current_base(self):
        a = self.ledger.prepare(self.owner, "A", base=None)
        self.ledger.publish(a, expected_head=None)
        with self.assertRaises(StateConflict):
            self.ledger.prepare(self.owner, "B", base=None)

    def test_optional_buffer_is_not_canonical(self):
        ignored = self.ledger.save_recovery_packet(
            self.owner, "unused draft", recovery_value=False
        )
        self.assertIsNone(ignored)
        packet = self.ledger.save_recovery_packet(
            self.owner, "valuable note", recovery_value=True
        )
        self.assertIn(packet, self.ledger.buffers)
        self.assertEqual(self.ledger.buffers[packet]["status"],
                         "UNACCEPTED_RECOVERY_ONLY")
        self.assertEqual(self.ledger.accepted, {})

    def test_readback_rejects_non_head_candidate(self):
        identity = self.ledger.prepare(self.owner, "unpublished", base=None)
        with self.assertRaises(VerificationError):
            self.ledger.readback(identity)

    def test_acceptance_remains_owner_scoped(self):
        a = self.ledger.prepare("owner-a", "A", base=None)
        self.ledger.publish(a, expected_head=None)
        self.ledger.accept("owner-a", a, "A", approved=True)
        b = self.ledger.prepare("owner-b", "B", base=a)
        self.ledger.publish(b, expected_head=a)
        self.ledger.accept("owner-b", b, "B", approved=True)
        self.assertEqual(self.ledger.accepted["owner-a"], a)
        self.assertEqual(self.ledger.accepted["owner-b"], b)
        self.assertEqual(self.ledger.head, b)


if __name__ == "__main__":
    unittest.main()

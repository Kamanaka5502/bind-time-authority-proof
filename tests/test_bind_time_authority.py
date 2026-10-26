"""Regression tests for the public bind-time demonstrator."""
import unittest

from bind_time_authority_fabric import CommitChain
from bind_time_authority_fabric.standing_token import StandingToken, verify


class CommitChainTests(unittest.TestCase):
    def make_chain(self):
        chain = CommitChain()
        chain.append("request-A")
        chain.append("decision-ADMIT")
        chain.append("receipt-123")
        return chain

    def test_valid_chain_verifies(self):
        self.assertTrue(self.make_chain().verify())

    def test_replacing_entry_is_detected(self):
        chain = self.make_chain()
        chain.chain[1] = "0" * 64
        self.assertFalse(chain.verify())

    def test_reordering_entries_is_detected(self):
        chain = self.make_chain()
        chain.chain[0], chain.chain[1] = chain.chain[1], chain.chain[0]
        self.assertFalse(chain.verify())

    def test_deleting_entry_is_detected(self):
        chain = self.make_chain()
        del chain.chain[1]
        self.assertFalse(chain.verify())

    def test_appending_arbitrary_entry_is_detected(self):
        chain = self.make_chain()
        chain.chain.append("arbitrary-string")
        self.assertFalse(chain.verify())

    def test_payload_mutation_is_detected(self):
        chain = self.make_chain()
        chain._payloads[1] = "decision-REFUSE"
        self.assertFalse(chain.verify())


class StandingTokenTests(unittest.TestCase):
    def test_token_verifies_with_original_payload(self):
        token = StandingToken(1, "scope-hash", "state-hash").sign()
        self.assertTrue(verify(token))

    def test_payload_mutation_invalidates_signature(self):
        token = StandingToken(1, "scope-hash", "state-hash").sign()
        token["payload"]["authority_epoch"] = 2
        self.assertFalse(verify(token))

    def test_signature_mutation_is_rejected(self):
        token = StandingToken(1, "scope-hash", "state-hash").sign()
        token["signature"] = "0" * 64
        self.assertFalse(verify(token))


if __name__ == "__main__":
    unittest.main()

"""
Automated Validation of JSON Test Scenarios against DFA Implementation.

Academic Course: Formal Languages and Automata Theory (FLA)
Module: Scenario Suite Validator
"""

from __future__ import annotations
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dfa_controller import (
    ControllerState,
    InputSymbol,
    InvalidSymbolError,
    SmartHomeEnergyDFA,
)


class TestScenariosFromJSON(unittest.TestCase):
    """Verifies that all sample scenarios in data/sample_scenarios.json match DFA outcomes."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.dfa = SmartHomeEnergyDFA()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        json_path = os.path.join(base_dir, "data", "sample_scenarios.json")
        with open(json_path, "r", encoding="utf-8") as f:
            cls.scenarios_data = json.load(f)["scenarios"]

    def test_all_json_scenarios(self) -> None:
        for scen in self.scenarios_data:
            with self.subTest(scenario_id=scen["id"], title=scen["title"]):
                # Case 1: Expected invalid token exception
                if scen["expected_state_sequence"] is None:
                    with self.assertRaises(InvalidSymbolError):
                        self.dfa.process_sequence(scen["input_sequence"])
                    continue

                # Case 2: Standard sequence validation
                result = self.dfa.process_sequence(scen["input_sequence"])
                
                # Check acceptance
                self.assertEqual(
                    result.is_accepted,
                    scen["is_accepted"],
                    f"Acceptance mismatch in {scen['id']}: expected {scen['is_accepted']}, got {result.is_accepted}",
                )

                # Check final state
                self.assertEqual(
                    result.final_state.value,
                    scen["expected_final_state"],
                    f"Final state mismatch in {scen['id']}: expected {scen['expected_final_state']}, got {result.final_state.value}",
                )

                # Check state trace
                actual_trace = [s.value for s in result.trace]
                self.assertEqual(
                    actual_trace,
                    scen["expected_state_sequence"],
                    f"Trace mismatch in {scen['id']}: expected {scen['expected_state_sequence']}, got {actual_trace}",
                )

                # Check formal symbol trace
                actual_formal_trace = [s.formal_symbol for s in result.trace]
                self.assertEqual(
                    actual_formal_trace,
                    scen["expected_formal_trace"],
                    f"Formal trace mismatch in {scen['id']}",
                )


if __name__ == "__main__":
    unittest.main()

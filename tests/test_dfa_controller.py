"""
Comprehensive Automated Unit Tests for Smart-Home Energy DFA Controller.

Academic Course: Formal Languages and Automata Theory (FLA)
Module: Formal Verification and Unit Test Suite
"""

from __future__ import annotations
import os
import sys
import unittest

# Ensure src module is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dfa_controller import (
    ControllerState,
    InputSymbol,
    InvalidSymbolError,
    SmartHomeEnergyDFA,
    TRANSITION_TABLE,
    TelemetryDiscretizer,
)


class TestSmartHomeEnergyDFA(unittest.TestCase):
    """
    Formal Verification and Test Suite for Automaton M = (Q, Σ, δ, q0, F).
    """

    def setUp(self) -> None:
        """Instantiate a fresh DFA instance for every test."""
        self.dfa = SmartHomeEnergyDFA()

    # ------------------------------------------------------------------------
    # 1. Mathematical 5-Tuple Structure & Completeness Verification
    # ------------------------------------------------------------------------
    def test_initial_state_definition(self) -> None:
        """Verify initial state is unambiguously q0 (IDLE)."""
        self.assertEqual(self.dfa.q0, ControllerState.IDLE)
        self.assertEqual(self.dfa.current_state, ControllerState.IDLE)
        self.assertEqual(self.dfa.q0.formal_symbol, "q0")

    def test_state_set_cardinality(self) -> None:
        """Verify finite state set Q has exactly 5 well-defined states."""
        expected_states = {
            ControllerState.IDLE,
            ControllerState.NORMAL_OPERATION,
            ControllerState.SOLAR_PRIORITY,
            ControllerState.ENERGY_SAVING,
            ControllerState.SAFETY_SHUTDOWN,
        }
        self.assertEqual(self.dfa.Q, expected_states)
        self.assertEqual(len(self.dfa.Q), 5)

    def test_alphabet_cardinality(self) -> None:
        """Verify finite input alphabet Σ contains exactly 6 distinct symbols."""
        expected_alphabet = {
            InputSymbol.NORMAL,
            InputSymbol.HIGH_DEMAND,
            InputSymbol.SOLAR_AVAILABLE,
            InputSymbol.LOW_BATTERY,
            InputSymbol.SAFETY_ALERT,
            InputSymbol.RESET,
        }
        self.assertEqual(self.dfa.Sigma, expected_alphabet)
        self.assertEqual(len(self.dfa.Sigma), 6)

    def test_accepting_states_subset(self) -> None:
        """Verify F ⊆ Q and SAFETY_SHUTDOWN (q4) is strictly excluded."""
        self.assertTrue(self.dfa.F.issubset(self.dfa.Q))
        self.assertIn(ControllerState.IDLE, self.dfa.F)
        self.assertIn(ControllerState.NORMAL_OPERATION, self.dfa.F)
        self.assertIn(ControllerState.SOLAR_PRIORITY, self.dfa.F)
        self.assertIn(ControllerState.ENERGY_SAVING, self.dfa.F)
        self.assertNotIn(ControllerState.SAFETY_SHUTDOWN, self.dfa.F)

    def test_transition_table_completeness(self) -> None:
        """
        Verify transition function δ is total:
        Every state q ∈ Q has exactly one outgoing transition for every symbol σ ∈ Σ.
        Total entries must equal |Q| × |Σ| = 5 × 6 = 30.
        """
        self.assertEqual(len(self.dfa.delta), 30)
        for state in self.dfa.Q:
            for symbol in self.dfa.Sigma:
                self.assertIn((state, symbol), self.dfa.delta)
                dest = self.dfa.delta[(state, symbol)]
                self.assertIn(dest, self.dfa.Q, f"Transition from {state} on {symbol} leaves Q!")

    def test_dfa_determinism(self) -> None:
        """Verify determinism: transition function yields exactly one next state."""
        for (q, sigma), target in self.dfa.delta.items():
            # In Python dict, each key has a single unique value by construction
            self.assertIsInstance(target, ControllerState)

    # ------------------------------------------------------------------------
    # 2. Transition Dynamics for All States
    # ------------------------------------------------------------------------
    def test_idle_state_transitions(self) -> None:
        """Verify all outgoing transitions from q0 (IDLE)."""
        q0 = ControllerState.IDLE
        self.assertEqual(self.dfa.delta[(q0, InputSymbol.NORMAL)], ControllerState.NORMAL_OPERATION)
        self.assertEqual(self.dfa.delta[(q0, InputSymbol.HIGH_DEMAND)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q0, InputSymbol.SOLAR_AVAILABLE)], ControllerState.SOLAR_PRIORITY)
        self.assertEqual(self.dfa.delta[(q0, InputSymbol.LOW_BATTERY)], ControllerState.IDLE)
        self.assertEqual(self.dfa.delta[(q0, InputSymbol.SAFETY_ALERT)], ControllerState.SAFETY_SHUTDOWN)
        self.assertEqual(self.dfa.delta[(q0, InputSymbol.RESET)], ControllerState.IDLE)

    def test_normal_operation_transitions(self) -> None:
        """Verify all outgoing transitions from q1 (NORMAL_OPERATION)."""
        q1 = ControllerState.NORMAL_OPERATION
        self.assertEqual(self.dfa.delta[(q1, InputSymbol.NORMAL)], ControllerState.NORMAL_OPERATION)
        self.assertEqual(self.dfa.delta[(q1, InputSymbol.HIGH_DEMAND)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q1, InputSymbol.SOLAR_AVAILABLE)], ControllerState.SOLAR_PRIORITY)
        self.assertEqual(self.dfa.delta[(q1, InputSymbol.LOW_BATTERY)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q1, InputSymbol.SAFETY_ALERT)], ControllerState.SAFETY_SHUTDOWN)
        self.assertEqual(self.dfa.delta[(q1, InputSymbol.RESET)], ControllerState.IDLE)

    def test_solar_priority_transitions(self) -> None:
        """Verify all outgoing transitions from q2 (SOLAR_PRIORITY)."""
        q2 = ControllerState.SOLAR_PRIORITY
        self.assertEqual(self.dfa.delta[(q2, InputSymbol.NORMAL)], ControllerState.NORMAL_OPERATION)
        self.assertEqual(self.dfa.delta[(q2, InputSymbol.HIGH_DEMAND)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q2, InputSymbol.SOLAR_AVAILABLE)], ControllerState.SOLAR_PRIORITY)
        self.assertEqual(self.dfa.delta[(q2, InputSymbol.LOW_BATTERY)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q2, InputSymbol.SAFETY_ALERT)], ControllerState.SAFETY_SHUTDOWN)
        self.assertEqual(self.dfa.delta[(q2, InputSymbol.RESET)], ControllerState.IDLE)

    def test_energy_saving_transitions(self) -> None:
        """Verify all outgoing transitions from q3 (ENERGY_SAVING)."""
        q3 = ControllerState.ENERGY_SAVING
        self.assertEqual(self.dfa.delta[(q3, InputSymbol.NORMAL)], ControllerState.NORMAL_OPERATION)
        self.assertEqual(self.dfa.delta[(q3, InputSymbol.HIGH_DEMAND)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q3, InputSymbol.SOLAR_AVAILABLE)], ControllerState.SOLAR_PRIORITY)
        self.assertEqual(self.dfa.delta[(q3, InputSymbol.LOW_BATTERY)], ControllerState.ENERGY_SAVING)
        self.assertEqual(self.dfa.delta[(q3, InputSymbol.SAFETY_ALERT)], ControllerState.SAFETY_SHUTDOWN)
        self.assertEqual(self.dfa.delta[(q3, InputSymbol.RESET)], ControllerState.IDLE)

    # ------------------------------------------------------------------------
    # 3. Safety Lockout Latch & Reset Recovery Invariance
    # ------------------------------------------------------------------------
    def test_safety_alert_from_every_state(self) -> None:
        """Verify SAFETY_ALERT forces an immediate transition to q4 from any state."""
        for state in self.dfa.Q:
            dest = self.dfa.delta[(state, InputSymbol.SAFETY_ALERT)]
            self.assertEqual(
                dest,
                ControllerState.SAFETY_SHUTDOWN,
                f"SAFETY_ALERT from state {state.value} failed to reach SAFETY_SHUTDOWN!",
            )

    def test_safety_lockout_latching_invariance(self) -> None:
        """
        Verify fail-safe lockout: when in SAFETY_SHUTDOWN (q4),
        no operational symbol (NORMAL, HIGH_DEMAND, SOLAR_AVAILABLE, LOW_BATTERY, SAFETY_ALERT)
        can bypass the shutdown. Only RESET recovers the system.
        """
        q4 = ControllerState.SAFETY_SHUTDOWN
        operational_symbols = [
            InputSymbol.NORMAL,
            InputSymbol.HIGH_DEMAND,
            InputSymbol.SOLAR_AVAILABLE,
            InputSymbol.LOW_BATTERY,
            InputSymbol.SAFETY_ALERT,
        ]
        for sym in operational_symbols:
            self.assertEqual(
                self.dfa.delta[(q4, sym)],
                ControllerState.SAFETY_SHUTDOWN,
                f"Latching violated: δ(q4, {sym.value}) escaped q4!",
            )

    def test_reset_recovery_from_safety_shutdown(self) -> None:
        """Verify RESET from SAFETY_SHUTDOWN cleanly recovers exclusively to q0 (IDLE)."""
        q4 = ControllerState.SAFETY_SHUTDOWN
        recovered = self.dfa.delta[(q4, InputSymbol.RESET)]
        self.assertEqual(recovered, ControllerState.IDLE)
        # Check that q0 is an accepting state
        self.assertIn(recovered, self.dfa.F)

    def test_soft_reset_from_operational_states(self) -> None:
        """Verify RESET from q1, q2, q3 returns controller gracefully to standby q0."""
        for state in [ControllerState.NORMAL_OPERATION, ControllerState.SOLAR_PRIORITY, ControllerState.ENERGY_SAVING]:
            self.assertEqual(self.dfa.delta[(state, InputSymbol.RESET)], ControllerState.IDLE)

    # ------------------------------------------------------------------------
    # 4. Input Alphabet Parsing and Rejection of Invalid Symbols
    # ------------------------------------------------------------------------
    def test_symbol_from_shorthand_token(self) -> None:
        """Verify single-character shorthand parsing."""
        self.assertEqual(InputSymbol.from_token("N"), InputSymbol.NORMAL)
        self.assertEqual(InputSymbol.from_token("H"), InputSymbol.HIGH_DEMAND)
        self.assertEqual(InputSymbol.from_token("S"), InputSymbol.SOLAR_AVAILABLE)
        self.assertEqual(InputSymbol.from_token("B"), InputSymbol.LOW_BATTERY)
        self.assertEqual(InputSymbol.from_token("A"), InputSymbol.SAFETY_ALERT)
        self.assertEqual(InputSymbol.from_token("R"), InputSymbol.RESET)

    def test_symbol_case_insensitivity_and_whitespace(self) -> None:
        """Verify robust whitespace and case-insensitive handling."""
        self.assertEqual(InputSymbol.from_token("  normal  "), InputSymbol.NORMAL)
        self.assertEqual(InputSymbol.from_token("s"), InputSymbol.SOLAR_AVAILABLE)
        self.assertEqual(InputSymbol.from_token("High_Demand"), InputSymbol.HIGH_DEMAND)

    def test_rejection_of_invalid_symbols(self) -> None:
        """Verify invalid symbols raise InvalidSymbolError with explanatory message."""
        invalid_tokens = ["X", "UNKNOWN", "123", "@#$", "SOLAR_BURST", "GRID_FAIL"]
        for bad_token in invalid_tokens:
            with self.assertRaises(InvalidSymbolError):
                InputSymbol.from_token(bad_token)

    # ------------------------------------------------------------------------
    # 5. Extended Transition Function δ*(q0, w) and Acceptance Tests
    # ------------------------------------------------------------------------
    def test_empty_sequence_acceptance(self) -> None:
        """
        Verify empty sequence w = ε:
        By formal definition δ*(q0, ε) = q0. Since q0 ∈ F (undisturbed idle baseline),
        ε ∈ L(M) is accepted.
        """
        res = self.dfa.process_sequence("")
        self.assertEqual(res.final_state, ControllerState.IDLE)
        self.assertTrue(res.is_accepted)
        self.assertEqual(res.trace, [ControllerState.IDLE])
        self.assertEqual(len(res.transitions), 0)

    def test_scenario_normal_operation(self) -> None:
        """Trace: q0 --(N)--> q1 --(N)--> q1 --(N)--> q1 (Accepted)."""
        res = self.dfa.process_sequence(["NORMAL", "NORMAL", "NORMAL"])
        self.assertEqual(res.final_state, ControllerState.NORMAL_OPERATION)
        self.assertTrue(res.is_accepted)
        self.assertEqual(res.trace, [
            ControllerState.IDLE,
            ControllerState.NORMAL_OPERATION,
            ControllerState.NORMAL_OPERATION,
            ControllerState.NORMAL_OPERATION,
        ])

    def test_scenario_solar_priority(self) -> None:
        """Trace: q0 --(N)--> q1 --(S)--> q2 --(S)--> q2 --(N)--> q1 (Accepted)."""
        res = self.dfa.process_sequence("N, S, S, N")
        self.assertEqual(res.final_state, ControllerState.NORMAL_OPERATION)
        self.assertTrue(res.is_accepted)
        self.assertEqual(res.trace, [
            ControllerState.IDLE,
            ControllerState.NORMAL_OPERATION,
            ControllerState.SOLAR_PRIORITY,
            ControllerState.SOLAR_PRIORITY,
            ControllerState.NORMAL_OPERATION,
        ])

    def test_scenario_peak_demand_shedding(self) -> None:
        """Trace: q0 --(N)--> q1 --(H)--> q3 --(H)--> q3 (Accepted in ENERGY_SAVING)."""
        res = self.dfa.process_sequence("N, H, H")
        self.assertEqual(res.final_state, ControllerState.ENERGY_SAVING)
        self.assertTrue(res.is_accepted)

    def test_scenario_battery_depletion(self) -> None:
        """Trace: q0 --(S)--> q2 --(B)--> q3 --(N)--> q1 (Accepted)."""
        res = self.dfa.process_sequence("S, B, N")
        self.assertEqual(res.final_state, ControllerState.NORMAL_OPERATION)
        self.assertTrue(res.is_accepted)

    def test_scenario_safety_alert_rejection(self) -> None:
        """
        Trace: q0 --(N)--> q1 --(A)--> q4 --(N)--> q4 --(S)--> q4 (Rejected: w ∉ L(M)).
        """
        res = self.dfa.process_sequence("N, A, N, S")
        self.assertEqual(res.final_state, ControllerState.SAFETY_SHUTDOWN)
        self.assertFalse(res.is_accepted)
        self.assertIn("REJECTED", res.status_summary)

    def test_scenario_reset_recovery_acceptance(self) -> None:
        """
        Trace: q0 --(N)--> q1 --(A)--> q4 --(R)--> q0 --(N)--> q1 (Accepted).
        """
        res = self.dfa.process_sequence("N, A, R, N")
        self.assertEqual(res.final_state, ControllerState.NORMAL_OPERATION)
        self.assertTrue(res.is_accepted)
        self.assertEqual(res.trace, [
            ControllerState.IDLE,
            ControllerState.NORMAL_OPERATION,
            ControllerState.SAFETY_SHUTDOWN,
            ControllerState.IDLE,
            ControllerState.NORMAL_OPERATION,
        ])

    def test_scenario_repeated_events(self) -> None:
        """Verify stability and idempotency under repeated identical event bursts."""
        res = self.dfa.process_sequence("H, H, H, H")
        self.assertEqual(res.final_state, ControllerState.ENERGY_SAVING)
        self.assertTrue(res.is_accepted)

    # ------------------------------------------------------------------------
    # 6. Sensor Telemetry Discretizer Validation
    # ------------------------------------------------------------------------
    def test_discretizer_priorities(self) -> None:
        """Verify continuous sensor thresholds map accurately to discrete tokens."""
        # 1. Safety trip has highest precedence
        sym1 = TelemetryDiscretizer.discretize(demand_kw=1.0, solar_w_m2=900.0, battery_pct=100.0, safety_trip=True)
        self.assertEqual(sym1, InputSymbol.SAFETY_ALERT)

        # 2. Reset commanded
        sym2 = TelemetryDiscretizer.discretize(demand_kw=1.0, solar_w_m2=900.0, battery_pct=100.0, reset_triggered=True)
        self.assertEqual(sym2, InputSymbol.RESET)

        # 3. High demand threshold (> 4.5 kW)
        sym3 = TelemetryDiscretizer.discretize(demand_kw=5.2, solar_w_m2=800.0, battery_pct=80.0)
        self.assertEqual(sym3, InputSymbol.HIGH_DEMAND)

        # 4. Low battery threshold (< 25%)
        sym4 = TelemetryDiscretizer.discretize(demand_kw=2.0, solar_w_m2=100.0, battery_pct=15.0)
        self.assertEqual(sym4, InputSymbol.LOW_BATTERY)

        # 5. Solar harvest available (>= 300 W/m²)
        sym5 = TelemetryDiscretizer.discretize(demand_kw=2.0, solar_w_m2=550.0, battery_pct=85.0)
        self.assertEqual(sym5, InputSymbol.SOLAR_AVAILABLE)

        # 6. Nominal baseline
        sym6 = TelemetryDiscretizer.discretize(demand_kw=2.0, solar_w_m2=150.0, battery_pct=80.0)
        self.assertEqual(sym6, InputSymbol.NORMAL)


if __name__ == "__main__":
    unittest.main()

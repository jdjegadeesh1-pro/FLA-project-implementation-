"""
Design and Implementation of a Deterministic Finite Automaton (DFA)
for Smart-Home Energy Automation Controllers.

Academic Course: Formal Languages and Automata Theory (FLA)
Module: Core Automaton Engine & Mathematical 5-Tuple Formulation
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Sequence, Set, Tuple, Union


class ControllerState(str, Enum):
    """
    Q: Finite set of internal controller states.
    
    States:
        IDLE (q0): Quiescent standby state; sensors active, power stage disconnected.
        NORMAL_OPERATION (q1): Grid-connected active distribution under nominal load.
        SOLAR_PRIORITY (q2): Rooftop photovoltaic harvest prioritized for home loads.
        ENERGY_SAVING (q3): Demand-response / load curtailment / battery reserve mode.
        SAFETY_SHUTDOWN (q4): Emergency isolation latch; all power relays de-energized.
    """
    IDLE = "IDLE"
    NORMAL_OPERATION = "NORMAL_OPERATION"
    SOLAR_PRIORITY = "SOLAR_PRIORITY"
    ENERGY_SAVING = "ENERGY_SAVING"
    SAFETY_SHUTDOWN = "SAFETY_SHUTDOWN"

    @property
    def formal_symbol(self) -> str:
        """Academic formal notation mapping (q0 - q4)."""
        mapping = {
            ControllerState.IDLE: "q0",
            ControllerState.NORMAL_OPERATION: "q1",
            ControllerState.SOLAR_PRIORITY: "q2",
            ControllerState.ENERGY_SAVING: "q3",
            ControllerState.SAFETY_SHUTDOWN: "q4",
        }
        return mapping[self]


class InputSymbol(str, Enum):
    """
    Σ: Finite input alphabet of discrete environmental and operational events.
    
    Alphabet:
        NORMAL (N): Power demand is within nominal threshold; no safety hazards.
        HIGH_DEMAND (H): Load demand exceeds grid/inverter configured threshold.
        SOLAR_AVAILABLE (S): Renewable solar generation is sufficient for powering loads.
        LOW_BATTERY (B): Storage battery state of charge (SoC) dropped below limit.
        SAFETY_ALERT (A): Critical condition detected (thermal runaway, short, surge).
        RESET (R): Supervised reset signal issued by operator or self-test recovery.
    """
    NORMAL = "NORMAL"
    HIGH_DEMAND = "HIGH_DEMAND"
    SOLAR_AVAILABLE = "SOLAR_AVAILABLE"
    LOW_BATTERY = "LOW_BATTERY"
    SAFETY_ALERT = "SAFETY_ALERT"
    RESET = "RESET"

    @property
    def formal_token(self) -> str:
        """Shorthand single-character notation for strings and diagrams."""
        mapping = {
            InputSymbol.NORMAL: "N",
            InputSymbol.HIGH_DEMAND: "H",
            InputSymbol.SOLAR_AVAILABLE: "S",
            InputSymbol.LOW_BATTERY: "B",
            InputSymbol.SAFETY_ALERT: "A",
            InputSymbol.RESET: "R",
        }
        return mapping[self]

    @classmethod
    def from_token(cls, token: str) -> InputSymbol:
        """Parse token string (full name or single-character shorthand)."""
        token_upper = token.strip().upper()
        # Direct enum value match
        for item in cls:
            if item.value == token_upper:
                return item
        # Shorthand mapping
        shorthand_map = {
            "N": cls.NORMAL,
            "H": cls.HIGH_DEMAND,
            "S": cls.SOLAR_AVAILABLE,
            "B": cls.LOW_BATTERY,
            "A": cls.SAFETY_ALERT,
            "R": cls.RESET,
        }
        if token_upper in shorthand_map:
            return shorthand_map[token_upper]
        raise InvalidSymbolError(
            f"Symbol '{token}' is not recognized in input alphabet Σ = {[s.value for s in cls]} "
            f"or shorthand tokens {list(shorthand_map.keys())}."
        )


class InvalidSymbolError(ValueError):
    """Raised when an input symbol does not belong to the alphabet Σ."""
    pass


class DFATransitionStep(NamedTuple):
    """Record of a single deterministic transition step."""
    step_number: int
    source_state: ControllerState
    input_symbol: InputSymbol
    destination_state: ControllerState


class SimulationResult(NamedTuple):
    """Structured report returned upon evaluating an input sequence."""
    initial_state: ControllerState
    input_sequence: List[InputSymbol]
    trace: List[ControllerState]
    transitions: List[DFATransitionStep]
    final_state: ControllerState
    is_accepted: bool
    status_summary: str


# ============================================================================
# EXPLICIT STATE TRANSITION TABLE δ : Q × Σ → Q
# Total mapping with exactly |Q| × |Σ| = 5 × 6 = 30 deterministic entries.
# ============================================================================
TRANSITION_TABLE: Dict[Tuple[ControllerState, InputSymbol], ControllerState] = {
    # ------------------------------------------------------------------------
    # State q0: IDLE (Quiescent Standby / Initial State)
    # ------------------------------------------------------------------------
    (ControllerState.IDLE, InputSymbol.NORMAL): ControllerState.NORMAL_OPERATION,
    (ControllerState.IDLE, InputSymbol.HIGH_DEMAND): ControllerState.ENERGY_SAVING,
    (ControllerState.IDLE, InputSymbol.SOLAR_AVAILABLE): ControllerState.SOLAR_PRIORITY,
    (ControllerState.IDLE, InputSymbol.LOW_BATTERY): ControllerState.IDLE,
    (ControllerState.IDLE, InputSymbol.SAFETY_ALERT): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.IDLE, InputSymbol.RESET): ControllerState.IDLE,

    # ------------------------------------------------------------------------
    # State q1: NORMAL_OPERATION (Nominal Grid Operation)
    # ------------------------------------------------------------------------
    (ControllerState.NORMAL_OPERATION, InputSymbol.NORMAL): ControllerState.NORMAL_OPERATION,
    (ControllerState.NORMAL_OPERATION, InputSymbol.HIGH_DEMAND): ControllerState.ENERGY_SAVING,
    (ControllerState.NORMAL_OPERATION, InputSymbol.SOLAR_AVAILABLE): ControllerState.SOLAR_PRIORITY,
    (ControllerState.NORMAL_OPERATION, InputSymbol.LOW_BATTERY): ControllerState.ENERGY_SAVING,
    (ControllerState.NORMAL_OPERATION, InputSymbol.SAFETY_ALERT): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.NORMAL_OPERATION, InputSymbol.RESET): ControllerState.IDLE,

    # ------------------------------------------------------------------------
    # State q2: SOLAR_PRIORITY (Renewable Eco Mode)
    # ------------------------------------------------------------------------
    (ControllerState.SOLAR_PRIORITY, InputSymbol.NORMAL): ControllerState.NORMAL_OPERATION,
    (ControllerState.SOLAR_PRIORITY, InputSymbol.HIGH_DEMAND): ControllerState.ENERGY_SAVING,
    (ControllerState.SOLAR_PRIORITY, InputSymbol.SOLAR_AVAILABLE): ControllerState.SOLAR_PRIORITY,
    (ControllerState.SOLAR_PRIORITY, InputSymbol.LOW_BATTERY): ControllerState.ENERGY_SAVING,
    (ControllerState.SOLAR_PRIORITY, InputSymbol.SAFETY_ALERT): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.SOLAR_PRIORITY, InputSymbol.RESET): ControllerState.IDLE,

    # ------------------------------------------------------------------------
    # State q3: ENERGY_SAVING (Demand Response / Peak Shaving)
    # ------------------------------------------------------------------------
    (ControllerState.ENERGY_SAVING, InputSymbol.NORMAL): ControllerState.NORMAL_OPERATION,
    (ControllerState.ENERGY_SAVING, InputSymbol.HIGH_DEMAND): ControllerState.ENERGY_SAVING,
    (ControllerState.ENERGY_SAVING, InputSymbol.SOLAR_AVAILABLE): ControllerState.SOLAR_PRIORITY,
    (ControllerState.ENERGY_SAVING, InputSymbol.LOW_BATTERY): ControllerState.ENERGY_SAVING,
    (ControllerState.ENERGY_SAVING, InputSymbol.SAFETY_ALERT): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.ENERGY_SAVING, InputSymbol.RESET): ControllerState.IDLE,

    # ------------------------------------------------------------------------
    # State q4: SAFETY_SHUTDOWN (Lockout Latch / Non-Accepting Hazard State)
    # Fail-safe invariant: Only a supervised RESET clears the latch to IDLE (q0).
    # All operational inputs remain safely trapped in q4.
    # ------------------------------------------------------------------------
    (ControllerState.SAFETY_SHUTDOWN, InputSymbol.NORMAL): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.SAFETY_SHUTDOWN, InputSymbol.HIGH_DEMAND): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.SAFETY_SHUTDOWN, InputSymbol.SOLAR_AVAILABLE): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.SAFETY_SHUTDOWN, InputSymbol.LOW_BATTERY): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.SAFETY_SHUTDOWN, InputSymbol.SAFETY_ALERT): ControllerState.SAFETY_SHUTDOWN,
    (ControllerState.SAFETY_SHUTDOWN, InputSymbol.RESET): ControllerState.IDLE,
}


class SmartHomeEnergyDFA:
    """
    Formal Deterministic Finite Automaton (DFA) Model M = (Q, Σ, δ, q0, F).
    
    Mathematical Specification:
        Q  = { IDLE, NORMAL_OPERATION, SOLAR_PRIORITY, ENERGY_SAVING, SAFETY_SHUTDOWN }
        Σ  = { NORMAL, HIGH_DEMAND, SOLAR_AVAILABLE, LOW_BATTERY, SAFETY_ALERT, RESET }
        δ  : Q × Σ → Q (as formulated in TRANSITION_TABLE)
        q0 = IDLE
        F  = { IDLE, NORMAL_OPERATION, SOLAR_PRIORITY, ENERGY_SAVING }
        
    Language Semantics:
        The language L(M) accepted by the automaton represents the set of all input
        event traces w ∈ Σ* that keep or leave the controller in a healthy,
        compliant operational state.
        
        Sequences that terminate in SAFETY_SHUTDOWN (q4) without an authorized RESET
        recovery are REJECTED (w ∉ L(M)), formally designating an unresolved
        emergency lockout condition.
        
        Important Academic Clarification:
        Acceptance by this formal automaton proves language membership in the
        mathematical model; it does not constitute physical verification of
        electrical circuitry or actual household wiring.
    """

    def __init__(
        self,
        initial_state: ControllerState = ControllerState.IDLE,
        accepting_states: Optional[Set[ControllerState]] = None,
    ) -> None:
        self.Q: FrozenSet[ControllerState] = frozenset(ControllerState)
        self.Sigma: FrozenSet[InputSymbol] = frozenset(InputSymbol)
        self.delta: Dict[Tuple[ControllerState, InputSymbol], ControllerState] = TRANSITION_TABLE
        self.q0: ControllerState = initial_state
        
        # Default accepting states F = Q \ {SAFETY_SHUTDOWN}
        if accepting_states is None:
            self.F: FrozenSet[ControllerState] = frozenset({
                ControllerState.IDLE,
                ControllerState.NORMAL_OPERATION,
                ControllerState.SOLAR_PRIORITY,
                ControllerState.ENERGY_SAVING,
            })
        else:
            self.F = frozenset(accepting_states)

        self.current_state: ControllerState = self.q0
        self.validate_dfa()

    def validate_dfa(self) -> bool:
        """
        Formally verifies mathematical consistency and completeness:
        1. q0 ∈ Q
        2. F ⊆ Q
        3. Transition table δ contains exactly |Q| × |Σ| entries.
        4. Every state-symbol pair (q, σ) has a deterministic destination in Q.
        """
        if self.q0 not in self.Q:
            raise ValueError(f"Initial state {self.q0} is not in state set Q.")
        if not self.F.issubset(self.Q):
            raise ValueError(f"Accepting states {self.F} are not a subset of Q.")
        
        expected_size = len(self.Q) * len(self.Sigma)
        actual_size = len(self.delta)
        if actual_size != expected_size:
            raise ValueError(
                f"Transition table is incomplete! Expected {expected_size} entries "
                f"for |Q|={len(self.Q)} × |Σ|={len(self.Sigma)}, but found {actual_size}."
            )

        for q in self.Q:
            for s in self.Sigma:
                if (q, s) not in self.delta:
                    raise ValueError(f"Missing transition rule for pair ({q.value}, {s.value}).")
                next_q = self.delta[(q, s)]
                if next_q not in self.Q:
                    raise ValueError(
                        f"Transition δ({q.value}, {s.value}) -> {next_q} leads outside Q."
                    )
        return True

    def reset_to_initial(self) -> None:
        """Resets the automaton instance back to state q0."""
        self.current_state = self.q0

    def step(self, symbol: Union[InputSymbol, str]) -> ControllerState:
        """
        Executes single transition δ(current_state, symbol) -> next_state in O(1) time.
        
        Args:
            symbol: InputSymbol instance or valid token string.
            
        Returns:
            New ControllerState.
        """
        parsed_symbol = symbol if isinstance(symbol, InputSymbol) else InputSymbol.from_token(symbol)
        next_state = self.delta[(self.current_state, parsed_symbol)]
        self.current_state = next_state
        return self.current_state

    def process_sequence(
        self,
        sequence: Union[Sequence[Union[InputSymbol, str]], str],
        start_state: Optional[ControllerState] = None,
    ) -> SimulationResult:
        """
        Evaluates the extended transition function δ*(q_start, w) across string w.
        
        Args:
            sequence: Sequence of InputSymbols, token strings, or comma/space-separated string.
            start_state: Optional initial state override (defaults to self.q0).
            
        Returns:
            SimulationResult containing full trace, step records, final state, and acceptance.
        """
        state = start_state if start_state is not None else self.q0
        
        # Tokenize if string
        parsed_tokens: List[InputSymbol] = []
        if isinstance(sequence, str):
            clean_str = sequence.strip()
            if not clean_str:
                tokens = []
            elif "," in clean_str:
                tokens = [t.strip() for t in clean_str.split(",") if t.strip()]
            elif " " in clean_str:
                tokens = [t.strip() for t in clean_str.split() if t.strip()]
            else:
                # Try multi-char token first, else single-character stream (e.g., "NSHB")
                try:
                    single_parsed = InputSymbol.from_token(clean_str)
                    tokens = [clean_str]
                except InvalidSymbolError:
                    tokens = list(clean_str)
            for t in tokens:
                parsed_tokens.append(InputSymbol.from_token(t))
        else:
            for item in sequence:
                parsed_tokens.append(item if isinstance(item, InputSymbol) else InputSymbol.from_token(item))

        trace: List[ControllerState] = [state]
        transitions: List[DFATransitionStep] = []

        # Extended transition computation δ*(q0, w)
        for idx, sym in enumerate(parsed_tokens, start=1):
            next_state = self.delta[(state, sym)]
            transitions.append(DFATransitionStep(
                step_number=idx,
                source_state=state,
                input_symbol=sym,
                destination_state=next_state,
            ))
            state = next_state
            trace.append(state)

        is_accepted = state in self.F
        if is_accepted:
            summary = (
                f"ACCEPTED: System reached compliant operating state '{state.value}' "
                f"({state.formal_symbol} ∈ F)."
            )
        else:
            summary = (
                f"REJECTED: System terminated in unrecovered hazard state '{state.value}' "
                f"({state.formal_symbol} ∉ F)."
            )

        return SimulationResult(
            initial_state=start_state if start_state is not None else self.q0,
            input_sequence=parsed_tokens,
            trace=trace,
            transitions=transitions,
            final_state=state,
            is_accepted=is_accepted,
            status_summary=summary,
        )


class TelemetryDiscretizer:
    """
    Sensor Data Abstraction and Discretization Function:
        f : R^n × {0,1}^m → Σ
        
    Translates continuous physical measurements into discrete formal alphabet tokens:
    - Power demand (kW)
    - Solar irradiance (W/m²)
    - Battery state-of-charge (%)
    - Hardware safety trip line (Boolean)
    - Operator reset latch (Boolean)
    """
    DEMAND_THRESHOLD_KW: float = 4.5
    SOLAR_THRESHOLD_W_M2: float = 300.0
    BATTERY_LOW_THRESHOLD_PCT: float = 25.0

    @classmethod
    def discretize(
        cls,
        demand_kw: float,
        solar_w_m2: float,
        battery_pct: float,
        safety_trip: bool = False,
        reset_triggered: bool = False,
    ) -> InputSymbol:
        """
        Deterministic discretization priority:
        1. SAFETY_ALERT if hardware fault triggered.
        2. RESET if operator manual reset commanded.
        3. HIGH_DEMAND if demand > 4.5 kW.
        4. LOW_BATTERY if battery SoC < 25.0%.
        5. SOLAR_AVAILABLE if solar irradiance >= 300 W/m².
        6. NORMAL under standard nominal conditions.
        """
        if safety_trip:
            return InputSymbol.SAFETY_ALERT
        if reset_triggered:
            return InputSymbol.RESET
        if demand_kw > cls.DEMAND_THRESHOLD_KW:
            return InputSymbol.HIGH_DEMAND
        if battery_pct < cls.BATTERY_LOW_THRESHOLD_PCT:
            return InputSymbol.LOW_BATTERY
        if solar_w_m2 >= cls.SOLAR_THRESHOLD_W_M2:
            return InputSymbol.SOLAR_AVAILABLE
        return InputSymbol.NORMAL

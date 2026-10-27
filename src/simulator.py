"""
Interactive Command-Line Simulator for Smart-Home Energy DFA Controller.

Academic Course: Formal Languages and Automata Theory (FLA)
Module: Execution Harness and Simulation Runner
"""

from __future__ import annotations
import sys
import time
from typing import List, Optional

# Ensure package import compatibility
if __name__ == "__main__" and __package__ is None:
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dfa_controller import (
    ControllerState,
    DFATransitionStep,
    InputSymbol,
    InvalidSymbolError,
    SimulationResult,
    SmartHomeEnergyDFA,
    TelemetryDiscretizer,
)


def print_banner() -> None:
    print("=" * 78)
    print("  DETERMINISTIC FINITE AUTOMATON (DFA) SMART-HOME ENERGY CONTROLLER")
    print("  Formal Model: M = (Q, Σ, δ, q0, F) | Academic Simulation Engine")
    print("=" * 78)
    print("  * Note: All operational outputs represent formal automaton states in a")
    print("    simulated discrete-event model, not live electrical measurements.")
    print("=" * 78)


def display_transition_step(step: DFATransitionStep, is_accepting: bool) -> None:
    """Pretty prints an individual state transition."""
    acc_badge = "[ACCEPTING]" if is_accepting else "[NON-ACCEPTING]"
    src = f"{step.source_state.value} ({step.source_state.formal_symbol})"
    dst = f"{step.destination_state.value} ({step.destination_state.formal_symbol})"
    sym = f"{step.input_symbol.value} ('{step.input_symbol.formal_token}')"
    print(f"  Step {step.step_number:02d}: δ({src}, {sym}) --> {dst}  {acc_badge}")


def print_formal_transition_table(dfa: SmartHomeEnergyDFA) -> None:
    """Renders the complete formal transition table δ : Q × Σ → Q."""
    print("\n" + "=" * 78)
    print("                FORMAL DFA STATE TRANSITION TABLE δ(q, σ)")
    print("=" * 78)
    header = f"{'State (q)':<22} | " + " | ".join(f"{s.formal_token:<6}" for s in InputSymbol)
    print(header)
    print("-" * 78)
    
    for state in ControllerState:
        row_label = f"{state.formal_symbol} ({state.value[:10]})"
        if state == dfa.q0:
            row_label = "-> " + row_label
        elif state in dfa.F:
            row_label = " * " + row_label
        else:
            row_label = "   " + row_label
            
        cells = []
        for symbol in InputSymbol:
            next_state = dfa.delta[(state, symbol)]
            cells.append(f"{next_state.formal_symbol:<6}")
        print(f"{row_label:<22} | " + " | ".join(cells))
        
    print("-" * 78)
    print("Notation: '->' = Initial State (q0); '*' = Accepting/Final State (F).")
    print("Tokens: N = NORMAL, H = HIGH_DEMAND, S = SOLAR_AVAILABLE,")
    print("        B = LOW_BATTERY, A = SAFETY_ALERT, R = RESET.")
    print("=" * 78 + "\n")


def run_interactive_stepping(dfa: SmartHomeEnergyDFA) -> None:
    """Interactive step-by-step event injection."""
    dfa.reset_to_initial()
    print("\n[Interactive Mode Initiated]")
    print("Type an event name or single token: N, H, S, B, A, R (or 'QUIT'/'RESET'):")
    print(f"Initial State: {dfa.current_state.value} ({dfa.current_state.formal_symbol})\n")
    
    step_num = 1
    while True:
        try:
            user_input = input(f"[{dfa.current_state.formal_symbol}] Inject Event > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting interactive stepping.")
            break
            
        if not user_input:
            continue
        if user_input.upper() in {"QUIT", "EXIT", "Q"}:
            break
        if user_input.upper() == "RESET_MACHINE":
            dfa.reset_to_initial()
            step_num = 1
            print(f"Machine reset to q0: {dfa.current_state.value}\n")
            continue
            
        try:
            symbol = InputSymbol.from_token(user_input)
            prev_state = dfa.current_state
            next_state = dfa.step(symbol)
            is_acc = next_state in dfa.F
            step_record = DFATransitionStep(step_num, prev_state, symbol, next_state)
            display_transition_step(step_record, is_acc)
            step_num += 1
        except InvalidSymbolError as err:
            print(f"  [ERROR] {err}")
            
    print(f"\nFinal State reached: {dfa.current_state.value} ({dfa.current_state.formal_symbol})")
    status = "ACCEPTED (Safe/Compliant)" if dfa.current_state in dfa.F else "REJECTED (Lockout/Fault)"
    print(f"Formal Status: {status}\n")


def run_batch_sequence(dfa: SmartHomeEnergyDFA, raw_sequence: Optional[str] = None) -> SimulationResult:
    """Processes a discrete string of symbols and displays mathematical trajectory."""
    if raw_sequence is None:
        raw_sequence = input("\nEnter symbol sequence (e.g., 'N,S,H,B,A,R' or 'NSHBAR'): ").strip()
        
    print(f"\nEvaluating Input Sequence: '{raw_sequence}'")
    print("-" * 78)
    
    try:
        result = dfa.process_sequence(raw_sequence)
    except InvalidSymbolError as err:
        print(f"[REJECTION ERROR] {err}")
        raise
        
    for step in result.transitions:
        display_transition_step(step, step.destination_state in dfa.F)
        
    print("-" * 78)
    formal_trace = " -> ".join(s.formal_symbol for s in result.trace)
    print(f"State Sequence Trace: {formal_trace}")
    print(f"Initial State       : {result.initial_state.value} ({result.initial_state.formal_symbol})")
    print(f"Final State         : {result.final_state.value} ({result.final_state.formal_symbol})")
    print(f"Evaluation Outcome  : {'ACCEPTED (w ∈ L(M))' if result.is_accepted else 'REJECTED (w ∉ L(M))'}")
    print(f"Summary             : {result.status_summary}\n")
    return result


def run_sensor_telemetry_simulation(dfa: SmartHomeEnergyDFA) -> None:
    """
    Demonstrates continuous telemetry discretization into formal DFA transitions.
    Simulates a 24-hour smart-home lifecycle profile.
    """
    print("\n" + "=" * 78)
    print("       CONTINUOUS SENSOR TELEMETRY DISCRETIZATION & DFA DISPATCH")
    print("=" * 78)
    print("Simulating temporal sensor telemetry mapped via Discretization Function:")
    print("  f(demand, solar, battery, safety_trip, reset_btn) -> σ ∈ Σ\n")
    
    # Representative telemetry frames (simulated physical values)
    telemetry_frames = [
        {"desc": "06:00 Dawn Quiescent Standby", "demand": 1.2, "solar": 50.0, "batt": 80.0, "trip": False, "rst": False},
        {"desc": "08:00 Morning Routine (Grid Active)", "demand": 2.8, "solar": 180.0, "batt": 78.0, "trip": False, "rst": False},
        {"desc": "12:00 Solar Peak Generation", "demand": 2.1, "solar": 720.0, "batt": 92.0, "trip": False, "rst": False},
        {"desc": "15:00 Sustained Solar Harvest", "demand": 2.4, "solar": 650.0, "batt": 95.0, "trip": False, "rst": False},
        {"desc": "18:00 Evening Peak Demand Surge", "demand": 5.8, "solar": 80.0, "batt": 60.0, "trip": False, "rst": False},
        {"desc": "21:00 High Load Continues", "demand": 5.2, "solar": 0.0, "batt": 45.0, "trip": False, "rst": False},
        {"desc": "23:00 Demand Normalizes", "demand": 2.0, "solar": 0.0, "batt": 40.0, "trip": False, "rst": False},
        {"desc": "02:00 Battery Critical Discharge", "demand": 1.5, "solar": 0.0, "batt": 18.0, "trip": False, "rst": False},
        {"desc": "03:15 Electrical Short / Thermal Spike", "demand": 6.8, "solar": 0.0, "batt": 17.0, "trip": True, "rst": False},
        {"desc": "03:30 Post-Trip Sunrise Attempt", "demand": 1.0, "solar": 400.0, "batt": 18.0, "trip": False, "rst": False},
        {"desc": "04:00 Supervised Safety Reset", "demand": 1.0, "solar": 400.0, "batt": 50.0, "trip": False, "rst": True},
        {"desc": "04:30 Day Resumption", "demand": 1.8, "solar": 520.0, "batt": 55.0, "trip": False, "rst": False},
    ]

    dfa.reset_to_initial()
    for idx, frame in enumerate(telemetry_frames, start=1):
        symbol = TelemetryDiscretizer.discretize(
            demand_kw=frame["demand"],
            solar_w_m2=frame["solar"],
            battery_pct=frame["batt"],
            safety_trip=frame["trip"],
            reset_triggered=frame["rst"],
        )
        prev_state = dfa.current_state
        next_state = dfa.step(symbol)
        
        telemetry_str = (
            f"Demand={frame['demand']:.1f}kW, Solar={frame['solar']:.0f}W/m², "
            f"Batt={frame['batt']:.0f}%, Trip={frame['trip']}, Rst={frame['rst']}"
        )
        print(f"Frame {idx:02d} [{frame['desc']}]:")
        print(f"  Sensor Reading : {telemetry_str}")
        print(f"  Discretized    : σ = {symbol.value} ('{symbol.formal_token}')")
        print(f"  Transition     : δ({prev_state.formal_symbol}, {symbol.formal_token}) -> {next_state.formal_symbol} ({next_state.value})")
        print(f"  State Status   : {'[ACCEPTING]' if next_state in dfa.F else '[LOCKOUT LATCHED]'}\n")
        time.sleep(0.05)


def run_demonstration_suite(dfa: SmartHomeEnergyDFA) -> None:
    """Executes the standard suite of academic scenarios."""
    scenarios = [
        ("Scenario 1: Nominal Power Dispatch", "N, N, N"),
        ("Scenario 2: Renewable Solar Transition", "N, S, S, N"),
        ("Scenario 3: Peak Demand Surge & Shedding", "N, H, H, N"),
        ("Scenario 4: Battery Depletion & Conservation", "N, S, B, N"),
        ("Scenario 5: Safety Fault Trip & Lockout Latch", "N, S, A, N, H, S"),
        ("Scenario 6: Fault Recovery via Supervised Reset", "N, A, R, N"),
        ("Scenario 7: Repeated & Redundant Events", "H, H, H, S, S, S"),
        ("Scenario 8: Quiescent Edge Case (Empty Sequence)", ""),
    ]
    
    print("\n" + "=" * 78)
    print("             ACADEMIC DEMONSTRATION & VERIFICATION SUITE")
    print("=" * 78)
    for title, seq in scenarios:
        print(f"\n>>> {title}")
        run_batch_sequence(dfa, seq)


def main() -> None:
    dfa = SmartHomeEnergyDFA()
    print_banner()
    
    menu = """
Select Simulation Mode:
  1. View Formal DFA Transition Table δ(Q, Σ)
  2. Run Academic Demonstration Scenarios (8 Scenarios)
  3. Interactive Step-by-Step Transition Injection
  4. Process Custom Input Sequence (Batch Evaluation)
  5. Continuous Sensor Telemetry Discretization Simulation
  6. Exit Simulator
"""
    while True:
        print(menu)
        try:
            choice = input("Enter choice (1-6): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting simulator.")
            break
            
        if choice == "1":
            print_formal_transition_table(dfa)
        elif choice == "2":
            run_demonstration_suite(dfa)
        elif choice == "3":
            run_interactive_stepping(dfa)
        elif choice == "4":
            try:
                run_batch_sequence(dfa)
            except InvalidSymbolError:
                pass
        elif choice == "5":
            run_sensor_telemetry_simulation(dfa)
        elif choice == "6":
            print("Exiting simulator. Thank you.")
            break
        else:
            print("Invalid selection. Please choose 1 through 6.")


if __name__ == "__main__":
    main()

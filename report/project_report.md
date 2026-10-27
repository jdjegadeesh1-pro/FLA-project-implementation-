# DESIGN AND IMPLEMENTATION OF A DETERMINISTIC FINITE AUTOMATON (DFA) FOR SMART-HOME ENERGY AUTOMATION CONTROLLERS

---

```
                   SRM INSTITUTE OF SCIENCE AND TECHNOLOGY
                           TIRUCHIRAPPALLI - 621105
                      B.Tech in Information Technology
                                 2026-2027

                           Course Code: 21CSC301T
                  Course Name: FORMAL LANGUAGE AND AUTOMATA

                                 Report on
     DESIGN AND IMPLEMENTATION OF A DETERMINISTIC FINITE AUTOMATON (DFA)
              FOR SMART-HOME ENERGY AUTOMATION CONTROLLERS

                               Submitted by
                 Name of the Student : [STUDENT NAME 1]
                 Roll Number         : [REGISTER NUMBER 1]
                 Name of the Student : [STUDENT NAME 2]
                 Roll Number         : [REGISTER NUMBER 2]

                           Under the guidance of
                         [FACULTY GUIDE NAME, Ph.D.]
                            [Designation / Title]

                    DEPARTMENT OF INFORMATION TECHNOLOGY
                   COLLEGE OF ENGINEERING AND TECHNOLOGY
                   SRM INSTITUTE OF SCIENCE AND TECHNOLOGY
```

---

## TABLE OF CONTENTS

1. [Abstract](#abstract)
2. [1. Introduction & Theoretical Motivation](#1-introduction--theoretical-motivation)
   - [1.1 Problem Statement](#11-problem-statement)
   - [1.2 The Case for Formal Language and Automata Theory (FLA)](#12-the-case-for-formal-language-and-automata-theory-fla)
   - [1.3 Motivation and Objectives](#13-motivation-and-objectives)
   - [1.4 Scope and Limitations](#14-scope-and-limitations)
3. [2. Literature Survey & Theoretical Foundation](#2-literature-survey--theoretical-foundation)
   - [2.1 Classical Automata in Industrial and Cyber-Physical Control](#21-classical-automata-in-industrial-and-cyber-physical-control)
   - [2.2 Comparative Analysis: DFA vs. Heuristic vs. Machine Learning Models](#22-comparative-analysis-dfa-vs-heuristic-vs-machine-learning-models)
4. [3. Methodology & Mathematical Formalization](#3-methodology--mathematical-formalization)
   - [3.1 Sensor Data Abstraction and Discretization](#31-sensor-data-abstraction-and-discretization)
   - [3.2 Formal 5-Tuple Definition of the DFA](#32-formal-5-tuple-definition-of-the-dfa)
   - [3.3 State Descriptions ($Q$)](#33-state-descriptions-q)
   - [3.4 Input Alphabet and Event Semantics ($\Sigma$)](#34-input-alphabet-and-event-semantics-sigma)
   - [3.5 Complete State Transition Table ($\delta$)](#35-complete-state-transition-table-delta)
   - [3.6 State Transition Logic and Safety Latching Rules](#36-state-transition-logic-and-safety-latching-rules)
   - [3.7 State Transition Diagram](#37-state-transition-diagram)
5. [4. System Implementation & Software Architecture](#4-system-implementation--software-architecture)
   - [4.1 System Components and Architecture](#41-system-components-and-architecture)
   - [4.2 Discretization and DFA Dispatch Pseudocode](#42-discretization-and-dfa-dispatch-pseudocode)
   - [4.3 Implementation Details](#43-implementation-details)
6. [5. Experimental Results & Validation Scenarios](#5-experimental-results--validation-scenarios)
   - [5.1 Demonstration Scenarios and Execution Traces](#51-demonstration-scenarios-and-execution-traces)
   - [5.2 Automated Test Suite Results](#52-automated-test-suite-results)
   - [5.3 Terminal Simulation Output Evidence](#53-terminal-simulation-output-evidence)
7. [6. Discussion & Formal Analysis](#6-discussion--formal-analysis)
   - [6.1 Proof of Determinism and Completeness](#61-proof-of-determinism-and-completeness)
   - [6.2 Time and Space Complexity Analysis](#62-time-and-space-complexity-analysis)
   - [6.3 Comparison with Non-Deterministic Models (NFA)](#63-comparison-with-non-deterministic-models-nfa)
   - [6.4 Distinguishing Abstract DFA Models from Production Electrical Hardware](#64-distinguishing-abstract-dfa-models-from-production-electrical-hardware)
8. [7. Conclusion & Future Scope](#7-conclusion--future-scope)
   - [7.1 Conclusion](#71-conclusion)
   - [7.2 Future Scope & Extensions](#72-future-scope--extensions)
9. [8. References](#8-references)

---

## ABSTRACT

In modern residential cyber-physical energy systems, managing distributed energy resources (DER)—including rooftop photovoltaic arrays, lithium-ion battery storage, and dynamic residential loads—demands high-integrity control logic. While probabilistic machine learning algorithms and heuristic rule engines are widely deployed for long-term forecasting, they exhibit stochastic failure modes, unverified edge-case state spaces, and race conditions that are intolerable in physical electrical switching infrastructure. 

This project formulates, designs, implements, and validates a **Deterministic Finite Automaton (DFA)** for smart-home energy automation controllers. Continuous multidimensional sensor telemetry—comprising instantaneous load demand, solar irradiance levels, battery state of charge (SoC), and hardware fault trip lines—is mapped via a deterministic discretization function $f: \mathbb{R}^n \times \{0,1\}^m \to \Sigma$ onto a formal discrete input alphabet $\Sigma = \{ \text{NORMAL}, \text{HIGH\_DEMAND}, \text{SOLAR\_AVAILABLE}, \text{LOW\_BATTERY}, \text{SAFETY\_ALERT}, \text{RESET} \}$. The controller is formalized as a rigorous 5-tuple machine $M = (Q, \Sigma, \delta, q_0, F)$ comprising five distinct operational states ($Q = \{ \text{IDLE}, \text{NORMAL\_OPERATION}, \text{SOLAR\_PRIORITY}, \text{ENERGY\_SAVING}, \text{SAFETY\_SHUTDOWN} \}$) and an inspectable, total state transition matrix $\delta$ containing $|Q| \times |\Sigma| = 30$ transitions.

The automaton enforces fail-safe safety latching: upon asserting an emergency safety alert, the controller locks into $\text{SAFETY\_SHUTDOWN}$, ignoring all operational and renewable inputs until a supervised, operator-authorized $\text{RESET}$ transitions the machine back to quiescent standby ($\text{IDLE}$). The system is implemented in Python 3 without external opaque frameworks, featuring an interactive CLI simulator, a graphical state diagram generator, and a comprehensive automated test suite of 27 unit tests achieving 100% test passage. Theoretical complexity analysis confirms strict $O(1)$ constant time transition execution and $O(1)$ bounded memory overhead, proving that formal language models provide mathematically verifiable, race-condition-free foundations for embedded microcontrollers in smart energy automation.

---

## 1. INTRODUCTION & THEORETICAL MOTIVATION

### 1.1 Problem Statement
Residential energy infrastructure is experiencing unprecedented decentralization. Modern households increasingly integrate multi-source microgrids incorporating grid utility feeds, rooftop photovoltaic (PV) generation, stationary battery storage units, and intermittent high-draw appliances (e.g., heat pumps, electric vehicle supply equipment). Coordinating these distributed energy resources requires continuous supervisory decision-making:
1. When renewable generation is abundant, local solar consumption must be maximized.
2. During periods of peak grid tariff or excessive aggregate load, non-critical appliances must be curtailed (demand response).
3. If battery reserves deplete, storage degradation must be averted by shedding loads.
4. If electrical abnormalities arise (e.g., thermal runaway, circuit overload, line-to-ground faults), all power paths must be de-energized instantaneously.

Conventional home automation systems predominantly rely on ad-hoc nested conditional scripts (`if-else` cascades) or unverified heuristic timers. In multi-sensor environments, ad-hoc state implementations suffer from:
- **Unhandled Edge Cases:** Unforeseen event orderings result in undefined or dangling operational states.
- **Race Conditions:** Simultaneous sensor triggers cause erratic contactor cycling (chattering).
- **Safety Lockout Violations:** Inadvertent re-energization of damaged circuits while a thermal or electrical fault condition remains physically unmitigated.

### 1.2 The Case for Formal Language and Automata Theory (FLA)
Formal Languages and Automata Theory provides the rigorous mathematical framework needed to guarantee safety and liveness in cyber-physical systems (CPS) and industrial supervisory control:
1. **Mathematical Determinism:** For any system configuration $q \in Q$ and sensor event $\sigma \in \Sigma$, the system transitions to exactly one next state ($\delta(q, \sigma)$). Superposition and ambiguity are mathematically impossible.
2. **Deterministic Response Time ($O(1)$):** Microcontrollers governing electrical switchgear (e.g., ARM Cortex-M, ESP32) operate under hard real-time deadlines. A DFA transition executes via a direct table lookup in $O(1)$ constant time with negligible memory footprint, avoiding the latency and memory unpredictability of statistical neural networks.
3. **Formal Verifiability & Reachability Analysis:** The entire state space ($|Q| = 5$) and transition domain ($|Q \times \Sigma| = 30$) can be completely enumerated and verified against safety invariants, proving that unsafe states cannot be bypassed.

### 1.3 Motivation and Objectives
The objective of this project is to bridge formal language theory and practical cyber-physical energy automation by designing, implementing, and verifying an academically rigorous DFA controller. The project achieves the following milestones:
- Formulate the complete mathematical 5-tuple $M = (Q, \Sigma, \delta, q_0, F)$.
- Construct an explicit, 30-entry total state transition function $\delta: Q \times \Sigma \to Q$.
- Implement the controller in Python 3 using type hints and object-oriented abstractions.
- Develop an interactive command-line simulator capable of processing discrete strings and continuous telemetry.
- Generate an academic state transition diagram with formal notation.
- Validate the system against at least 8 distinct operational scenarios and edge cases.
- Prove time and space complexity and verify transition determinism through automated tests.

### 1.4 Scope and Limitations
- **Scope:** This project models the supervisory discrete-event control logic of a residential energy controller. It formalizes state transitions, sensor discretization, and safety latching.
- **Limitations:** The controller operates in discrete logical time over abstract event symbols. It simulates power control commands but does not interface directly with physical high-voltage contactors, pulse-width modulation (PWM) inverter drivers, or real-time AC phase synchronization hardware.

---

## 2. LITERATURE SURVEY & THEORETICAL FOUNDATION

### 2.1 Classical Automata in Industrial and Cyber-Physical Control
Finite state machines (FSMs), originally formalized by McCulloch, Pitts, Rabin, and Scott, have served as the foundational bedrock of computing, lexical analysis, synchronous sequential logic, and industrial Programmable Logic Controllers (PLCs). In cyber-physical supervisory control theory (formalized by Ramadge and Wonham in 1989), continuous physical dynamics are discretized into plant events, and a supervisory automaton restricts plant behavior to enforce safety specifications.

In energy management systems (EMS), supervisory controllers coordinate state transitions between grid-tied, islanded, battery-backup, and peak-shaving modes. Formalizing these transitions as a Deterministic Finite Automaton (DFA) guarantees that the controller recognizes only valid sequences of energy transitions and traps any hazardous sequence into an absorbing safety lockout.

### 2.2 Comparative Analysis: DFA vs. Heuristic vs. Machine Learning Models

| Evaluation Metric | Deterministic Finite Automaton (DFA) | Heuristic / Nested If-Else | Machine Learning / Neural Models |
| :--- | :--- | :--- | :--- |
| **Behavioral Determinism** | **100% Guaranteed**; exactly one transition per input. | High in small scripts, but degrades rapidly with scale. | Probabilistic / Stochastic; non-deterministic predictions. |
| **State Memory & History** | Explicitly tracked via discrete states ($Q$). | Implicitly scattered across flag variables. | Implicitly embedded in hidden weights/vectors. |
| **Computational Complexity** | **$O(1)$ time, $O(1)$ auxiliary space** per event. | $O(1)$ time, but prone to deeply nested branches. | $O(N \cdot M)$ matrix operations; high compute/memory. |
| **Safety Verification** | **Mathematically provable**; exhaustive state reachability. | Difficult to verify; susceptible to unhandled combinations. | Black-box behavior; vulnerable to adversarial/out-of-distribution drift. |
| **Embedded Suitability** | Runs on ultra-low-power microcontrollers (e.g., PIC, ESP32). | Feasible on microcontrollers. | Requires high-end edge accelerators or cloud offloading. |

---

## 3. METHODOLOGY & MATHEMATICAL FORMALIZATION

### 3.1 Sensor Data Abstraction and Discretization
Continuous physical sensors sample analog quantities over real-valued domains:
- Aggregate household demand $P_{\text{demand}} \in \mathbb{R}^+$ (kilowatts, kW)
- Solar irradiance $I_{\text{solar}} \in \mathbb{R}^+$ (watts per square meter, $\text{W/m}^2$)
- Battery State of Charge $\text{SoC} \in [0, 100]$ (%)
- Electrical safety trip circuit $\text{Trip}_{\text{hw}} \in \{0, 1\}$ (Boolean)
- Supervised operator reset signal $\text{Reset}_{\text{cmd}} \in \{0, 1\}$ (Boolean)

To bridge continuous observations into the formal language framework, a deterministic discretization function $f: \mathbb{R}^3 \times \{0,1\}^2 \to \Sigma$ evaluates sensor inputs according to strict hierarchical precedence:

$$f(P_{\text{demand}}, I_{\text{solar}}, \text{SoC}, \text{Trip}_{\text{hw}}, \text{Reset}_{\text{cmd}}) = \begin{cases}
\text{SAFETY\_ALERT} & \text{if } \text{Trip}_{\text{hw}} = 1 \\
\text{RESET} & \text{else if } \text{Reset}_{\text{cmd}} = 1 \\
\text{HIGH\_DEMAND} & \text{else if } P_{\text{demand}} > 4.5\text{ kW} \\
\text{LOW\_BATTERY} & \text{else if } \text{SoC} < 25.0\% \\
\text{SOLAR\_AVAILABLE} & \text{else if } I_{\text{solar}} \ge 300\text{ W/m}^2 \\
\text{NORMAL} & \text{otherwise}
\end{cases}$$

### 3.2 Formal 5-Tuple Definition of the DFA
The smart-home energy controller is formalized as a deterministic finite automaton:

$$M = (Q, \Sigma, \delta, q_0, F)$$

where:
1. **$Q$:** Finite set of 5 internal controller states.
2. **$\Sigma$:** Finite input alphabet of 6 discrete event tokens.
3. **$\delta$:** Total deterministic transition function $\delta: Q \times \Sigma \to Q$.
4. **$q_0$:** Designated initial state, $q_0 = \text{IDLE}$.
5. **$F$:** Set of accepting states, $F = \{ \text{IDLE}, \text{NORMAL\_OPERATION}, \text{SOLAR\_PRIORITY}, \text{ENERGY\_SAVING} \}$.

### 3.3 State Descriptions ($Q$)
The state set $Q = \{ q_0, q_1, q_2, q_3, q_4 \}$ models the physical operational phases:
- **$q_0$ (`IDLE`):** Quiescent standby state upon controller initialization. Power contactors remain open; the system monitors sensor telemetry before dispatching energy.
- **$q_1$ (`NORMAL_OPERATION`):** Standard grid-tied energy delivery. Household consumption is balanced within nominal utility parameters.
- **$q_2$ (`SOLAR_PRIORITY`):** Green eco-dispatch mode. Rooftop solar generation is prioritized to power household circuits and charge battery storage.
- **$q_3$ (`ENERGY_SAVING`):** Demand response / peak shaving mode. Triggered by either excessive load demand ($>4.5\text{ kW}$) or low battery reserves ($<25\%$). Non-essential loads are shed.
- **$q_4$ (`SAFETY_SHUTDOWN`):** Emergency fail-safe isolation latch. Triggered by any electrical abnormality. All contactors open to isolate the home.

### 3.4 Input Alphabet and Event Semantics ($\Sigma$)
The input alphabet $\Sigma = \{ \text{NORMAL}, \text{HIGH\_DEMAND}, \text{SOLAR\_AVAILABLE}, \text{LOW\_BATTERY}, \text{SAFETY\_ALERT}, \text{RESET} \}$ is represented by single-character formal tokens $\Sigma_{\text{token}} = \{ N, H, S, B, A, R \}$:
- **$N$ (`NORMAL`):** Nominal steady-state consumption within configured capacity.
- **$H$ (`HIGH_DEMAND`):** Aggregate load exceeds configured capacity threshold.
- **$S$ (`SOLAR_AVAILABLE`):** Sufficient solar generation available to power circuits.
- **$B$ (`LOW_BATTERY`):** Battery state of charge drops below reserve threshold.
- **$A$ (`SAFETY_ALERT`):** Emergency safety fault (thermal, over-current, short circuit).
- **$R$ (`RESET`):** Supervised operator or self-test reset command.

### 3.5 Complete State Transition Table ($\delta$)
Every cell in the matrix $\delta: Q \times \Sigma \to Q$ contains exactly one destination state, guaranteeing completeness and determinism:

| State ($q \in Q$) | $N$ (`NORMAL`) | $H$ (`HIGH_DEMAND`) | $S$ (`SOLAR_AVAILABLE`) | $B$ (`LOW_BATTERY`) | $A$ (`SAFETY_ALERT`) | $R$ (`RESET`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$\to q_0$ (`IDLE`)** | $q_1$ | $q_3$ | $q_2$ | $q_0$ | $q_4$ | $q_0$ |
| **$* q_1$ (`NORMAL_OPERATION`)** | $q_1$ | $q_3$ | $q_2$ | $q_3$ | $q_4$ | $q_0$ |
| **$* q_2$ (`SOLAR_PRIORITY`)** | $q_1$ | $q_3$ | $q_2$ | $q_3$ | $q_4$ | $q_0$ |
| **$* q_3$ (`ENERGY_SAVING`)** | $q_1$ | $q_3$ | $q_2$ | $q_3$ | $q_4$ | $q_0$ |
| **$q_4$ (`SAFETY_SHUTDOWN`)** | $q_4$ | $q_4$ | $q_4$ | $q_4$ | $q_4$ | $q_0$ |

*Notation:* $\to$ indicates initial state $q_0$; $*$ indicates accepting states in $F = \{q_0, q_1, q_2, q_3\}$.

### 3.6 State Transition Logic and Safety Latching Rules
1. **Startup Dispatch:** From quiescent standby $q_0$, receiving $N$ initiates standard grid delivery ($q_1$), $S$ activates solar harvesting ($q_2$), and $H$ immediately engages load-shedding ($q_3$).
2. **Solar Switching Invariance:** Whenever renewable harvest is signaled ($S$), healthy states $q_0, q_1, q_3$ transition to $q_2$, while $q_2$ self-loops.
3. **Curtailment Invariance:** Whenever load exceeds threshold ($H$), healthy states transition to $q_3$ to protect microgrid capacity.
4. **Emergency Trip Invariance:** From **any** state $q \in Q$, assertion of $A$ (`SAFETY_ALERT`) forces an immediate, unconditional transition:
   $$\forall q \in Q, \quad \delta(q, A) = q_4$$
5. **Fail-Safe Lockout Latching:** Once in $q_4$ (`SAFETY_SHUTDOWN`), the machine exhibits strict latching invariance:
   $$\forall \sigma \in \{ N, H, S, B, A \}, \quad \delta(q_4, \sigma) = q_4$$
   Normal fluctuations in sunlight, demand, or battery charge cannot clear the fault condition.
6. **Supervised Recovery Rule:** The only transition out of $q_4$ requires the authorized token $R$ (`RESET`), and its destination is strictly $q_0$ (`IDLE`):
   $$\delta(q_4, R) = q_0$$
   This prevents unsafe direct transitions to energized states ($q_1, q_2$), forcing the controller to evaluate system parameters from a zero-load baseline.

### 3.7 State Transition Diagram

```
                 +-----------------------------------+
                 |         q1: NORMAL_OP             |<----+
                 |         (Grid Active)             |     |
                 +-----------------------------------+     |
                   ^   |              |            ^       |
                 N |   | S          H | B        N |       |
                   |   v              v            |       |
+-------+  start +-----------------------------------+     |
| START |=======>|            q0: IDLE               |     |
+-------+        |            (Standby)              |     |
                 +-----------------------------------+     |
                   |   ^              ^            |       |
                 H |   | R (Recovery) | R          | S     |
                   v   |              |            v       |
                 +-----------------------------------+     |
                 |       q3: ENERGY_SAVING           |     |
                 |         (Curtailment)             |     |
                 +-----------------------------------+     |
                   |                                       |
                   | A (Emergency Trip from ALL states)     |
                   v                                       |
                 +-----------------------------------+     |
                 |       q4: SAFETY_SHUTDOWN         |     |
                 |        (Lockout Latched)          |     |
                 +-----------------------------------+     |
                   |               |                       |
                   | [N,H,S,B,A]   +---------- R ----------+
                   +--(Latch)--> q4           (To q0 Standby)
```

The high-resolution state diagram rendered in `docs/state_diagram.png` visualizes all double-circle accepting states, single-circle fault states, directed edges, and transition labels matching the formal table.

---

## 4. SYSTEM IMPLEMENTATION & SOFTWARE ARCHITECTURE

### 4.1 System Components and Architecture
The software architecture is decoupled into distinct, modular subsystems:
1. **Core DFA Engine (`src/dfa_controller.py`):** Encapsulates the formal mathematical 5-tuple, immutable enumeration classes, transition table validation, single-step execution, and extended transition evaluation.
2. **Interactive Simulator (`src/simulator.py`):** Command-line simulation runner providing interactive event injection, batch string processing, full transition table rendering, and continuous sensor telemetry simulation.
3. **Diagram Generator (`src/visualize_dfa.py`):** Produces both standardized Graphviz DOT specifications and 300-DPI publication diagrams using Matplotlib.
4. **Test Suite (`tests/test_dfa_controller.py` & `tests/test_scenarios.py`):** Automated unit tests validating mathematical completeness, determinism, and 10 representative test scenarios.
5. **Scenario Data Store (`data/sample_scenarios.json`):** Machine-readable catalog of operational traces with formal justification.

### 4.2 Discretization and DFA Dispatch Pseudocode

```text
Algorithm 1: DiscretizeSensorTelemetryAndDispatch
Input  : Telemetry vector T = (P_demand, I_solar, SoC_batt, Trip_hw, Reset_cmd), Current State q
Output : Next State q', Acceptance Status Acc

1:  if Trip_hw == True then
2:      sigma <- InputSymbol.SAFETY_ALERT
3:  else if Reset_cmd == True then
4:      sigma <- InputSymbol.RESET
5:  else if P_demand > 4.5 then
6:      sigma <- InputSymbol.HIGH_DEMAND
7:  else if SoC_batt < 25.0 then
8:      sigma <- InputSymbol.LOW_BATTERY
9:  else if I_solar >= 300.0 then
10:     sigma <- InputSymbol.SOLAR_AVAILABLE
11: else
12:     sigma <- InputSymbol.NORMAL
13: end if

14: if (q, sigma) not in delta then
15:     raise InvalidTransitionError("Transition function undefined")
16: end if

17: q' <- delta[(q, sigma)]
18: Acc <- (q' in F)
19: return q', Acc
```

### 4.3 Implementation Details
- **Programming Language:** Python 3.12 (standard library utilized for core logic).
- **Type Safety:** Comprehensive type annotations (`typing.NamedTuple`, `typing.FrozenSet`, `typing.Dict`).
- **Data Encapsulation:** States and input symbols are represented as subclassed string enumerations (`ControllerState(str, Enum)`, `InputSymbol(str, Enum)`), ensuring syntax immutability and O(1) hash lookups.
- **Inspectable Transition Table:** The table is stored as an immutable dictionary mapping `Tuple[ControllerState, InputSymbol]` to `ControllerState`.

---

## 5. EXPERIMENTAL RESULTS & VALIDATION SCENARIOS

### 5.1 Demonstration Scenarios and Execution Traces
The automaton was evaluated across 10 representative operational scenarios spanning normal dispatch, renewable switching, load shedding, safety alert trips, lockout latches, repeated events, reset recoveries, and edge cases.

| Scenario ID | Category | Input Sequence | Formal State Trace | Final State | Accepted? |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **SCEN-01** | Normal Operation | `N, N, N` | $q_0 \to q_1 \to q_1 \to q_1$ | `NORMAL_OP` ($q_1$) | **YES** |
| **SCEN-02** | Solar Priority | `N, S, S, N` | $q_0 \to q_1 \to q_2 \to q_2 \to q_1$ | `NORMAL_OP` ($q_1$) | **YES** |
| **SCEN-03** | High Demand Peak | `N, H, H, N` | $q_0 \to q_1 \to q_3 \to q_3 \to q_1$ | `NORMAL_OP` ($q_1$) | **YES** |
| **SCEN-04** | Low Battery Depletion | `S, B, S` | $q_0 \to q_2 \to q_3 \to q_2$ | `SOLAR_PRIO` ($q_2$) | **YES** |
| **SCEN-05** | Safety Fault & Latch | `N, S, A, N, H` | $q_0 \to q_1 \to q_2 \to q_4 \to q_4 \to q_4$ | `SAFETY_SHUT` ($q_4$) | **NO** |
| **SCEN-06** | Supervised Reset | `N, A, R, N` | $q_0 \to q_1 \to q_4 \to q_0 \to q_1$ | `NORMAL_OP` ($q_1$) | **YES** |
| **SCEN-07** | Repeated Event Bursts | `H, H, H, S, S` | $q_0 \to q_3 \to q_3 \to q_3 \to q_2 \to q_2$ | `SOLAR_PRIO` ($q_2$) | **YES** |
| **SCEN-08** | Empty Sequence ($\epsilon$) | `(empty)` | $q_0$ | `IDLE` ($q_0$) | **YES** |
| **SCEN-09** | Fault During Curtailment | `H, A, S` | $q_0 \to q_3 \to q_4 \to q_4$ | `SAFETY_SHUT` ($q_4$) | **NO** |
| **SCEN-10** | Malformed Token Rejection | `N, ERR, N` | Parser Exception Raised | `None` | **NO** |

### 5.2 Automated Test Suite Results
The automated unit test suite (`tests/test_dfa_controller.py` and `tests/test_scenarios.py`) was executed in the test environment using Python's built-in `unittest` runner. 

```text
test_accepting_states_subset ......................................... ok
test_alphabet_cardinality ............................................ ok
test_dfa_determinism ................................................. ok
test_discretizer_priorities .......................................... ok
test_empty_sequence_acceptance ....................................... ok
test_energy_saving_transitions ....................................... ok
test_idle_state_transitions .......................................... ok
test_initial_state_definition ........................................ ok
test_normal_operation_transitions .................................... ok
test_rejection_of_invalid_symbols .................................... ok
test_reset_recovery_from_safety_shutdown ............................. ok
test_safety_alert_from_every_state ................................... ok
test_safety_lockout_latching_invariance .............................. ok
test_scenario_battery_depletion ...................................... ok
test_scenario_normal_operation ....................................... ok
test_scenario_peak_demand_shedding ................................... ok
test_scenario_repeated_events ........................................ ok
test_scenario_reset_recovery_acceptance .............................. ok
test_scenario_safety_alert_rejection ................................. ok
test_scenario_solar_priority ......................................... ok
test_soft_reset_from_operational_states .............................. ok
test_solar_priority_transitions ...................................... ok
test_state_set_cardinality ........................................... ok
test_symbol_case_insensitivity_and_whitespace ........................ ok
test_symbol_from_shorthand_token ..................................... ok
test_transition_table_completeness ................................... ok
test_all_json_scenarios (10 subtests evaluated) ...................... ok

----------------------------------------------------------------------
Ran 27 tests in 0.020s

OK (100% Pass Rate - 0 Failures, 0 Errors)
```

### 5.3 Terminal Simulation Output Evidence
Below is an excerpt from the execution harness demonstrating the real-time processing of Scenario 6 (Supervised Reset):

```text
Evaluating Input Sequence: 'N, A, R, N'
------------------------------------------------------------------------------
  Step 01: δ(IDLE (q0), NORMAL ('N')) --> NORMAL_OPERATION (q1)  [ACCEPTING]
  Step 02: δ(NORMAL_OPERATION (q1), SAFETY_ALERT ('A')) --> SAFETY_SHUTDOWN (q4)  [NON-ACCEPTING]
  Step 03: δ(SAFETY_SHUTDOWN (q4), RESET ('R')) --> IDLE (q0)  [ACCEPTING]
  Step 04: δ(IDLE (q0), NORMAL ('N')) --> NORMAL_OPERATION (q1)  [ACCEPTING]
------------------------------------------------------------------------------
State Sequence Trace: q0 -> q1 -> q4 -> q0 -> q1
Initial State       : IDLE (q0)
Final State         : NORMAL_OPERATION (q1)
Evaluation Outcome  : ACCEPTED (w ∈ L(M))
Summary             : ACCEPTED: System reached compliant operating state 'NORMAL_OPERATION' (q1 ∈ F).
```

---

## 6. DISCUSSION & FORMAL ANALYSIS

### 6.1 Proof of Determinism and Completeness
1. **Determinism:** A finite automaton is deterministic if and only if for every state $q \in Q$ and symbol $\sigma \in \Sigma$, $|\delta(q, \sigma)| = 1$. The state transition dictionary in `src/dfa_controller.py` maps each composite key `(state, symbol)` to a single unique state enumeration. The absence of multi-valued mappings or $\epsilon$-transitions guarantees 100% behavioral determinism.
2. **Completeness:** The domain of the transition function is the Cartesian product $Q \times \Sigma$. With $|Q| = 5$ and $|\Sigma| = 6$, the required size is $|\operatorname{dom}(\delta)| = 30$. The automated verification method `validate_dfa()` confirms that all 30 distinct pairs exist and map strictly into $Q$, preventing any runtime exceptions due to unhandled transitions.

### 6.2 Time and Space Complexity Analysis
- **Time Complexity:**
  - *Per Event Transition:* Transition computation consists of a Python hash-map lookup:
    $$\text{Time}(\delta(q, \sigma)) = O(1)$$
  - *Per Sequence of Length $n$:* For an input sequence $w = \sigma_1 \sigma_2 \dots \sigma_n$, the total time to compute $\delta^*(q_0, w)$ is strictly:
    $$\text{Time}(w) = O(n)$$
- **Space Complexity:**
  - *Transition Table:* Stores $|Q| \times |\Sigma| = 30$ entries. In memory, this occupies constant auxiliary space:
    $$\text{Space}(\delta) = O(|Q| \cdot |\Sigma|) = O(1)$$
  - *Runtime State:* Only the current state pointer ($O(1)$) is maintained during execution.
  - This bounded footprint demonstrates that the automaton can be flashed directly onto resource-constrained embedded microcontrollers (e.g., ATmega328P with 2 KB RAM) without dynamic heap allocation.

### 6.3 Comparison with Non-Deterministic Models (NFA)
Non-Deterministic Finite Automata (NFAs) permit multiple transitions from a single state-symbol pair ($\delta: Q \times \Sigma \to \mathcal{P}(Q)$) and spontaneous $\epsilon$-transitions. In theoretical computer science, NFAs are computationally equivalent to DFAs in language recognition ($L(\text{NFA}) = L(\text{DFA})$).

However, in cyber-physical systems and energy automation controllers, **NFAs are strictly unacceptable**:
- Physical actuators (e.g., high-voltage contactors, transfer relays) cannot exist in a superposition of states. A contactor cannot be simultaneously open and closed.
- Resolving non-deterministic branches requires backtracking or parallel state set tracking ($O(2^{|Q|})$), introducing execution latency and memory overhead that violate real-time embedded safety deadlines.

### 6.4 Distinguishing Abstract DFA Models from Production Electrical Hardware
It is vital to maintain academic honesty regarding the distinction between this formal DFA model and production smart-home controllers:
- **Simulated Outputs vs. Physical Actuation:** Acceptance in the formal DFA ($w \in L(M)$) indicates mathematical compliance with the state model. It does not certify that physical relay contacts did not weld shut or that electrical arc flash did not occur.
- **Analog Dynamics:** Real power systems involve continuous transients (voltage sags, frequency deviations, inrush currents, reactive power). The DFA acts as a high-level discrete supervisor, relying on lower-level analog hardware protection circuits (e.g., thermal-magnetic breakers, metal-oxide varistors) for sub-millisecond physical protection.

---

## 7. CONCLUSION & FUTURE SCOPE

### 7.1 Conclusion
This project successfully designed, formalized, implemented, and validated a Deterministic Finite Automaton (DFA) for smart-home energy automation controllers. By mapping multidimensional sensor readings into a discrete input alphabet and designing a complete 30-entry transition matrix across 5 operational states, the controller enforces mathematical determinism, fail-safe lockout latching, and controlled recovery. Evaluated across 10 operational scenarios and 27 automated unit tests, the system achieved a 100% pass rate with $O(1)$ constant-time transitions. The project demonstrates the practical value of Formal Languages and Automata Theory in establishing provably safe cyber-physical control architectures.

### 7.2 Future Scope & Extensions
1. **Mealy / Moore Machine Formulation:** Extend the DFA language recognizer into a transducer ($M = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$) that directly emits hardware actuation vectors (e.g., `ACTIVATE_INVERTER`, `TRIP_BREAKER_2`, `SOUND_ALARM`) along transition edges or state visits.
2. **Pushdown Automata (PDA) for Energy Quotas:** Incorporate a stack alphabet to count and regulate daily energy consumption allowances and cumulative battery discharge cycles.
3. **Timed and Hybrid Automata:** Integrate continuous differential equations modeling battery degradation and solar thermal heating using Timed Automata (e.g., UPPAAL) for formal model checking.
4. **Hardware Firmware Deployment:** Cross-compile the validated Python transition matrix into C/C++ firmware for direct deployment on an ESP32 or STM32 microcontroller interfaced with real current sensors and solid-state relays.

---

## 8. REFERENCES

1. **Hopcroft, J. E., Motwani, R., & Ullman, J. D.** (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson Education / Addison-Wesley.
2. **Sipser, M.** (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
3. **Ramadge, P. J., & Wonham, W. M.** (1989). "The Control of Discrete Event Systems." *Proceedings of the IEEE*, 77(1), 81–98.
4. **Cassandras, C. G., & Lafortune, S.** (2008). *Introduction to Discrete Event Systems* (2nd ed.). Springer Science & Business Media.
5. **International Electrotechnical Commission (IEC).** (2010). *IEC 61508: Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems*. IEC Standard.
6. **Python Software Foundation.** (2024). *Python 3.12 Standard Library Documentation: `enum`, `unittest`, `typing`*. https://docs.python.org/3/

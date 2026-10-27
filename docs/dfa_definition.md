# Formal Mathematical Specification: Deterministic Finite Automaton for Smart-Home Energy Automation Controllers

**Academic Course:** Formal Languages and Automata Theory (FLA)  
**Model Designation:** $M = (Q, \Sigma, \delta, q_0, F)$  

---

## 1. Mathematical 5-Tuple Definition

A deterministic finite automaton (DFA) is defined as a 5-tuple:

$$M = (Q, \Sigma, \delta, q_0, F)$$

where:
1. **$Q$** is a finite, non-empty set of internal controller states.
2. **$\Sigma$** is a finite, non-empty input alphabet of discrete sensor and operational events.
3. **$\delta$** is the deterministic transition function $\delta: Q \times \Sigma \to Q$.
4. **$q_0$** is the designated initial state ($q_0 \in Q$).
5. **$F$** is the set of accepting (final) states ($F \subseteq Q$).

---

## 2. State Set Definition ($Q$)

$$Q = \{ q_0, q_1, q_2, q_3, q_4 \}$$

| State Symbol | State Identifier | Operational Semantics | Power Stage Status |
| :---: | :--- | :--- | :--- |
| **$q_0$** | `IDLE` | Quiescent standby baseline; system initialized, power stage disconnected, monitoring telemetry. | Relays open; zero active load. |
| **$q_1$** | `NORMAL_OPERATION` | Standard grid-tied power delivery; household consumption within nominal threshold. | Grid contactor closed; standard circuits energized. |
| **$q_2$** | `SOLAR_PRIORITY` | Eco-harvest mode; rooftop photovoltaic generation prioritized for home loads and storage. | Solar inverter active; grid import minimized. |
| **$q_3$** | `ENERGY_SAVING` | Demand response / peak shaving / storage conservation; non-essential loads curtailed. | Secondary load breakers open; critical loads preserved. |
| **$q_4$** | `SAFETY_SHUTDOWN` | Emergency fail-safe isolation; critical thermal, surge, or short-circuit fault detected. | All power relays de-energized; emergency lockout latched. |

---

## 3. Input Alphabet ($\Sigma$)

$$\Sigma = \{ \text{NORMAL}, \text{HIGH\_DEMAND}, \text{SOLAR\_AVAILABLE}, \text{LOW\_BATTERY}, \text{SAFETY\_ALERT}, \text{RESET} \}$$

For compact formal traces and state diagrams, the alphabet is isomorphic to single-character tokens:
$$\Sigma_{\text{token}} = \{ N, H, S, B, A, R \}$$

| Token | Symbol Identifier | Discretization Event Semantics | Hardware Sensor Trigger Condition |
| :---: | :--- | :--- | :--- |
| **$N$** | `NORMAL` | Power demand within nominal bounds; no alerts. | $P_{\text{demand}} \le 4.5\text{ kW} \land I_{\text{solar}} < 300\text{ W/m}^2 \land \text{SoC} \ge 25\%$ |
| **$H$** | `HIGH_DEMAND` | Load demand exceeds configured threshold. | $P_{\text{demand}} > 4.5\text{ kW}$ |
| **$S$** | `SOLAR_AVAILABLE` | Solar irradiance exceeds operational threshold. | $I_{\text{solar}} \ge 300\text{ W/m}^2 \land P_{\text{demand}} \le 4.5\text{ kW}$ |
| **$B$** | `LOW_BATTERY` | Battery state of charge (SoC) depleted. | $\text{SoC}_{\text{battery}} < 25.0\%$ |
| **$A$** | `SAFETY_ALERT` | Abnormal hazard (thermal runaway, surge, short). | Hardware trip line asserted ($\text{Trip}_{\text{hw}} = \text{True}$) |
| **$R$** | `RESET` | Supervised operator manual/self-test recovery. | Supervised reset pushbutton ($\text{Reset}_{\text{cmd}} = \text{True}$) |

---

## 4. Initial State ($q_0$) and Accepting States ($F$)

### Initial State
$$q_0 = \text{IDLE}$$
Upon system power-on, the automaton initializes into quiescent standby state $q_0$.

### Accepting States Set
$$F = \{ q_0, q_1, q_2, q_3 \} = Q \setminus \{ q_4 \}$$

### Semantics of Formal Acceptance
In formal language theory, a sequence $w \in \Sigma^*$ is accepted by $M$ ($w \in L(M)$) if and only if the extended transition function evaluates to a state in $F$:

$$\delta^*(q_0, w) \in F$$

- **Accepted Sequences ($w \in L(M)$):** The sequence represents an operational history that leaves the controller in a healthy, safe, functioning state ($q_0, q_1, q_2, q_3$).
- **Rejected Sequences ($w \notin L(M)$):** The sequence drives the controller into an unrecovered emergency lockdown ($q_4$). Rejection formally denotes a safety fault trajectory requiring physical intervention.
- **Empty Sequence ($\epsilon$):** By inductive definition, $\delta^*(q_0, \epsilon) = q_0$. Since $q_0 \in F$, $\epsilon \in L(M)$ is accepted. This mathematically models an unperturbed power-on baseline: before disturbances manifest, the quiescent system is hazard-free.
- **Academic Boundary Notice:** Acceptance by this formal mathematical DFA confirms language membership under the formalized model; it does not constitute physical electrical certification of real power hardware.

---

## 5. Complete State Transition Table ($\delta: Q \times \Sigma \to Q$)

The transition function is total and deterministic, containing exactly $|Q| \times |\Sigma| = 5 \times 6 = 30$ entries.

| Current State ($q \in Q$) | $N$ (`NORMAL`) | $H$ (`HIGH_DEMAND`) | $S$ (`SOLAR_AVAILABLE`) | $B$ (`LOW_BATTERY`) | $A$ (`SAFETY_ALERT`) | $R$ (`RESET`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$\to q_0$ (`IDLE`)** | $q_1$ | $q_3$ | $q_2$ | $q_0$ | $q_4$ | $q_0$ |
| **$* q_1$ (`NORMAL_OPERATION`)** | $q_1$ | $q_3$ | $q_2$ | $q_3$ | $q_4$ | $q_0$ |
| **$* q_2$ (`SOLAR_PRIORITY`)** | $q_1$ | $q_3$ | $q_2$ | $q_3$ | $q_4$ | $q_0$ |
| **$* q_3$ (`ENERGY_SAVING`)** | $q_1$ | $q_3$ | $q_2$ | $q_3$ | $q_4$ | $q_0$ |
| **$q_4$ (`SAFETY_SHUTDOWN`)** | $q_4$ | $q_4$ | $q_4$ | $q_4$ | $q_4$ | $q_0$ |

*Notation:* $\to$ indicates the initial state ($q_0$); $*$ indicates an accepting state ($q \in F$).

---

## 6. Mathematical Safety & Liveness Theorems

### Theorem 1: Determinism
For all state-input pairs $(q, \sigma) \in Q \times \Sigma$, the transition relation $|\delta(q, \sigma)| = 1$.  
*Proof:* By inspection of the transition table, every cell contains exactly one singleton destination in $Q$. There are no $\epsilon$-transitions, empty entries, or multi-valued mappings. $\blacksquare$

### Theorem 2: Fail-Safe Lockout Invariance
Let $q = q_4$ (`SAFETY_SHUTDOWN`). For all operational input symbols $\sigma \in \Sigma \setminus \{\text{RESET}\}$, $\delta(q_4, \sigma) = q_4$.  
*Significance:* The machine cannot be tricked into re-energizing circuits by transient operational signals (e.g., sunrise `SOLAR_AVAILABLE` or load drop `NORMAL`) while in emergency shutdown.

### Theorem 3: Controlled Recovery Precedence
The only transition leaving $q_4$ is commanded by `RESET`, and its destination is strictly $q_0$ (`IDLE`):
$$\delta(q_4, \text{RESET}) = q_0$$
*Significance:* Hardware safety standards mandate that clearing a fault trip must return the controller to a de-energized standby state ($q_0$), forcing a fresh evaluation of load and safety conditions before power contactors can close.

---

## 7. Extended Transition Function ($\delta^*$)

The extended transition function $\delta^* : Q \times \Sigma^* \to Q$ is defined inductively:
1. **Basis:** $\delta^*(q, \epsilon) = q$
2. **Induction:** $\delta^*(q, wa) = \delta(\delta^*(q, w), a)$ for all $w \in \Sigma^*$ and $a \in \Sigma$.

Language recognized:
$$L(M) = \{ w \in \Sigma^* \mid \delta^*(q_0, w) \in F \}$$

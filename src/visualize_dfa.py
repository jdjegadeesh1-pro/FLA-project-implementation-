"""
State Transition Diagram Generator for Smart-Home Energy DFA.

Academic Course: Formal Languages and Automata Theory (FLA)
Module: State Diagram Rendering & Formal Graph Visualization
"""

from __future__ import annotations
import os
import shutil
import subprocess
import sys
from typing import Dict, List, Tuple

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dfa_controller import (
    ControllerState,
    InputSymbol,
    SmartHomeEnergyDFA,
    TRANSITION_TABLE,
)


def generate_dot_source(dfa: SmartHomeEnergyDFA) -> str:
    """
    Generates standard Graphviz DOT source matching the transition table δ exactly.
    Groups transitions between the same state pairs to ensure readable layout.
    """
    # Group transitions: (src, dst) -> list of symbols
    transitions: Dict[Tuple[ControllerState, ControllerState], List[str]] = {}
    for (src, sym), dst in dfa.delta.items():
        key = (src, dst)
        transitions.setdefault(key, []).append(sym.formal_token)

    dot_lines = [
        "digraph SmartHomeEnergyDFA {",
        '    rankdir=LR;',
        '    size="12,7";',
        '    node [fontname="Helvetica", fontsize=11, penwidth=1.5];',
        '    edge [fontname="Helvetica", fontsize=9, penwidth=1.2];',
        "",
        "    // Initial State Indicator",
        '    __start [shape=none, label="", width=0, height=0];',
        '    __start -> "q0\\n(IDLE)" [label="start", penwidth=1.8];',
        "",
        "    // Accepting States (Double Circles)",
        '    node [shape=doublecircle, color="#1b5e20", fillcolor="#e8f5e9", style=filled];',
        '    "q0\\n(IDLE)";',
        '    "q1\\n(NORMAL_OPERATION)";',
        '    "q2\\n(SOLAR_PRIORITY)";',
        '    "q3\\n(ENERGY_SAVING)";',
        "",
        "    // Non-Accepting Hazard State (Single Circle, Safety Alert / Lockout)",
        '    node [shape=circle, color="#b71c1c", fillcolor="#ffebee", style=filled];',
        '    "q4\\n(SAFETY_SHUTDOWN)";',
        "",
        "    // State Transitions",
    ]

    def fmt_label(state: ControllerState) -> str:
        return f'"{state.formal_symbol}\\n({state.value})"'

    for (src, dst), symbols in sorted(transitions.items(), key=lambda x: (x[0][0].value, x[0][1].value)):
        tokens_str = ", ".join(sorted(symbols))
        color = "#1565c0"
        if "A" in symbols:
            color = "#c62828"  # Safety trip alert
        elif "R" in symbols:
            color = "#6a1b9a"  # Reset
        dot_lines.append(f'    {fmt_label(src)} -> {fmt_label(dst)} [label="{tokens_str}", color="{color}"];')

    dot_lines.append("}")
    return "\n".join(dot_lines)


def render_diagram_matplotlib(output_png_path: str) -> None:
    """
    Renders an academic, publication-quality DFA state diagram using matplotlib.
    This guarantees 100% reliable generation even when Graphviz binary is absent.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 9)
    ax.axis("off")

    # Coordinates for states in a legible circular/hierarchical layout
    # q0 at left, q1 center-top, q2 right-top, q3 bottom-center, q4 center-isolated
    coords = {
        ControllerState.IDLE: (1.8, 4.5),
        ControllerState.NORMAL_OPERATION: (6.5, 7.0),
        ControllerState.SOLAR_PRIORITY: (11.8, 5.8),
        ControllerState.ENERGY_SAVING: (7.2, 2.0),
        ControllerState.SAFETY_SHUTDOWN: (12.2, 1.8),
    }

    state_titles = {
        ControllerState.IDLE: ("q0", "IDLE\n(Standby)", True),
        ControllerState.NORMAL_OPERATION: ("q1", "NORMAL_OP\n(Grid Active)", True),
        ControllerState.SOLAR_PRIORITY: ("q2", "SOLAR_PRIO\n(Renewable)", True),
        ControllerState.ENERGY_SAVING: ("q3", "ENERGY_SAV\n(Curtailment)", True),
        ControllerState.SAFETY_SHUTDOWN: ("q4", "SAFETY_SHUT\n(Lockout)", False),
    }

    # Draw states
    radius = 0.95
    for state, (x, y) in coords.items():
        q_code, label, is_accepting = state_titles[state]
        fill_color = "#e8f5e9" if is_accepting else "#ffebee"
        edge_color = "#2e7d32" if is_accepting else "#c62828"

        # Outer circle
        outer = patches.Circle((x, y), radius, facecolor=fill_color, edgecolor=edge_color, linewidth=2.5, zorder=3)
        ax.add_patch(outer)

        # Double circle for accepting states
        if is_accepting:
            inner = patches.Circle((x, y), radius - 0.12, facecolor="none", edgecolor=edge_color, linewidth=1.5, zorder=3)
            ax.add_patch(inner)

        # Text labels
        ax.text(x, y + 0.18, q_code, ha="center", va="center", fontsize=13, fontweight="bold", color="#1a237e", zorder=4)
        ax.text(x, y - 0.22, label, ha="center", va="center", fontsize=8.5, fontweight="semibold", color="#263238", zorder=4)

    # Start arrow pointing to q0
    ax.annotate(
        "start",
        xy=(coords[ControllerState.IDLE][0] - radius, coords[ControllerState.IDLE][1]),
        xytext=(coords[ControllerState.IDLE][0] - 2.0, coords[ControllerState.IDLE][1]),
        arrowprops=dict(facecolor="#0d47a1", edgecolor="#0d47a1", width=2, headwidth=8, shrink=0.05),
        ha="center", va="center", fontsize=11, fontweight="bold", color="#0d47a1", zorder=5
    )

    # Aggregated transitions between distinct state pairs
    # Explicit grouped list for clarity
    edges = [
        # (src, dst, rad, label, color, (offset_x, offset_y))
        (ControllerState.IDLE, ControllerState.NORMAL_OPERATION, 0.15, "N", "#1565c0", (0.0, 0.25)),
        (ControllerState.IDLE, ControllerState.SOLAR_PRIORITY, 0.35, "S", "#2e7d32", (0.0, 0.35)),
        (ControllerState.IDLE, ControllerState.ENERGY_SAVING, -0.15, "H", "#e65100", (0.0, -0.25)),
        (ControllerState.IDLE, ControllerState.SAFETY_SHUTDOWN, -0.35, "A", "#c62828", (0.0, -0.35)),

        (ControllerState.NORMAL_OPERATION, ControllerState.SOLAR_PRIORITY, 0.15, "S", "#2e7d32", (0.0, 0.25)),
        (ControllerState.NORMAL_OPERATION, ControllerState.ENERGY_SAVING, -0.1, "H, B", "#e65100", (0.2, 0.0)),
        (ControllerState.NORMAL_OPERATION, ControllerState.IDLE, -0.25, "R", "#6a1b9a", (0.0, -0.3)),
        (ControllerState.NORMAL_OPERATION, ControllerState.SAFETY_SHUTDOWN, 0.15, "A", "#c62828", (0.2, 0.2)),

        (ControllerState.SOLAR_PRIORITY, ControllerState.NORMAL_OPERATION, 0.15, "N", "#1565c0", (0.0, -0.25)),
        (ControllerState.SOLAR_PRIORITY, ControllerState.ENERGY_SAVING, 0.15, "H, B", "#e65100", (-0.25, 0.0)),
        (ControllerState.SOLAR_PRIORITY, ControllerState.IDLE, -0.45, "R", "#6a1b9a", (0.0, -0.35)),
        (ControllerState.SOLAR_PRIORITY, ControllerState.SAFETY_SHUTDOWN, -0.15, "A", "#c62828", (0.25, 0.0)),

        (ControllerState.ENERGY_SAVING, ControllerState.NORMAL_OPERATION, 0.2, "N", "#1565c0", (-0.3, 0.0)),
        (ControllerState.ENERGY_SAVING, ControllerState.SOLAR_PRIORITY, -0.15, "S", "#2e7d32", (0.25, 0.0)),
        (ControllerState.ENERGY_SAVING, ControllerState.IDLE, 0.15, "R", "#6a1b9a", (0.0, 0.25)),
        (ControllerState.ENERGY_SAVING, ControllerState.SAFETY_SHUTDOWN, 0.05, "A", "#c62828", (0.0, -0.25)),

        (ControllerState.SAFETY_SHUTDOWN, ControllerState.IDLE, 0.45, "R (Recover)", "#6a1b9a", (0.0, 0.35)),
    ]

    for src, dst, rad, lbl, col, (ox, oy) in edges:
        x1, y1 = coords[src]
        x2, y2 = coords[dst]
        ax.annotate(
            "",
            xy=(x2, y2), xycoords="data",
            xytext=(x1, y1), textcoords="data",
            arrowprops=dict(
                arrowstyle="-|>",
                color=col,
                lw=1.6,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=radius * 1.15,
                shrinkB=radius * 1.15,
            ),
            zorder=2,
        )
        # Midpoint label approximation
        mx = (x1 + x2) / 2.0 + ox
        my = (y1 + y2) / 2.0 + oy
        ax.text(
            mx, my, lbl,
            fontsize=8.5, fontweight="bold", color=col,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor=col, alpha=0.9, lw=0.8),
            ha="center", va="center", zorder=5,
        )

    # Self-loops
    self_loops = [
        (ControllerState.IDLE, "B, R", (coords[ControllerState.IDLE][0] - 0.7, coords[ControllerState.IDLE][1] + 1.1)),
        (ControllerState.NORMAL_OPERATION, "N", (coords[ControllerState.NORMAL_OPERATION][0], coords[ControllerState.NORMAL_OPERATION][1] + 1.3)),
        (ControllerState.SOLAR_PRIORITY, "S", (coords[ControllerState.SOLAR_PRIORITY][0] + 0.8, coords[ControllerState.SOLAR_PRIORITY][1] + 1.1)),
        (ControllerState.ENERGY_SAVING, "H, B", (coords[ControllerState.ENERGY_SAVING][0], coords[ControllerState.ENERGY_SAVING][1] - 1.3)),
        (ControllerState.SAFETY_SHUTDOWN, "N, H, S, B, A\n(Lockout)", (coords[ControllerState.SAFETY_SHUTDOWN][0] + 0.9, coords[ControllerState.SAFETY_SHUTDOWN][1] - 1.2)),
    ]

    for state, lbl, (lx, ly) in self_loops:
        x, y = coords[state]
        ax.annotate(
            "",
            xy=(x - 0.3, y + radius - 0.05 if ly > y else y - radius + 0.05),
            xytext=(x + 0.3, y + radius - 0.05 if ly > y else y - radius + 0.05),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#455a64",
                lw=1.4,
                connectionstyle="arc3,rad=-1.3" if ly > y else "arc3,rad=1.3",
            ),
            zorder=2,
        )
        ax.text(
            lx, ly, lbl,
            fontsize=7.5, fontweight="bold", color="#37474f",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#f5f5f5", edgecolor="#90a4ae", alpha=0.9, lw=0.7),
            ha="center", va="center", zorder=5,
        )

    # Academic Diagram Title & Formal 5-Tuple Box
    title_box = (
        "Deterministic Finite Automaton M = (Q, Σ, δ, q0, F)\n"
        "Q = {q0:IDLE, q1:NORMAL_OP, q2:SOLAR_PRIO, q3:ENERGY_SAV, q4:SAFETY_SHUT}\n"
        "Σ = {N:NORMAL, H:HIGH_DEMAND, S:SOLAR_AVAILABLE, B:LOW_BATTERY, A:SAFETY_ALERT, R:RESET}\n"
        "q0 = q0 (IDLE)  |  F = {q0, q1, q2, q3} (Accepting: Double Circles)  |  q4 ∉ F (Lockout)"
    )
    ax.text(
        6.5, 8.5, title_box,
        fontsize=9, family="monospace", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#e8eaf6", edgecolor="#3949ab", lw=1.2),
        zorder=6,
    )

    # Legend
    legend_text = (
        "TRANSITION LEGEND:\n"
        "• Green (S): Solar Prioritization\n"
        "• Blue (N): Nominal Grid Operation\n"
        "• Orange (H, B): Peak Load / Low Battery Curtailment\n"
        "• Red (A): Emergency Safety Trip to Lockdown\n"
        "• Purple (R): Supervised Recovery to Standby (q0)"
    )
    ax.text(
        0.2, 0.4, legend_text,
        fontsize=8, ha="left", va="bottom",
        bbox=dict(boxstyle="square,pad=0.4", facecolor="#ffffff", edgecolor="#78909c", lw=0.9),
        zorder=6,
    )

    plt.tight_layout()
    plt.savefig(output_png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[SUCCESS] High-resolution DFA state diagram rendered to: {output_png_path}")


def main() -> None:
    dfa = SmartHomeEnergyDFA()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    dot_file_path = os.path.join(docs_dir, "state_diagram.dot")
    png_file_path = os.path.join(docs_dir, "state_diagram.png")

    # 1. Save standard Graphviz .dot file
    dot_content = generate_dot_source(dfa)
    with open(dot_file_path, "w", encoding="utf-8") as f:
        f.write(dot_content)
    print(f"[SUCCESS] Saved formal Graphviz DOT source to: {dot_file_path}")

    # 2. Attempt rendering via system graphviz dot if installed
    dot_bin = shutil.which("dot")
    if dot_bin:
        try:
            cmd = [dot_bin, "-Tpng", dot_file_path, "-o", png_file_path]
            subprocess.run(cmd, check=True)
            print(f"[SUCCESS] Graphviz dot binary rendered diagram to: {png_file_path}")
            return
        except Exception as e:
            print(f"[INFO] System dot binary invocation failed ({e}), falling back to matplotlib renderer.")

    # 3. Direct matplotlib rendering (guaranteed publication-grade diagram)
    render_diagram_matplotlib(png_file_path)


if __name__ == "__main__":
    main()

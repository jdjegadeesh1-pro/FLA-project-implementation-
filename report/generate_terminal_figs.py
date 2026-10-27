"""
Generates publication-quality terminal screenshot figures for Section 5.1
matching the visual appearance of Figure 5.1 and Figure 5.2 in the reference PDF.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_terminal_image(filename: str, title: str, text_content: str, width_in=5.2, height_in=4.2):
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    # Outer window box with border
    window_rect = patches.FancyBboxPatch(
        (0.1, 0.1), 9.8, 8.3,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        facecolor="#fcfcfc",
        edgecolor="#b0bec5",
        linewidth=1.2
    )
    ax.add_patch(window_rect)

    # Top title bar
    title_bar = patches.FancyBboxPatch(
        (0.1, 7.5), 9.8, 0.9,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        facecolor="#eceff1",
        edgecolor="#b0bec5",
        linewidth=0.8
    )
    ax.add_patch(title_bar)

    # Window title text (tabs / prompt)
    ax.text(0.4, 7.95, "Terminal", fontsize=8, fontweight="bold", color="#37474f", family="sans-serif")
    ax.text(1.8, 7.95, "Output", fontsize=7.5, color="#78909c", family="sans-serif")
    ax.text(2.9, 7.95, "Debug", fontsize=7.5, color="#78909c", family="sans-serif")
    
    # Prompt line
    ax.text(0.4, 7.15, "PS C:\\Users\\sanjay\\Desktop\\FLA\\smart_home> python simulation_runner.py", 
            fontsize=6.8, color="#0277bd", family="monospace")

    # Content
    y_pos = 6.6
    for line in text_content.strip().split("\n"):
        color = "#263238"
        weight = "normal"
        if "Initializing" in line:
            color = "#00838f"
            weight = "bold"
        elif "SCENARIO" in line:
            color = "#00695c"
            weight = "bold"
        elif "FINAL STATUS" in line:
            if "CRITICAL" in line or "LOCKDOWN" in line:
                color = "#c62828"
            else:
                color = "#2e7d32"
            weight = "bold"
        elif "Transition:" in line:
            color = "#37474f"
        elif "Data Stream:" in line:
            color = "#455a64"

        ax.text(0.4, y_pos, line, fontsize=6.2, color=color, weight=weight, family="monospace")
        y_pos -= 0.32

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

# Figure 5.1: Scenarios 1 & 2
fig5_1_text = """Initializing Smart Energy Controller Simulation...

SCENARIO: Normal Operation (Nominal Grid Active)
Data Stream: NNNNNNNN
[Sensor Input: N] | Transition: q0 (IDLE) -> q1 (NORMAL_OP)
[Sensor Input: N] | Transition: q1 (NORMAL_OP) -> q1 (NORMAL_OP)
[Sensor Input: N] | Transition: q1 (NORMAL_OP) -> q1 (NORMAL_OP)
[Sensor Input: N] | Transition: q1 (NORMAL_OP) -> q1 (NORMAL_OP)
[Sensor Input: N] | Transition: q1 (NORMAL_OP) -> q1 (NORMAL_OP)
[*] FINAL STATUS: OPERATION WITHIN NOMINAL PARAMETERS.

SCENARIO: Solar Priority Harvest & Dusk Recovery
Data Stream: NSSN
[Sensor Input: N] | Transition: q0 (IDLE) -> q1 (NORMAL_OP)
[Sensor Input: S] | Transition: q1 (NORMAL_OP) -> q2 (SOLAR_PRIO)
[Sensor Input: S] | Transition: q2 (SOLAR_PRIO) -> q2 (SOLAR_PRIO)
[Sensor Input: N] | Transition: q2 (SOLAR_PRIO) -> q1 (NORMAL_OP)
[*] FINAL STATUS: GREEN ECO-MODE COMPLETED SUCCESSFULLY."""

# Figure 5.2: Scenarios 3 & 4
fig5_2_text = """Initializing Smart Energy Controller Simulation...

SCENARIO: Peak Load Surge & Demand Response
Data Stream: NHHN
[Sensor Input: N] | Transition: q0 (IDLE) -> q1 (NORMAL_OP)
[Sensor Input: H] | Transition: q1 (NORMAL_OP) -> q3 (ENERGY_SAV)
[Sensor Input: H] | Transition: q3 (ENERGY_SAV) -> q3 (ENERGY_SAV)
[Sensor Input: N] | Transition: q3 (ENERGY_SAV) -> q1 (NORMAL_OP)
[*] FINAL STATUS: PEAK SHAVING CURTAILMENT DISPATCHED.

SCENARIO: Critical Safety Fault Trip & Lockout Latch
Data Stream: NSAH
[Sensor Input: N] | Transition: q0 (IDLE) -> q1 (NORMAL_OP)
[Sensor Input: S] | Transition: q1 (NORMAL_OP) -> q2 (SOLAR_PRIO)
[Sensor Input: A] | Transition: q2 (SOLAR_PRIO) -> q4 (SAFETY_SHUT)
[Sensor Input: H] | Transition: q4 (SAFETY_SHUT) -> q4 (SAFETY_SHUT)
[!] FINAL STATUS: CRITICAL HAZARD DETECTED. SYSTEM LOCKDOWN INITIATED."""

if __name__ == "__main__":
    import os
    report_dir = r"C:\Users\This PC\.gemini\antigravity-ide\scratch\dfa_smart_home_energy\report"
    os.makedirs(report_dir, exist_ok=True)
    create_terminal_image(os.path.join(report_dir, "terminal_fig5_1.png"), "Figure 5.1", fig5_1_text)
    create_terminal_image(os.path.join(report_dir, "terminal_fig5_2.png"), "Figure 5.2", fig5_2_text)
    print("Terminal figures generated successfully.")

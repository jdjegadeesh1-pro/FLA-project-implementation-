"""
Generates the institutional SRM emblem and Tiruchirappalli banner
matching the bottom of Page 1 in the reference PDF.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_srm_logo(output_path: str):
    fig, ax = plt.subplots(figsize=(3.6, 1.4), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    # Circular crest on left
    crest_outer = patches.Circle((1.8, 2.5), 1.1, facecolor="#ffffff", edgecolor="#0d47a1", linewidth=2)
    crest_inner = patches.Circle((1.8, 2.5), 0.9, facecolor="#e3f2fd", edgecolor="#0d47a1", linewidth=1)
    ax.add_patch(crest_outer)
    ax.add_patch(crest_inner)
    
    # Book / lamp icon in crest
    ax.text(1.8, 2.45, "SRM", ha="center", va="center", fontsize=8, fontweight="bold", color="#0d47a1")

    # SRM text
    ax.text(3.4, 2.6, "SRM", fontsize=28, fontweight="bold", color="#0d47a1", family="sans-serif")
    ax.text(3.4, 2.15, "INSTITUTE OF SCIENCE & TECHNOLOGY", fontsize=5.8, fontweight="bold", color="#1565c0", family="sans-serif")
    ax.text(3.4, 1.75, "(Deemed to be University u/s 3 of UGC Act, 1956)", fontsize=4.8, color="#455a64", family="sans-serif")

    # Blue banner at bottom
    banner = patches.Rectangle((0.4, 0.4), 9.2, 0.9, facecolor="#0d47a1", edgecolor="none")
    ax.add_patch(banner)
    ax.text(5.0, 0.85, "T I R U C H I R A P P A L L I", ha="center", va="center", fontsize=10, fontweight="bold", color="#ffffff", family="sans-serif")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", transparent=False, facecolor="#ffffff", dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_srm_logo(r"C:\Users\This PC\.gemini\antigravity-ide\scratch\dfa_smart_home_energy\report\srm_logo.png")
    print("SRM logo generated.")

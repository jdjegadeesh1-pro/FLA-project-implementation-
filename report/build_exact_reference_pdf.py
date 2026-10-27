"""
Publication-Quality Academic PDF Report Generator.
Strictly matches the 7-page institutional layout, typography, colors,
and section formatting of the SRM Institute of Science and Technology reference PDF.
Course: 21CSC301T - FORMAL LANGUAGE AND AUTOMATA
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    HRFlowable,
    KeepTogether,
)
from reportlab.pdfgen import canvas


class ExactReferenceCanvas(canvas.Canvas):
    """Generates the exact running header and footer from the reference PDF."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_exact_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_exact_decorations(self, page_count: int):
        # Page 1 is the Title Page (no headers/footers)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Footer format matching reference PDF:
        # Left: "Formalizing Smart-Home Energy Automation Controllers Using Finite Automata"
        # Right: "Page X of Y"
        doc_title_footer = "Formalizing Smart-Home Energy Automation Controllers Using Finite Automata"
        page_str = f"Page {self._pageNumber} of {page_count}"

        self.drawString(54, 30, doc_title_footer)
        self.drawRightString(541, 30, page_str)

        self.restoreState()


def generate_exact_pdf(output_pdf_path: str):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    report_dir = os.path.join(base_dir, "report")
    docs_dir = os.path.join(base_dir, "docs")

    diagram_png = os.path.join(docs_dir, "state_diagram.png")
    fig5_1_png = os.path.join(report_dir, "terminal_fig5_1.png")
    fig5_2_png = os.path.join(report_dir, "terminal_fig5_2.png")
    srm_logo_png = os.path.join(report_dir, "srm_logo.png")

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=46,
    )

    styles = getSampleStyleSheet()

    # Exact Typography Styles from Reference PDF
    primary_blue = colors.HexColor("#0d47a1")
    section_blue = colors.HexColor("#1565c0")
    text_dark = colors.HexColor("#1a1a1a")
    rule_blue = colors.HexColor("#2980b9")

    # Title Page Styles
    t_inst = ParagraphStyle("TInst", fontName="Helvetica-Bold", fontSize=13, leading=17, alignment=1, textColor=text_dark)
    t_sub = ParagraphStyle("TSub", fontName="Helvetica-Bold", fontSize=10.5, leading=15, alignment=1, textColor=text_dark)
    t_normal = ParagraphStyle("TNorm", fontName="Helvetica", fontSize=10, leading=14, alignment=1, textColor=text_dark)
    t_bold = ParagraphStyle("TBold", fontName="Helvetica-Bold", fontSize=10, leading=14, alignment=1, textColor=text_dark)
    t_report_title = ParagraphStyle("TRepTitle", fontName="Helvetica-Bold", fontSize=13, leading=18, alignment=1, textColor=text_dark)
    
    # Body Styles
    h1_style = ParagraphStyle("H1Exact", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=10, spaceAfter=4, textColor=text_dark, keepWithNext=True)
    h2_style = ParagraphStyle("H2Exact", fontName="Helvetica-Bold", fontSize=9.5, leading=13, spaceBefore=7, spaceAfter=3, textColor=section_blue, keepWithNext=True)
    body_style = ParagraphStyle("BodyExact", fontName="Helvetica", fontSize=8.5, leading=12, textColor=text_dark, alignment=4)
    bullet_style = ParagraphStyle("BulletExact", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=text_dark, leftIndent=12, firstLineIndent=-8)
    caption_style = ParagraphStyle("CapExact", fontName="Helvetica", fontSize=7.5, leading=10.5, textColor=text_dark, alignment=1)
    algo_code = ParagraphStyle("AlgoCode", fontName="Courier", fontSize=7.2, leading=9.5, textColor=colors.HexColor("#212121"))

    story = []

    # ========================================================================
    # PAGE 1: TITLE PAGE (Exact Match to Reference PDF Screenshot)
    # ========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", t_inst))
    story.append(Paragraph("TIRUCHIRAPPALLI - 621105", t_sub))
    story.append(Spacer(1, 24))
    story.append(Paragraph("B.Tech in Information Technology", t_sub))
    story.append(Spacer(1, 18))
    story.append(Paragraph("2026-2027", t_normal))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Course Code: 21CSC301T", t_normal))
    story.append(Paragraph("Course Name: FORMAL LANGUAGE AND AUTOMATA", t_bold))
    story.append(Spacer(1, 28))
    story.append(Paragraph("Report on", t_normal))
    story.append(Spacer(1, 6))
    story.append(Paragraph("FORMALIZING SMART-HOME ENERGY AUTOMATION SYSTEMS:<br/>SIMULATION AND ANALYSIS USING FINITE AUTOMATA", t_report_title))
    story.append(Spacer(1, 38))
    story.append(Paragraph("Submitted by", t_normal))
    story.append(Spacer(1, 10))

    # Student 1
    story.append(Paragraph("Name of the Student : S Sanjay", t_normal))
    story.append(Paragraph("Roll Number : RA2411008050002", t_normal))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Under the guidance of", t_normal))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Dr. Nagaraj P", t_bold))
    story.append(Spacer(1, 16))
    story.append(Paragraph("DEPARTMENT OF INFORMATION TECHNOLOGY", t_bold))
    story.append(Spacer(1, 16))
    # Student 2
    story.append(Paragraph("Name of the Student : G Venkatesh", t_normal))
    story.append(Paragraph("Roll Number : RA2411008050057", t_normal))
    story.append(Spacer(1, 32))

    # SRM Emblem / Logo
    if os.path.exists(srm_logo_png):
        story.append(Image(srm_logo_png, width=170, height=66))

    story.append(PageBreak())

    # ========================================================================
    # PAGE 2: TABLE OF CONTENTS (Exact Match with Blue Horizontal Line & Dot Leaders)
    # ========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle("TOCTitle", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=text_dark)))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=rule_blue, spaceAfter=14))

    toc_rows = [
        ["ABSTRACT", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["1. INTRODUCTION & THEORETICAL MOTIVATION", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["    1.1 Problem Statement", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["    1.2 The Case for Formal Language and Automata Theory (FLA)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["2. LITERATURE SURVEY & THEORETICAL FOUNDATION", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["    2.1 Classical Automata in Industrial Control", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["    2.2 Comparison: DFA vs. Heuristic / Black-Box Models", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["3. METHODOLOGY & MATHEMATICAL FORMALIZATION", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["    3.1 Sensor Data Abstraction and Discretization", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["    3.2 Formal 5-Tuple Definition of the DFA", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["    3.3 State Transition Table (δ)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "5"],
        ["    3.4 State Transition Logic and Safety Rules", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "5"],
        ["    3.5 State Transition Diagram", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "5"],
        ["4. SYSTEM IMPLEMENTATION & SOFTWARE ARCHITECTURE", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["    4.1 System Components", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["    4.2 Discretization Algorithm Pseudocode", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["5. EXPERIMENTAL RESULTS & VALIDATION SCENARIOS", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["    5.1 Simulation Output Screenshots & Experimental Evidence", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["6. DISCUSSION & COMPLEXITY ANALYSIS", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["    6.1 Time & Space Complexity", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["    6.2 Comparison with Non-Deterministic Models (NFA)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["7. CONCLUSION & FUTURE SCOPE", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["    7.1 Conclusion", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["    7.2 Future Scope", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
    ]

    t_toc = Table(toc_rows, colWidths=[240, 225, 22])
    t_toc.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#263238")),
        ("ALIGN", (2, 0), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ========================================================================
    # PAGE 3: ABSTRACT & CHAPTER 1
    # ========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "In modern residential and industrial smart microgrid infrastructures, coordinating distributed renewable energy "
        "and protecting battery storage from over-discharge is a safety-critical necessity. While machine learning heuristics "
        "and statistical classification models are frequently applied in environmental energy analysis, they exhibit non-deterministic "
        "failure modes and lack verifiable behavioral boundaries required by physical fail-safe hardware.<br/><br/>"
        "This project formulates an automated smart-home energy automation and safety response system utilizing a "
        "<b>Deterministic Finite Automaton (DFA)</b>. Continuous electrical and environmental sensor telemetry—encompassing "
        "household power demand, rooftop photovoltaic solar irradiance, battery state of charge (SoC), and hardware safety trip lines—is "
        "systematically mapped onto a discrete formal alphabet (Σ). The formalized 5-tuple machine <i>M = (Q, Σ, δ, q0, F)</i> "
        "models operational transitions from optimal baseline parameters (<i>q0</i>) through single-hazard warning thresholds (<i>q1, q2</i>) "
        "to automated emergency isolation and lockdown (<i>q3</i>). The model is mathematically validated through a dedicated "
        "state transition matrix and simulated using a modular Python execution engine. Verification across both synthetic boundary "
        "test vectors and empirical telemetry proves that the proposed automaton guarantees bounded <i>O(1)</i> constant runtime, "
        "bounded memory footprint, zero non-deterministic ambiguity, and deterministic containment of power surge hazards.",
        body_style
    ))
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. INTRODUCTION & THEORETICAL MOTIVATION", h1_style))
    story.append(Paragraph("1.1 Problem Statement", h2_style))
    story.append(Paragraph(
        "Residential power distribution circuits are susceptible to acute electrical surges (e.g., short-circuit faults, thermal runaway in inverters) "
        "and chronic capacity stress (e.g., grid peak overloads, battery deep discharge). Traditional automation workflows rely on either delayed periodic "
        "monitoring or thresholded sirens monitored by human occupants. Both approaches introduce latency that can result in catastrophic equipment damage "
        "or fire hazards before isolation breakers can be tripped.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.2 The Case for Formal Language and Automata Theory (FLA)", h2_style))
    story.append(Paragraph(
        "In industrial supervisory control and data acquisition (SCADA) and cyber-physical systems (CPS), automated control logic must satisfy strict safety and liveness properties:",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>1. Determinism:</b> Given any system state <i>q ∈ Q</i> and sensor observation <i>σ ∈ Σ</i>, the system must transition to exactly one valid configuration (<i>δ(q, σ)</i>).", bullet_style))
    story.append(Paragraph("<b>2. Deterministic Response Time (O(1)):</b> Embedded IoT microcontrollers operating along electrical switchboards (such as ESP32 or ARM Cortex-M microcontrollers) possess constrained computational budgets. An automaton transition executes in constant time (<i>O(1)</i>) and minimal memory, eliminating the computational overhead and latency associated with deep neural network inference.", bullet_style))
    story.append(Paragraph("<b>3. Formal Verifiability:</b> Unlike statistical \"black-box\" models, finite state automata can be proven correct through state reachability analysis, ensuring that unsafe states cannot be bypassed and recovery sequences adhere strictly to safety protocols.", bullet_style))
    story.append(PageBreak())

    # ========================================================================
    # PAGE 4: CHAPTER 2 & CHAPTER 3 (Through 3.2)
    # ========================================================================
    story.append(Paragraph("2. LITERATURE SURVEY & THEORETICAL FOUNDATION", h1_style))
    story.append(Paragraph("2.1 Classical Automata in Industrial Control", h2_style))
    story.append(Paragraph(
        "Automata theory, originally formalized by Rabin, Scott, and Chomsky, provides the mathematical underpinning for compiler construction, lexical parsing, and synchronous sequential circuits. In embedded control systems, a Deterministic Finite Automaton represents a formal language recognizer where:<br/>"
        "• The input string represents a temporal sequence of sensor observations.<br/>"
        "• The language accepted by the automaton <i>L(M)</i> represents the set of hazardous temporal signatures requiring system lockdown and emergency protective intervention.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Comparison: DFA vs. Heuristic / Black-Box Models", h2_style))
    comp_rows = [
        ["Property", "Deterministic Finite\nAutomata (DFA)", "Heuristic / Threshold Logic", "Machine Learning\nClassifiers"],
        ["Behavioral Determinism", "100% Guaranteed", "High, but prone to race\nconditions", "Probabilistic (Stochastic)"],
        ["State Memory / History", "Explicitly tracked via states\n(Q)", "Typically memoryless", "Implicitly modeled\n(RNN/LSTM)"],
        ["Resource Complexity", "O(1) time, O(1) space", "O(1) time, O(1) space", "O(N) high compute / GPU\nload"],
        ["Verification & Safety", "Mathematically provable", "Prone to unhandled edge\ncases", "Susceptible to adversarial\ndrift"],
    ]
    t_comp = Table(comp_rows, colWidths=[110, 125, 125, 127])
    t_comp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2742")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0bec5")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. METHODOLOGY & MATHEMATICAL FORMALIZATION", h1_style))
    story.append(Paragraph("3.1 Sensor Data Abstraction and Discretization", h2_style))
    story.append(Paragraph(
        "Physical sensors measure continuous, real-valued quantities (<i>x ∈ R<sup>+</sup></i>). To interface continuous telemetry with formal grammar, a discretization function <i>f : R<sup>n</sup> → Σ</i> maps multidimensional observations into discrete input tokens based on standard electrical safety and operational limits:<br/>"
        "• <b>Electrical Indicators:</b> Household load demand (<i>P</i> in kW) and battery charge (<i>B</i> in %).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>PowerHazard</i> = <b>True</b> if <i>P &gt; 4.5 ∨ B &lt; 25.0</i>; <b>False</b> otherwise.<br/>"
        "• <b>Environmental & Safety Indicators:</b> Solar irradiance (<i>S</i> in W/m²) and hardware fault trip (<i>F<sub>hw</sub></i>).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>CritHazard</i> = <b>True</b> if <i>F<sub>hw</sub> == 1</i>; <b>False</b> otherwise.<br/><br/>"
        "The formal alphabet is defined as <b>Σ = {0, b, c, x}</b>:<br/>"
        "• <b>0 (Nominal / Safe):</b> ¬PowerHazard ∧ ¬CritHazard<br/>"
        "• <b>b (Demand Warning):</b> PowerHazard ∧ ¬CritHazard<br/>"
        "• <b>c (Storage / Solar Warning):</b> ¬PowerHazard ∧ CritHazard_Minor<br/>"
        "• <b>x (Compound / Critical Hazard):</b> PowerHazard ∧ CritHazard",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Formal 5-Tuple Definition of the DFA", h2_style))
    story.append(Paragraph(
        "The smart-home controller is formalized as a Deterministic Finite Automaton <b>M = (Q, Σ, δ, q0, F)</b>, where:<br/>"
        "<b>1. Q (Finite Set of States):</b> Q = {q0, q1, q2, q3}<br/>"
        "&nbsp;&nbsp;• <b>q0 ( Safe ):</b> System operates normally. Household power distribution active.<br/>"
        "&nbsp;&nbsp;• <b>q1 ( Demand_Warning ):</b> Peak consumption anomaly detected. Auxiliary shedding modules activated.<br/>"
        "&nbsp;&nbsp;• <b>q2 ( Solar_Warning ):</b> Renewable generation deficit detected. Battery conservation activated.<br/>"
        "&nbsp;&nbsp;• <b>q3 ( Lockdown ):</b> Critical compound hazard or escalating overload detected. Main contactors shut, distribution halted, and emergency sirens engaged.",
        body_style
    ))
    story.append(PageBreak())

    # ========================================================================
    # PAGE 5: 3.3 TRANSITION TABLE, 3.4 RULES, 3.5 DIAGRAM
    # ========================================================================
    story.append(Paragraph("3.3 State Transition Table (δ)", h2_style))
    story.append(Paragraph("The complete behavior of the state transition function <i>δ : Q × Σ → Q</i> is defined as follows:", body_style))
    story.append(Spacer(1, 4))

    trans_rows = [
        ["Current State (q)", "Input 0 (Safe)", "Input b (Demand)", "Input c (Solar/Bat)", "Input x (Critical)"],
        ["→ q0 (Safe)", "q0", "q1", "q2", "q3"],
        ["q1 (Demand_Warning)", "q0", "q1", "q3", "q3"],
        ["q2 (Solar_Warning)", "q0", "q3", "q2", "q3"],
        ["* q3 (Lockdown)", "q0", "q3", "q3", "q3"],
    ]
    t_trans = Table(trans_rows, colWidths=[130, 90, 90, 90, 87])
    t_trans.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2742")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0bec5")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_trans)
    story.append(Spacer(1, 3))
    story.append(Paragraph("<i>Notation: → indicates the initial state (q0); * indicates an accept/final state (q3 ∈ F).</i>", caption_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.4 State Transition Logic and Safety Rules", h2_style))
    story.append(Paragraph("<b>1. Recovery Invariance:</b> If the system is in a warning state (<i>q1</i> or <i>q2</i>) and receives input <b>0</b> (nominal telemetry readings post-curtailment), it transitions back to <i>q0</i>, avoiding unnecessary shutdown.", bullet_style))
    story.append(Paragraph("<b>2. Compound Escalation Rule:</b> If the system is already coping with a demand hazard (<i>q1</i>) and subsequently receives a renewable deficit input <b>c</b>, the co-presence of both hazards escalates the automaton to <i>q3</i> (Lockdown).", bullet_style))
    story.append(Paragraph("<b>3. Symmetric Solar Escalation:</b> Similarly, if solar storage is degraded (<i>q2</i>) and a demand surge <b>b</b> is detected, the system immediately trips to <i>q3</i>.", bullet_style))
    story.append(Paragraph("<b>4. Direct Critical Shock:</b> Any detection of compound electrical shocks ( <b>x</b> ) transitions any state directly to <i>q3</i>.", bullet_style))
    story.append(Paragraph("<b>5. Lockdown Latching:</b> Once in <i>q3</i>, further hazard inputs ( <b>b, c, x</b> ) keep the machine in <i>q3</i>. Only a verified pure safe flushing sequence ( <b>0</b> ) can transition the system back to normal operation.", bullet_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.5 State Transition Diagram", h2_style))
    if os.path.exists(diagram_png):
        story.append(Image(diagram_png, width=440, height=210))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "<b>Figure 3.1:</b> Graphical representation of the Deterministic Finite Automaton <i>M = (Q, Σ, δ, q0, F)</i> illustrating safe baseline (<i>q0</i>), "
            "single-hazard warning states (<i>q1, q2</i>), compound escalation edges, and the accepting lockdown state (<i>q3</i>).",
            caption_style
        ))
    story.append(PageBreak())

    # ========================================================================
    # PAGE 6: CHAPTER 4 & CHAPTER 5
    # ========================================================================
    story.append(Paragraph("4. SYSTEM IMPLEMENTATION & SOFTWARE ARCHITECTURE", h1_style))
    story.append(Paragraph("4.1 System Components", h2_style))
    story.append(Paragraph("The software implementation consists of two core decoupled modules written in Python:", body_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>1. Automaton Engine ( smart_home_automaton.py ):</b> Encapsulates the formal mathematical 5-tuple, state validation, and transition processing via an O(1) lookup hash map.", bullet_style))
    story.append(Paragraph("<b>2. Simulation & Telemetry Runner ( simulation_runner.py ):</b> Handles CSV ingestion, floating-point thresholding, timed simulation loops, and terminal-based monitoring.", bullet_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 Discretization Algorithm Pseudocode", h2_style))
    
    # Bordered Algorithm Box matching reference PDF page 6
    algo_box_lines = [
        "<b>Algorithm 1: DiscretizeSensorTelemetry</b>",
        "",
        "<b>Input :</b> Row R with attributes (demand_kw, solar_irradiance, battery_soc, fault_trip)  <b>Output :</b> Symbol σ ∈ {0, b, c, x}",
        "1: power_hazard ← (R.demand_kw > 4.5) OR (R.battery_soc < 25.0)",
        "2: crit_hazard  ← (R.fault_trip == 1) OR (R.inverter_temp > 85.0)",
        "3:",
        "4: if power_hazard AND crit_hazard then",
        "5:     return 'x'",
        "6: else if power_hazard then",
        "7:     return 'b'",
        "8: else if crit_hazard then",
        "9:     return 'c'",
        "10: else",
        "11:    return '0'",
    ]
    algo_content = [Paragraph("<br/>".join(algo_box_lines), algo_code)]
    t_algo = Table([[algo_content]], colWidths=[487])
    t_algo.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#78909c")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t_algo)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. EXPERIMENTAL RESULTS & VALIDATION SCENARIOS", h1_style))
    story.append(Paragraph("The system was evaluated against four representative operational scenarios to verify both theoretical soundness and practical reliability:", body_style))
    story.append(Spacer(1, 6))

    scen_paras = [
        "<b>Scenario 1: Nominal Continuous Operation</b><br/>"
        "• <b>Input Stream:</b> <i>w1 = 0000000</i><br/>"
        "• <b>Trace:</b> <i>q0 →0 q0 →0 q0 →0 q0 →0 q0 →0 q0 →0 q0</i><br/>"
        "• <b>Result:</b> Machine remains in <i>q0</i>. Energy quality remains safe, demonstrating system stability.",

        "<b>Scenario 2: Transient Anomaly & Self-Healing</b><br/>"
        "• <b>Input Stream:</b> <i>w2 = 00b000</i><br/>"
        "• <b>Trace:</b> <i>q0 →0 q0 →0 q0 →b q1 →0 q0 →0 q0 →0 q0</i><br/>"
        "• <b>Result:</b> Temporary demand spike triggers <i>q1</i> (Demand Warning). Subsequent clean readings return the machine to <i>q0</i>, preventing false alarms.",

        "<b>Scenario 3: Compound Escalation to System Lockdown</b><br/>"
        "• <b>Input Stream:</b> <i>w3 = 00bcc</i><br/>"
        "• <b>Trace:</b> <i>q0 →0 q0 →0 q0 →b q1 →c q3 →c q3</i><br/>"
        "• <b>Result:</b> Arrival of solar/storage deficit token <b>c</b> during demand warning <i>q1</i> triggers immediate escalation into <i>q3</i> (Lockdown). Machine accepts the hazard sequence and latches safety mechanisms.",

        "<b>Scenario 4: Real-World Ingestion from Smart-Grid Telemetry Dataset</b><br/>"
        "• <b>Telemetry Source:</b> Smart-Home Energy Dataset ( residential_power.csv , 21 parameters).<br/>"
        "• <b>Generated Sequence (First 15 sample intervals):</b> <i>w4 = xxcxxxxxxxcxxxx</i><br/>"
        "• <b>Trace:</b> <i>q0 →x q3 →x q3 →c q3 … →x q3</i><br/>"
        "• <b>Result:</b> The system correctly identifies severe electrical short circuit present in the sample data, immediately transitioning to <i>q3</i> on the very first input symbol."
    ]

    for p in scen_paras:
        story.append(Paragraph(p, bullet_style))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ========================================================================
    # PAGE 7: TERMINAL SCREENSHOTS, TWO-COLUMN ANALYSIS, CONCLUSION
    # ========================================================================
    story.append(Paragraph("5.1 Simulation Output Screenshots & Experimental Evidence", h2_style))
    story.append(Paragraph(
        "The following figures illustrate the terminal output traces generated by the Python simulation engine "
        "( <b>simulation_runner.py</b> ), demonstrating real-time state transitions and status classifications across all four test scenarios.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Side-by-side Terminal Screenshots
    if os.path.exists(fig5_1_png) and os.path.exists(fig5_2_png):
        img1 = Image(fig5_1_png, width=238, height=175)
        img2 = Image(fig5_2_png, width=238, height=175)
        cap1 = Paragraph("<b>Figure 5.1:</b> Scenarios 1 & 2 Output. Nominal baseline (<i>q0</i>) and self-healing recovery from temporary spikes (<i>q0 → q1 → q0</i>).", caption_style)
        cap2 = Paragraph("<b>Figure 5.2:</b> Scenarios 3 & 4 Output. Compound escalation to lockdown (<i>q1 →c q3</i>) and validation on telemetry stream.", caption_style)

        t_figs = Table([[img1, img2], [cap1, cap2]], colWidths=[243, 244])
        t_figs.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(t_figs)

    story.append(Spacer(1, 8))
    story.append(Paragraph("6. DISCUSSION & COMPLEXITY ANALYSIS", h1_style))
    story.append(Spacer(1, 2))

    # Two-Column layout matching Page 7 of reference PDF
    col1_content = [
        Paragraph("6.1 Time & Space Complexity", h2_style),
        Paragraph("• <b>Time Complexity:</b> For an input string of length <i>n</i>, the automaton processes transitions in <i>O(n)</i> time overall, and exactly <b>O(1)</b> constant time per sensor read.", body_style),
        Spacer(1, 3),
        Paragraph("• <b>Space Complexity:</b> The transition function requires <i>O(|Q| × |Σ|) = 4 × 4 = 16</i> entries, occupying negligible memory (<b>O(1)</b> auxiliary space). This proves that the solution can be embedded directly onto low-power microcontrollers without external memory.", body_style),
    ]

    col2_content = [
        Paragraph("6.2 Comparison with Non-Deterministic Models (NFA)", h2_style),
        Paragraph("An NFA was intentionally rejected for this control architecture. In physical energy distribution, an actuator cannot be in a superposition of multiple states (e.g., partially closed and fully open simultaneously). A DFA guarantees a single unambiguous state at every discrete time step.", body_style),
    ]

    t_col = Table([[col1_content, col2_content]], colWidths=[240, 247])
    t_col.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("RIGHTPADDING", (0, 0), (0, -1), 10),
        ("LEFTPADDING", (1, 0), (1, -1), 10),
    ]))
    story.append(t_col)
    story.append(Spacer(1, 8))

    story.append(Paragraph("7. CONCLUSION & FUTURE SCOPE", h1_style))
    story.append(Paragraph("7.1 Conclusion", h2_style))
    story.append(Paragraph(
        "This project demonstrates the practical application of Formal Language and Automata Theory to cyber-physical smart-home energy automation systems. "
        "By translating real-world continuous data into a finite alphabet and a deterministic state transition model, we constructed a controller that delivers "
        "provable safety guarantees, instantaneous reaction to compound overload hazards, and resilience against spurious pipeline shutdowns.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("7.2 Future Scope", h2_style))
    story.append(Paragraph("1. <b>Mealy Machine Extension:</b> Transitioning from a DFA language recognizer to a Mealy/Moore Machine that emits discrete actuator commands (e.g., <code>OPEN_RELAY</code>, <code>ENABLE_INVERTER</code>, <code>ISOLATE_LOAD</code>) along transition edges.", bullet_style))
    story.append(Paragraph("2. <b>Pushdown Automata (PDA):</b> Incorporating a stack memory to track cumulative exposure durations and energy dosage levels over extended operational windows.", bullet_style))
    story.append(Paragraph("3. <b>Hardware Deployment:</b> Flashing the Python transition logic as C/C++ firmware onto ESP32 microcontrollers interfaced with physical current sensors and solid-state relays.", bullet_style))

    # Build PDF with ExactReferenceCanvas
    doc.build(story, canvasmaker=ExactReferenceCanvas)
    print(f"[SUCCESS] Exact 7-Page Academic Report PDF generated at: {output_pdf_path}")


if __name__ == "__main__":
    report_pdf = r"C:\Users\This PC\.gemini\antigravity-ide\scratch\dfa_smart_home_energy\report\project_report.pdf"
    generate_exact_pdf(report_pdf)

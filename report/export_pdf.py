"""
Academic Report PDF Generator for SRM Institute of Science and Technology.
Course: 21CSC301T - Formal Languages and Automata Theory (FLA)

Compiles the academic project report into a publication-quality PDF
matching the institutional format of the SRM IST Tiruchirappalli template.
"""

from __future__ import annotations
import os
import sys
from reportlab.lib.pagesizes import letter, A4
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


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page count (Page X of Y) and running headers."""

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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        # Suppress headers and footers on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#455a64"))

        # Running Header
        header_text = "Design and Implementation of DFA for Smart-Home Energy Automation"
        self.drawString(54, 800, header_text)
        self.setStrokeColor(colors.HexColor("#b0bec5"))
        self.setLineWidth(0.5)
        self.line(54, 794, 541, 794)

        # Running Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 36, footer_text)
        inst_text = "SRM Institute of Science and Technology - Department of Information Technology"
        self.drawString(54, 36, inst_text)
        self.line(54, 48, 541, 48)

        self.restoreState()


def build_academic_pdf(output_pdf_path: str, diagram_png_path: str) -> None:
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0d47a1")
    text_color = colors.HexColor("#212121")

    title_inst = ParagraphStyle(
        "CoverInst",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#1a237e"),
    )
    title_loc = ParagraphStyle(
        "CoverLoc",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#263238"),
    )
    title_course = ParagraphStyle(
        "CoverCourse",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#37474f"),
    )
    title_report_on = ParagraphStyle(
        "CoverReportOn",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=primary_color,
    )
    title_main = ParagraphStyle(
        "CoverMainTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#0d47a1"),
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        alignment=4,  # Justified
    )
    h1_style = ParagraphStyle(
        "Header1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "Header2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#1565c0"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )
    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1b1b1b"),
    )
    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        alignment=1,
    )

    story = []

    # ========================================================================
    # COVER PAGE (Matching SRM IST Template exactly)
    # ========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", title_inst))
    story.append(Paragraph("TIRUCHIRAPPALLI - 621105", title_loc))
    story.append(Spacer(1, 15))
    story.append(Paragraph("B.Tech in Information Technology", title_loc))
    story.append(Paragraph("2026-2027", title_course))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Course Code: 21CSC301T", title_course))
    story.append(Paragraph("Course Name: FORMAL LANGUAGE AND AUTOMATA", title_inst))
    story.append(Spacer(1, 35))
    story.append(Paragraph("Report on", title_course))
    story.append(Spacer(1, 5))
    story.append(
        Paragraph(
            "DESIGN AND IMPLEMENTATION OF A DETERMINISTIC FINITE AUTOMATON (DFA) FOR SMART-HOME ENERGY AUTOMATION CONTROLLERS",
            title_main,
        )
    )
    story.append(Spacer(1, 50))
    story.append(Paragraph("Submitted by", title_course))
    story.append(Spacer(1, 8))

    student_table_data = [
        [Paragraph("<b>Name of the Student :</b> [STUDENT NAME 1]", meta_style)],
        [Paragraph("<b>Roll Number :</b> [REGISTER NUMBER 1]", meta_style)],
        [Paragraph("<b>Name of the Student :</b> [STUDENT NAME 2]", meta_style)],
        [Paragraph("<b>Roll Number :</b> [REGISTER NUMBER 2]", meta_style)],
    ]
    t_stud = Table(student_table_data, colWidths=[400])
    t_stud.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(t_stud)

    story.append(Spacer(1, 40))
    story.append(Paragraph("Under the guidance of", title_course))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>[FACULTY GUIDE NAME, Ph.D.]</b>", meta_style))
    story.append(Paragraph("[Designation / Department of Information Technology]", title_course))

    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>DEPARTMENT OF INFORMATION TECHNOLOGY</b>", title_loc))
    story.append(Paragraph("COLLEGE OF ENGINEERING AND TECHNOLOGY", title_course))
    story.append(PageBreak())

    # ========================================================================
    # TABLE OF CONTENTS
    # ========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))

    toc_data = [
        ["ABSTRACT", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["1. INTRODUCTION & THEORETICAL MOTIVATION", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["   1.1 Problem Statement", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["   1.2 The Case for Formal Language and Automata Theory (FLA)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "3"],
        ["2. LITERATURE SURVEY & THEORETICAL FOUNDATION", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["   2.1 Classical Automata in Industrial Control", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["   2.2 Comparison: DFA vs. Heuristic / Black-Box Models", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["3. METHODOLOGY & MATHEMATICAL FORMALIZATION", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["   3.1 Sensor Data Abstraction and Discretization", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["   3.2 Formal 5-Tuple Definition of the DFA", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "4"],
        ["   3.3 State Transition Table (δ)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "5"],
        ["   3.4 State Transition Logic and Safety Rules", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "5"],
        ["   3.5 State Transition Diagram", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "5"],
        ["4. SYSTEM IMPLEMENTATION & SOFTWARE ARCHITECTURE", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["   4.1 System Components", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["   4.2 Discretization Algorithm Pseudocode", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["5. EXPERIMENTAL RESULTS & VALIDATION SCENARIOS", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "6"],
        ["   5.1 Simulation Output Traces & Experimental Evidence", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["6. DISCUSSION & COMPLEXITY ANALYSIS", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["   6.1 Time & Space Complexity", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["   6.2 Comparison with Non-Deterministic Models (NFA)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["7. CONCLUSION & FUTURE SCOPE", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
        ["8. REFERENCES", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "7"],
    ]

    t_toc = Table(toc_data, colWidths=[240, 210, 30])
    t_toc.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#37474f")),
            ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ])
    )
    story.append(t_toc)
    story.append(PageBreak())

    # ========================================================================
    # ABSTRACT & CHAPTER 1
    # ========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(
        Paragraph(
            "In modern residential smart-grid infrastructure, coordinating renewable solar energy, storage reserves, and fluctuating power demand requires verifiable, race-condition-free control logic. While statistical learning models are widely applied for forecasting, their non-deterministic failure modes and black-box nature are unsuitable for safety-critical power contactors. "
            "This project formulates an automated smart-home energy automation controller utilizing a <b>Deterministic Finite Automaton (DFA)</b>. Continuous sensor telemetry—encompassing power demand, solar irradiance, battery state of charge (SoC), and hardware safety trip lines—is mapped onto a discrete formal alphabet (Σ). The formalized 5-tuple machine <i>M = (Q, Σ, δ, q0, F)</i> models operational transitions from quiescent standby (<i>q0</i>) through standard grid delivery (<i>q1</i>), solar eco-harvest (<i>q2</i>), and load-shedding conservation (<i>q3</i>) to emergency lockdown (<i>q4</i>). The model is mathematically validated through a 30-entry total transition matrix and simulated via an execution engine. Verification across 10 operational scenarios and 27 automated unit tests proves that the automaton guarantees bounded <i>O(1)</i> constant runtime, bounded memory footprint, zero non-deterministic ambiguity, and deterministic fail-safe latching.",
            body_style,
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. INTRODUCTION & THEORETICAL MOTIVATION", h1_style))
    story.append(Paragraph("1.1 Problem Statement", h2_style))
    story.append(
        Paragraph(
            "Residential distributed energy resources (DER) combine multi-directional energy flows from utility grids, rooftop photovoltaic arrays, and battery storage. Coordinating these resources under volatile consumption surges and weather fluctuations exposes systems to operational hazards such as breaker tripping, battery over-discharge, and inadvertent re-energization during short circuits. Ad-hoc scripting techniques relying on heuristic conditionals fail to provide provable guarantees against race conditions and undefined state transitions.",
            body_style,
        )
    )

    story.append(Paragraph("1.2 The Case for Formal Language and Automata Theory (FLA)", h2_style))
    story.append(
        Paragraph(
            "In cyber-physical control architectures, automated switching logic must satisfy strict safety and liveness criteria:<br/>"
            "<b>1. Determinism:</b> Given any controller state <i>q ∈ Q</i> and observation <i>σ ∈ Σ</i>, the system must transition to exactly one valid configuration (<i>δ(q, σ)</i>).<br/>"
            "<b>2. Deterministic Response Time (O(1)):</b> Embedded microcontrollers operating along electrical distribution boards possess constrained execution budgets. An automaton transition executes in constant time (<i>O(1)</i>) via direct hash lookup, eliminating inference latency.<br/>"
            "<b>3. Formal Verifiability:</b> State reachability analysis proves that unsafe operational states cannot be entered and recovery sequences adhere strictly to safety protocols.",
            body_style,
        )
    )
    story.append(Spacer(1, 10))

    # ========================================================================
    # CHAPTER 2: LITERATURE SURVEY
    # ========================================================================
    story.append(Paragraph("2. LITERATURE SURVEY & THEORETICAL FOUNDATION", h1_style))
    story.append(Paragraph("2.1 Classical Automata in Industrial Control", h2_style))
    story.append(
        Paragraph(
            "Automata theory, originally formalized by Rabin, Scott, and Chomsky, provides the mathematical underpinning for compiler construction and discrete event systems (Ramadge & Wonham, 1989). In smart-home energy automation, a DFA represents a formal language recognizer where the input string represents a temporal trace of energy events, and the accepted language <i>L(M)</i> defines the set of compliant, hazard-free operational traces.",
            body_style,
        )
    )

    story.append(Paragraph("2.2 Comparison: DFA vs. Heuristic / Black-Box Models", h2_style))
    comp_data = [
        ["Property", "Deterministic Finite Automata (DFA)", "Heuristic / Threshold Logic", "Machine Learning Classifiers"],
        ["Behavioral Determinism", "100% Guaranteed", "High, but prone to race conditions", "Probabilistic (Stochastic)"],
        ["State Memory / History", "Explicitly tracked via states (Q)", "Typically scattered in flags", "Implicitly modeled (RNN/LSTM)"],
        ["Resource Complexity", "O(1) time, O(1) space", "O(1) time, O(1) space", "O(N) high compute / GPU load"],
        ["Verification & Safety", "Mathematically provable", "Prone to unhandled edge cases", "Susceptible to adversarial drift"],
    ]
    t_comp = Table(comp_data, colWidths=[110, 130, 120, 120])
    t_comp.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0bec5")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8f9fa")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
    )
    story.append(t_comp)
    story.append(PageBreak())

    # ========================================================================
    # CHAPTER 3: METHODOLOGY & MATHEMATICAL FORMALIZATION
    # ========================================================================
    story.append(Paragraph("3. METHODOLOGY & MATHEMATICAL FORMALIZATION", h1_style))
    story.append(Paragraph("3.1 Sensor Data Abstraction and Discretization", h2_style))
    story.append(
        Paragraph(
            "Continuous physical sensors measure real-valued quantities (<i>P<sub>demand</sub></i> in kW, <i>I<sub>solar</sub></i> in W/m², battery SoC in %). A discretization function <i>f : R<sup>n</sup> × {0,1}<sup>m</sup> → Σ</i> maps multi-channel telemetry into discrete formal alphabet tokens based on operational thresholds:<br/>"
            "• <b>SAFETY_ALERT (A):</b> Asserted if hardware electrical/thermal trip line is active.<br/>"
            "• <b>RESET (R):</b> Asserted if operator supervised reset pushbutton is triggered.<br/>"
            "• <b>HIGH_DEMAND (H):</b> Asserted if aggregate household load exceeds 4.5 kW.<br/>"
            "• <b>LOW_BATTERY (B):</b> Asserted if battery state of charge drops below 25.0%.<br/>"
            "• <b>SOLAR_AVAILABLE (S):</b> Asserted if solar irradiance exceeds 300 W/m².<br/>"
            "• <b>NORMAL (N):</b> Nominal conditions within bounds and no active hazard.",
            body_style,
        )
    )

    story.append(Paragraph("3.2 Formal 5-Tuple Definition of the DFA", h2_style))
    story.append(
        Paragraph(
            "The energy controller is formalized as a Deterministic Finite Automaton <b>M = (Q, Σ, δ, q0, F)</b>, where:<br/>"
            "<b>1. Q (Finite Set of States):</b> Q = {q0, q1, q2, q3, q4}<br/>"
            "   • <b>q0 (IDLE):</b> Quiescent standby baseline; power relays open.<br/>"
            "   • <b>q1 (NORMAL_OPERATION):</b> Grid-tied delivery balancing nominal household load.<br/>"
            "   • <b>q2 (SOLAR_PRIORITY):</b> Green eco-mode prioritizing rooftop photovoltaic harvest.<br/>"
            "   • <b>q3 (ENERGY_SAVING):</b> Demand response / load curtailment to avert overload.<br/>"
            "   • <b>q4 (SAFETY_SHUTDOWN):</b> Emergency isolation latch; all circuits de-energized.<br/>"
            "<b>2. Σ (Input Alphabet):</b> Σ = {N, H, S, B, A, R}<br/>"
            "<b>3. δ (Transition Function):</b> δ : Q × Σ → Q total mapping.<br/>"
            "<b>4. q0 (Initial State):</b> q0 = IDLE.<br/>"
            "<b>5. F (Accepting States):</b> F = {q0, q1, q2, q3} = Q \\ {q4}. Strings ending in q4 are rejected as hazardous.",
            body_style,
        )
    )

    story.append(Paragraph("3.3 State Transition Table (δ)", h2_style))
    table_data = [
        ["Current State (q)", "N (Normal)", "H (High)", "S (Solar)", "B (BattLow)", "A (Alert)", "R (Reset)"],
        ["→ q0 (IDLE)", "q1", "q3", "q2", "q0", "q4", "q0"],
        ["* q1 (NORMAL_OP)", "q1", "q3", "q2", "q3", "q4", "q0"],
        ["* q2 (SOLAR_PRIO)", "q1", "q3", "q2", "q3", "q4", "q0"],
        ["* q3 (ENERGY_SAV)", "q1", "q3", "q2", "q3", "q4", "q0"],
        ["q4 (SAFETY_SHUT)", "q4", "q4", "q4", "q4", "q4", "q0"],
    ]
    t_trans = Table(table_data, colWidths=[125, 58, 58, 58, 62, 58, 58])
    t_trans.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0bec5")),
            ("BACKGROUND", (0, 1), (-1, 4), colors.HexColor("#e8f5e9")),
            ("BACKGROUND", (0, 5), (-1, 5), colors.HexColor("#ffebee")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
    )
    story.append(t_trans)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>Notation: '→' indicates initial state (q0); '*' indicates accepting state (q ∈ F).</i>", body_style))

    story.append(Paragraph("3.4 State Transition Logic and Safety Rules", h2_style))
    story.append(
        Paragraph(
            "<b>1. Emergency Trip Invariance:</b> Assertion of <i>SAFETY_ALERT (A)</i> from any state unconditionally transitions the controller directly to <i>q4 (SAFETY_SHUTDOWN)</i>.<br/>"
            "<b>2. Lockdown Latching Invariance:</b> Once in <i>q4</i>, all operational inputs (<i>N, H, S, B, A</i>) self-loop in <i>q4</i>. Sunlight or load drop cannot clear an unresolved physical hazard.<br/>"
            "<b>3. Supervised Recovery Precedence:</b> The only escape vector from <i>q4</i> is <i>RESET (R)</i>, which strictly routes the system to <i>q0 (IDLE)</i> standby, preventing sudden re-energization.<br/>"
            "<b>4. Empty Sequence Invariance:</b> By extended definition <i>δ*(q0, ε) = q0 ∈ F</i>, confirming that unperturbed initialization is an accepted safe baseline.",
            body_style,
        )
    )
    story.append(PageBreak())

    # ========================================================================
    # STATE DIAGRAM & CHAPTER 4
    # ========================================================================
    story.append(Paragraph("3.5 State Transition Diagram", h2_style))
    if os.path.exists(diagram_png_path):
        story.append(Image(diagram_png_path, width=470, height=270))
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(
                "<b>Figure 3.1:</b> Graphical state diagram of the Deterministic Finite Automaton <i>M = (Q, Σ, δ, q0, F)</i> illustrating initial arrow, double-circle accepting states (q0–q3), single-circle fault lockout (q4), directed edges, and grouped tokens.",
                ParagraphStyle("Cap", parent=body_style, fontSize=8, alignment=1),
            )
        )
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. SYSTEM IMPLEMENTATION & SOFTWARE ARCHITECTURE", h1_style))
    story.append(Paragraph("4.1 System Components", h2_style))
    story.append(
        Paragraph(
            "The software implementation is structured into decoupled modules:<br/>"
            "<b>1. Automaton Engine (<code>dfa_controller.py</code>):</b> Implements formal 5-tuple structures, type-safe Enums, transition table validator, and O(1) step functions.<br/>"
            "<b>2. Simulation & Runner (<code>simulator.py</code>):</b> Provides interactive CLI event injection, batch evaluation, and continuous telemetry discretization loops.<br/>"
            "<b>3. Diagram Generator (<code>visualize_dfa.py</code>):</b> Renders publication-grade 300-DPI visual diagrams and standard Graphviz DOT files.",
            body_style,
        )
    )

    story.append(Paragraph("4.2 Discretization Algorithm Pseudocode", h2_style))
    pseudo_text = (
        "Algorithm 1: DiscretizeSensorTelemetryAndDispatch<br/>"
        "Input  : Telemetry vector T = (P_demand, I_solar, SoC_batt, Trip_hw, Reset_cmd), State q<br/>"
        "Output : Next State q', Acceptance Status Acc<br/>"
        "1:  if Trip_hw == True then sigma &lt;- InputSymbol.SAFETY_ALERT<br/>"
        "2:  else if Reset_cmd == True then sigma &lt;- InputSymbol.RESET<br/>"
        "3:  else if P_demand &gt; 4.5 then sigma &lt;- InputSymbol.HIGH_DEMAND<br/>"
        "4:  else if SoC_batt &lt; 25.0 then sigma &lt;- InputSymbol.LOW_BATTERY<br/>"
        "5:  else if I_solar &gt;= 300.0 then sigma &lt;- InputSymbol.SOLAR_AVAILABLE<br/>"
        "6:  else sigma &lt;- InputSymbol.NORMAL; end if<br/>"
        "7:  q' &lt;- delta[(q, sigma)]; Acc &lt;- (q' in F)<br/>"
        "8:  return q', Acc"
    )
    story.append(Paragraph(pseudo_text, code_style))
    story.append(PageBreak())

    # ========================================================================
    # CHAPTER 5: EXPERIMENTAL RESULTS
    # ========================================================================
    story.append(Paragraph("5. EXPERIMENTAL RESULTS & VALIDATION SCENARIOS", h1_style))
    story.append(
        Paragraph(
            "The automaton was rigorously evaluated across 10 representative operational scenarios to verify mathematical correctness, determinism, and safety latching:",
            body_style,
        )
    )
    story.append(Spacer(1, 6))

    scen_table_data = [
        ["ID", "Scenario Title", "Input Stream", "Formal Trace", "Final State", "Result"],
        ["SCEN-01", "Nominal Power Dispatch", "N, N, N", "q0 → q1 → q1 → q1", "NORMAL_OP", "ACCEPTED"],
        ["SCEN-02", "Solar Priority Harvest", "N, S, S, N", "q0 → q1 → q2 → q2 → q1", "NORMAL_OP", "ACCEPTED"],
        ["SCEN-03", "Peak Demand Shedding", "N, H, H, N", "q0 → q1 → q3 → q3 → q1", "NORMAL_OP", "ACCEPTED"],
        ["SCEN-04", "Battery Depletion", "S, B, S", "q0 → q2 → q3 → q2", "SOLAR_PRIO", "ACCEPTED"],
        ["SCEN-05", "Safety Trip & Lockout", "N, S, A, N, H", "q0 → q1 → q2 → q4 → q4 → q4", "SAFETY_SHUT", "REJECTED"],
        ["SCEN-06", "Supervised Reset Recovery", "N, A, R, N", "q0 → q1 → q4 → q0 → q1", "NORMAL_OP", "ACCEPTED"],
        ["SCEN-07", "Repeated Event Bursts", "H, H, H, S, S", "q0 → q3 → q3 → q3 → q2 → q2", "SOLAR_PRIO", "ACCEPTED"],
        ["SCEN-08", "Quiescent Baseline (ε)", "(empty)", "q0", "IDLE", "ACCEPTED"],
        ["SCEN-09", "Fault in Energy Saving", "H, A, S", "q0 → q3 → q4 → q4", "SAFETY_SHUT", "REJECTED"],
        ["SCEN-10", "Malformed Token Input", "N, ERR, N", "Parser Exception Raised", "None", "REJECTED"],
    ]

    t_scen = Table(scen_table_data, colWidths=[42, 110, 80, 125, 75, 55])
    t_scen.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0bec5")),
            ("ALIGN", (5, 0), (5, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])
    )
    story.append(t_scen)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.1 Simulation Output Traces & Experimental Evidence", h2_style))
    story.append(
        Paragraph(
            "Terminal execution logs verify that the Python execution engine correctly updates state configurations in real time:<br/>"
            "<code>&gt;&gt;&gt; SCEN-06 Execution: Input String 'N, A, R, N'<br/>"
            "  Step 01: δ(IDLE (q0), NORMAL ('N')) --&gt; NORMAL_OPERATION (q1) [ACCEPTING]<br/>"
            "  Step 02: δ(NORMAL_OPERATION (q1), SAFETY_ALERT ('A')) --&gt; SAFETY_SHUTDOWN (q4) [NON-ACCEPTING]<br/>"
            "  Step 03: δ(SAFETY_SHUTDOWN (q4), RESET ('R')) --&gt; IDLE (q0) [ACCEPTING]<br/>"
            "  Step 04: δ(IDLE (q0), NORMAL ('N')) --&gt; NORMAL_OPERATION (q1) [ACCEPTING]<br/>"
            "Trace: q0 -&gt; q1 -&gt; q4 -&gt; q0 -&gt; q1 | Final: NORMAL_OPERATION (q1) | Outcome: ACCEPTED</code>",
            code_style,
        )
    )
    story.append(Spacer(1, 10))

    # ========================================================================
    # CHAPTER 6 & 7: DISCUSSION & CONCLUSION
    # ========================================================================
    story.append(Paragraph("6. DISCUSSION & COMPLEXITY ANALYSIS", h1_style))
    story.append(Paragraph("6.1 Time & Space Complexity", h2_style))
    story.append(
        Paragraph(
            "<b>Time Complexity:</b> For an input sequence of length <i>n</i>, the controller processes transitions in <i>O(n)</i> time overall, and exactly <b>O(1) constant time</b> per event read via direct hash table indexing.<br/>"
            "<b>Space Complexity:</b> The transition table requires <i>O(|Q| × |Σ|) = 5 × 6 = 30</i> entries, occupying negligible constant auxiliary memory (<i>O(1)</i>). This enables flashing directly onto memory-constrained microcontrollers (e.g., PIC, ESP32) without heap allocation.<br/>"
            "<b>Comparison with Non-Deterministic Models (NFA):</b> An NFA was strictly rejected because physical actuators cannot exist in a superposition of states (e.g., a power contactor cannot be simultaneously open and closed). DFAs guarantee single unambiguous configurations.",
            body_style,
        )
    )

    story.append(Paragraph("7. CONCLUSION & FUTURE SCOPE", h1_style))
    story.append(Paragraph("7.1 Conclusion", h2_style))
    story.append(
        Paragraph(
            "This project demonstrates the practical application of Formal Languages and Automata Theory to cyber-physical smart-home energy automation. By formalizing sensor telemetry into a finite alphabet and a complete deterministic transition matrix, we engineered a controller that provides provable behavioral determinism, fail-safe lockout latching, and zero undefined edge cases.",
            body_style,
        )
    )

    story.append(Paragraph("7.2 Future Scope", h2_style))
    story.append(
        Paragraph(
            "<b>1. Mealy Machine Extension:</b> Transitioning from a language recognizer to a Mealy/Moore Machine emitting physical actuator control vectors (e.g., <code>OPEN_GRID_RELAY</code>, <code>ENABLE_INVERTER</code>) along transition edges.<br/>"
            "<b>2. Pushdown Automata (PDA):</b> Incorporating stack memory to track cumulative energy quotas and charging cycle allowances.<br/>"
            "<b>3. Embedded Hardware Deployment:</b> Flashing the transition matrix as C/C++ firmware onto ESP32 microcontrollers interfaced with real current sensors and solid-state relays.",
            body_style,
        )
    )

    story.append(Paragraph("8. REFERENCES", h1_style))
    story.append(
        Paragraph(
            "1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). <i>Introduction to Automata Theory, Languages, and Computation</i> (3rd ed.). Addison-Wesley.<br/>"
            "2. Sipser, M. (2013). <i>Introduction to the Theory of Computation</i> (3rd ed.). Cengage Learning.<br/>"
            "3. Ramadge, P. J., & Wonham, W. M. (1989). 'The Control of Discrete Event Systems.' <i>Proceedings of the IEEE</i>, 77(1), 81–98.<br/>"
            "4. Cassandras, C. G., & Lafortune, S. (2008). <i>Introduction to Discrete Event Systems</i> (2nd ed.). Springer.<br/>"
            "5. International Electrotechnical Commission. (2010). <i>IEC 61508: Functional Safety of Electrical/Electronic Systems</i>.<br/>"
            "6. Python Software Foundation. (2024). <i>Python 3.12 Standard Library Documentation</i>. https://docs.python.org/3/",
            body_style,
        )
    )

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Academic report PDF successfully generated at: {output_pdf_path}")


def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    report_pdf_path = os.path.join(base_dir, "report", "project_report.pdf")
    diagram_png_path = os.path.join(base_dir, "docs", "state_diagram.png")

    os.makedirs(os.path.join(base_dir, "report"), exist_ok=True)
    build_academic_pdf(report_pdf_path, diagram_png_path)


if __name__ == "__main__":
    main()

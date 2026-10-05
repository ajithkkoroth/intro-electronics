import hashlib
import random
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

# ==============================================================================
# 1. VERIFICATION CODE GENERATOR (Format: M3.1-<Roll no>-<4 char code>)
# ==============================================================================
def make_verification_code(roll_no, name, config):
    clean_roll = roll_no.strip().upper()
    clean_name = "".join(name.strip().upper().split())
    prefix = config["MODULE_PREFIX"]
    salt = config["SECRET_SALT"]
    raw = f"{prefix}|{clean_roll}|{clean_name}|{salt}"
    code4 = hashlib.sha256(raw.encode()).hexdigest().upper()[:4]
    return f"{prefix}-{clean_roll}-{code4}"

# ==============================================================================
# 2. ZERO-DEPENDENCY PURE-PYTHON SVG CIRCUIT RENDERER (IEEE SYMBOLS)
# ==============================================================================
def render_circuit_svg(circuit_type, p):
    style = """
    <style>
        .ckt-svg { background:#ffffff; border:1px solid #e0e0e0; border-radius:6px; margin:8px 0; max-width:100%; }
        .wire { stroke:#222; stroke-width:2.2; fill:none; stroke-linecap:round; stroke-linejoin:round; }
        .comp { stroke:#0d47a1; stroke-width:2.4; fill:none; stroke-linejoin:round; }
        .comp-fill { stroke:#0d47a1; stroke-width:2; fill:#bbdefb; }
        .lbl { font-family:'Segoe UI', Arial, sans-serif; font-size:13px; fill:#111; font-weight:600; }
        .sub-lbl { font-family:'Segoe UI', Arial, sans-serif; font-size:12px; fill:#0d47a1; font-weight:bold; }
    </style>
    """
    if circuit_type == "hwr":
        return f"""
        <svg class="ckt-svg" width="460" height="190" viewBox="0 0 460 190">
            {style}
            <!-- AC Source -->
            <circle cx="70" cy="95" r="24" class="comp"/>
            <path d="M 56 95 Q 63 80 70 95 T 84 95" class="comp"/>
            <text x="15" y="60" class="lbl">vs(t)</text>
            <text x="10" y="78" class="sub-lbl">Vm = {p['Vm']} V</text>
            <!-- Top Wire & Diode D1 -->
            <line x1="70" y1="71" x2="70" y2="35" class="wire"/>
            <line x1="70" y1="35" x2="185" y2="35" class="wire"/>
            <polygon points="185,22 185,48 215,35" class="comp-fill"/>
            <line x1="215" y1="20" x2="215" y2="50" class="comp"/>
            <text x="175" y="15" class="lbl">D1 (Ideal)</text>
            <line x1="215" y1="35" x2="340" y2="35" class="wire"/>
            <!-- Load Resistor RL -->
            <line x1="340" y1="35" x2="340" y2="62" class="wire"/>
            <polyline points="340,62 350,68 330,78 350,88 330,98 350,108 330,118 340,124" class="comp"/>
            <line x1="340" y1="124" x2="340" y2="155" class="wire"/>
            <text x="358" y="92" class="lbl">RL</text>
            <text x="358" y="110" class="sub-lbl">{p['RL']} kΩ</text>
            <!-- Bottom Return Wire & Ground -->
            <line x1="70" y1="119" x2="70" y2="155" class="wire"/>
            <line x1="70" y1="155" x2="340" y2="155" class="wire"/>
            <line x1="200" y1="155" x2="200" y2="168" class="wire"/>
            <line x1="186" y1="168" x2="214" y2="168" class="wire"/>
            <line x1="191" y1="173" x2="209" y2="173" class="wire"/>
            <line x1="196" y1="178" x2="204" y2="178" class="wire"/>
        </svg>"""

    elif circuit_type == "ctfwr":
        return f"""
        <svg class="ckt-svg" width="500" height="220" viewBox="0 0 500 220">
            {style}
            <!-- Upper AC Secondary -->
            <circle cx="80" cy="65" r="20" class="comp"/>
            <path d="M 68 65 Q 74 53 80 65 T 92 65" class="comp"/>
            <text x="10" y="55" class="sub-lbl">Vm = {p['Vm']} V</text>
            <!-- Lower AC Secondary -->
            <circle cx="80" cy="155" r="20" class="comp"/>
            <path d="M 68 155 Q 74 143 80 155 T 92 155" class="comp"/>
            <text x="10" y="165" class="sub-lbl">Vm = {p['Vm']} V</text>
            <!-- Center Tap Ground & RL Return -->
            <line x1="80" y1="85" x2="80" y2="135" class="wire"/>
            <circle cx="80" cy="110" r="3.5" fill="#222"/>
            <text x="22" y="114" class="lbl">CT (GND)</text>
            <line x1="80" y1="110" x2="260" y2="110" class="wire"/>
            <!-- Diode D1 (Top) -->
            <line x1="80" y1="45" x2="80" y2="25" class="wire"/>
            <line x1="80" y1="25" x2="185" y2="25" class="wire"/>
            <polygon points="185,14 185,36 210,25" class="comp-fill"/>
            <line x1="210" y1="13" x2="210" y2="37" class="comp"/>
            <text x="190" y="11" class="lbl">D1</text>
            <line x1="210" y1="25" x2="390" y2="25" class="wire"/>
            <!-- Diode D2 (Bottom) -->
            <line x1="80" y1="175" x2="80" y2="195" class="wire"/>
            <line x1="80" y1="195" x2="185" y2="195" class="wire"/>
            <polygon points="185,184 185,206 210,195" class="comp-fill"/>
            <line x1="210" y1="183" x2="210" y2="207" class="comp"/>
            <text x="190" y="180" class="lbl">D2</text>
            <line x1="210" y1="195" x2="390" y2="195" class="wire"/>
            <!-- Common Cathode Node & Load RL -->
            <line x1="390" y1="25" x2="390" y2="195" class="wire"/>
            <line x1="390" y1="110" x2="355" y2="110" class="wire"/>
            <polyline points="355,110 349,100 339,120 329,100 319,120 309,100 299,120 293,110" class="comp"/>
            <line x1="293" y1="110" x2="260" y2="110" class="wire"/>
            <text x="295" y="88" class="sub-lbl">RL = {p['RL']} kΩ</text>
        </svg>"""

    elif circuit_type == "bridge":
        return f"""
        <svg class="ckt-svg" width="490" height="210" viewBox="0 0 490 210">
            {style}
            <!-- AC Source -->
            <circle cx="65" cy="105" r="22" class="comp"/>
            <path d="M 52 105 Q 58 92 65 105 T 78 105" class="comp"/>
            <text x="10" y="65" class="sub-lbl">Vm = {p['Vm']} V</text>
            <text x="15" y="82" class="lbl">50 Hz</text>
            <line x1="65" y1="83" x2="65" y2="30" class="wire"/>
            <line x1="65" y1="30" x2="210" y2="30" class="wire"/>
            <line x1="65" y1="127" x2="65" y2="180" class="wire"/>
            <line x1="65" y1="180" x2="210" y2="180" class="wire"/>
            <!-- Diamond Bridge -->
            <line x1="210" y1="30" x2="150" y2="105" class="wire"/>
            <line x1="210" y1="30" x2="270" y2="105" class="wire"/>
            <line x1="150" y1="105" x2="210" y2="180" class="wire"/>
            <line x1="270" y1="105" x2="210" y2="180" class="wire"/>
            <circle cx="210" cy="30" r="3.5" fill="#222"/>
            <circle cx="210" cy="180" r="3.5" fill="#222"/>
            <circle cx="150" cy="105" r="3.5" fill="#0d47a1"/>
            <circle cx="270" cy="105" r="3.5" fill="#0d47a1"/>
            <text x="148" y="62" class="lbl">D4</text>
            <text x="248" y="62" class="lbl">D1</text>
            <text x="148" y="158" class="lbl">D3</text>
            <text x="248" y="158" class="lbl">D2</text>
            <!-- Output to RL -->
            <line x1="270" y1="105" x2="385" y2="105" class="wire"/>
            <polyline points="385,105 395,111 375,121 395,131 375,141 395,151 375,161 385,167" class="comp"/>
            <line x1="385" y1="167" x2="385" y2="195" class="wire"/>
            <line x1="150" y1="105" x2="150" y2="195" class="wire"/>
            <line x1="150" y1="195" x2="385" y2="195" class="wire"/>
            <text x="402" y="135" class="lbl">RL</text>
            <text x="402" y="153" class="sub-lbl">{p['RL']} kΩ</text>
        </svg>"""

    elif circuit_type in ("filter_analysis", "filter_design"):
        c_label = f"C = {p['C']} μF" if circuit_type == "filter_analysis" else f"C = ? μF (γ={p['gamma']})"
        return f"""
        <svg class="ckt-svg" width="500" height="190" viewBox="0 0 500 190">
            {style}
            <!-- FWR Block -->
            <rect x="25" y="45" width="110" height="100" rx="6" class="comp-fill"/>
            <text x="40" y="85" class="lbl">Full-Wave</text>
            <text x="45" y="103" class="lbl">Rectifier</text>
            <text x="35" y="125" class="sub-lbl">Vm = {p['Vm']} V</text>
            <text x="45" y="35" class="lbl">fin = 50 Hz</text>
            <!-- Top & Bottom Rails -->
            <line x1="135" y1="60" x2="390" y2="60" class="wire"/>
            <line x1="135" y1="135" x2="390" y2="135" class="wire"/>
            <!-- Shunt Capacitor Filter C -->
            <line x1="245" y1="60" x2="245" y2="88" class="wire"/>
            <line x1="227" y1="88" x2="263" y2="88" class="comp"/>
            <line x1="227" y1="102" x2="263" y2="102" class="comp"/>
            <line x1="245" y1="102" x2="245" y2="135" class="wire"/>
            <text x="180" y="50" class="sub-lbl">{c_label}</text>
            <!-- Load Resistor RL -->
            <line x1="390" y1="60" x2="390" y2="72" class="wire"/>
            <polyline points="390,72 400,77 380,85 400,93 380,101 400,109 380,117 390,122" class="comp"/>
            <line x1="390" y1="122" x2="390" y2="135" class="wire"/>
            <text x="410" y="95" class="lbl">RL</text>
            <text x="410" y="113" class="sub-lbl">{p['RL']} Ω</text>
        </svg>"""

    elif circuit_type == "zener":
        return f"""
        <svg class="ckt-svg" width="500" height="195" viewBox="0 0 500 195">
            {style}
            <!-- Unregulated DC Input Vin -->
            <circle cx="65" cy="98" r="22" class="comp"/>
            <text x="58" y="94" class="lbl">+</text>
            <text x="60" y="112" class="lbl">-</text>
            <text x="12" y="58" class="sub-lbl">Vin = {p['Vin']} V</text>
            <line x1="65" y1="76" x2="65" y2="40" class="wire"/>
            <line x1="65" y1="40" x2="125" y2="40" class="wire"/>
            <!-- Series Resistor RS -->
            <polyline points="125,40 131,30 141,50 151,30 161,50 171,30 181,50 187,40" class="comp"/>
            <text x="125" y="22" class="sub-lbl">RS = ? Ω (Design)</text>
            <line x1="187" y1="40" x2="390" y2="40" class="wire"/>
            <!-- Zener Diode Shunt Branch -->
            <line x1="265" y1="40" x2="265" y2="82" class="wire"/>
            <polygon points="251,112 279,112 265,84" class="comp-fill"/>
            <polyline points="247,78 251,84 279,84 283,90" class="comp"/>
            <line x1="265" y1="112" x2="265" y2="155" class="wire"/>
            <text x="285" y="92" class="sub-lbl">VZ = {p['VZ']} V</text>
            <text x="285" y="110" class="lbl">IZ = {p['IZ']} mA</text>
            <!-- Load Resistor RL -->
            <line x1="390" y1="40" x2="390" y2="68" class="wire"/>
            <polyline points="390,68 400,74 380,84 400,94 380,104 400,114 380,124 390,130" class="comp"/>
            <line x1="390" y1="130" x2="390" y2="155" class="wire"/>
            <text x="410" y="95" class="lbl">RL</text>
            <text x="410" y="113" class="sub-lbl">{p['RL']} Ω</text>
            <!-- Bottom Return Wire -->
            <line x1="65" y1="120" x2="65" y2="155" class="wire"/>
            <line x1="65" y1="155" x2="390" y2="155" class="wire"/>
        </svg>"""
    return ""

# ==============================================================================
# 3. TWO-STAGE GATED UI & AUTO-GRADER ENGINE
# ==============================================================================
def launch_assessment(config, mcq_bank, design_builder_fn):
    num_mcqs = min(config["NUM_MCQS"], len(mcq_bank))
    mcq_total_marks = num_mcqs * config["MARKS_PER_MCQ"]
    
    sample_designs = design_builder_fn(1, random.Random(1))
    num_designs = len(sample_designs)
    design_total_marks = num_designs * config["MARKS_PER_DESIGN"]
    overall_marks = mcq_total_marks + design_total_marks

    header_html = widgets.HTML(f"""
    <div style="background:linear-gradient(90deg, #1e3c72, #2a5298); color:white; padding:18px; border-radius:8px; margin-bottom:12px;">
        <h2 style="margin:0;">⚡ {config['COURSE_TITLE']}</h2>
        <p style="margin:6px 0 0 0;">
            <b>Stage 1:</b> {num_mcqs} MCQs ({mcq_total_marks} Marks) &nbsp;|&nbsp;
            <b>Stage 2:</b> {num_designs} Circuit Design Problems ({design_total_marks} Marks) &nbsp;|&nbsp;
            <b>Total: {overall_marks} Marks</b>
        </p>
    </div>
    """)

    roll_box = widgets.Text(description="Roll No:", placeholder="e.g., KTU24EE045", style={'description_width': '70px'})
    name_box = widgets.Text(description="Full Name:", placeholder="e.g., Rahul Nair", style={'description_width': '75px'})
    start_btn = widgets.Button(description="Start Assignment", button_style='primary', icon='play', layout=widgets.Layout(width='200px'))

    stage1_out = widgets.Output()
    stage1_feedback = widgets.Output()
    stage2_out = widgets.Output()
    stage2_feedback = widgets.Output()

    state = {
        "active_mcqs": [],
        "active_designs": [],
        "mcq_radios": [],
        "design_inputs": {}
    }

    def is_close(u_val, t_val):
        tol = config["TOLERANCE"]
        return abs(u_val - t_val) <= max(tol * abs(t_val), 0.015)

    def on_start_clicked(b):
        if not roll_box.value.strip() or not name_box.value.strip():
            with stage1_out:
                clear_output()
                display(HTML("<p style='color:#d32f2f; font-weight:bold;'>⚠️ Please enter both your Roll Number and Full Name.</p>"))
            return

        roll_box.disabled = True
        name_box.disabled = True
        start_btn.disabled = True

        clean_roll = roll_box.value.strip().upper()
        h = int(hashlib.sha256(clean_roll.encode()).hexdigest(), 16)
        rng = random.Random(h)

        sampled = rng.sample(mcq_bank, num_mcqs)
        state["active_mcqs"] = []
        for item in sampled:
            opts = list(item["options"])
            rng.shuffle(opts)
            state["active_mcqs"].append({"q": item["q"], "options": opts, "ans": item["ans"]})

        state["active_designs"] = design_builder_fn(h, rng)
        state["mcq_radios"] = []

        m_per_q = config["MARKS_PER_MCQ"]
        ui_list = [widgets.HTML(
            f"<div style='background:#e3f2fd; padding:12px; border-radius:6px; margin-top:10px;'>"
            f"<h3 style='margin:0; color:#0d47a1;'>🔒 Stage 1: Conceptual MCQs ({num_mcqs} × {m_per_q} = {mcq_total_marks} Marks)</h3>"
            f"<p style='margin:4px 0 0 0;'>Answer all {num_mcqs} questions correctly to unlock Stage 2 (Design Problems).</p></div>"
        )]

        for i, m in enumerate(state["active_mcqs"]):
            q_html = widgets.HTML(f"<p style='margin:12px 0 4px 0;'><b>Q{i+1}. {m['q']}</b> ({m_per_q} Mark)</p>")
            rb = widgets.RadioButtons(options=m["options"], value=None, layout=widgets.Layout(width='98%'))
            state["mcq_radios"].append(rb)
            ui_list.extend([q_html, rb])

        check_mcq_btn = widgets.Button(description="Verify MCQs & Unlock Stage 2", button_style='warning', icon='unlock',
                                       layout=widgets.Layout(width='270px', height='42px', margin='16px 0'))
        check_mcq_btn.on_click(on_verify_mcqs)
        ui_list.append(check_mcq_btn)

        with stage1_out:
            clear_output()
            display(widgets.VBox(ui_list))

    def on_verify_mcqs(b):
        total_q = len(state["active_mcqs"])
        correct_q = 0
        wrong_list = []

        for i, m in enumerate(state["active_mcqs"]):
            if state["mcq_radios"][i].value == m["ans"]:
                correct_q += 1
            else:
                wrong_list.append(f"Q{i+1}")

        if correct_q < total_q:
            with stage1_feedback:
                clear_output()
                display(HTML(
                    f"<div style='background:#ffebee; border-left:5px solid #c62828; padding:12px; margin:10px 0;'>"
                    f"<b>❌ Stage 1 Score: {correct_q * config['MARKS_PER_MCQ']} / {mcq_total_marks} Marks.</b> "
                    f"Please review and correct: <b>{', '.join(wrong_list)}</b> to unlock Stage 2!</div>"
                ))
        else:
            b.disabled = True
            for rb in state["mcq_radios"]:
                rb.disabled = True
            with stage1_feedback:
                clear_output()
                display(HTML(
                    f"<div style='background:#e8f5e9; border-left:5px solid #2e7d32; padding:12px; margin:10px 0;'>"
                    f"<b>✅ Stage 1 Complete ({mcq_total_marks} / {mcq_total_marks} Marks)!</b> "
                    f"Stage 2 (Circuit Analysis & Design) is now unlocked below.</div>"
                ))
            render_stage2()

    def render_stage2():
        state["design_inputs"] = {}
        m_per_d = config["MARKS_PER_DESIGN"]

        s2_ui = [widgets.HTML(
            f"<div style='background:#e8eaf6; padding:12px; border-radius:6px; margin-top:20px;'>"
            f"<h3 style='margin:0; color:#1a237e;'>🔓 Stage 2: Circuit Analysis & Design ({num_designs} × {m_per_d} = {design_total_marks} Marks)</h3>"
            f"<p style='margin:4px 0 0 0;'><i>Assigned to Roll No: <b>{roll_box.value.strip().upper()}</b>. Enter numerical values accurate to 2 decimal places.</i></p></div>"
        )]

        for prob in state["active_designs"]:
            svg_diagram = render_circuit_svg(prob["circuit_type"], prob["draw_params"])
            field_widgets = []
            for f_meta in prob["fields"]:
                w = widgets.FloatText(description=f_meta["label"], style={'description_width': '135px'}, layout=widgets.Layout(width='250px'))
                state["design_inputs"][f_meta["key"]] = w
                field_widgets.append(w)

            card_box = widgets.VBox([
                widgets.HTML(
                    f"<div style='background:#fafafa; padding:14px; border:1px solid #ddd; border-left:4px solid #1976d2; border-radius:6px; margin-top:15px;'>"
                    f"<h4 style='margin:0 0 6px 0;'>{prob['title']} ({m_per_d} Marks)</h4>"
                    f"<p style='margin:0 0 10px 0;'>{prob['desc']}</p>{svg_diagram}</div>"
                ),
                widgets.HBox(field_widgets, layout=widgets.Layout(flex_flow='row wrap', margin='8px 0 10px 0'))
            ])
            s2_ui.append(card_box)

        verify_s2_btn = widgets.Button(description="Verify All Design Problems & Generate Code", button_style='success', icon='check-circle',
                                       layout=widgets.Layout(width='340px', height='45px', margin='20px 0'))
        verify_s2_btn.on_click(on_verify_stage2)
        s2_ui.append(verify_s2_btn)

        with stage2_out:
            clear_output()
            display(widgets.VBox(s2_ui))

    def on_verify_stage2(b):
        m_per_d = config["MARKS_PER_DESIGN"]
        earned_design_marks = 0
        total_fields = 0
        passed_fields = 0
        feedback_rows = []

        for prob in state["active_designs"]:
            prob_correct = True
            prob_status = []
            for f_meta in prob["fields"]:
                total_fields += 1
                w = state["design_inputs"][f_meta["key"]]
                if is_close(w.value, f_meta["ans"]):
                    passed_fields += 1
                    w.disabled = True
                    prob_status.append(f"<span style='color:#2e7d32;'>✅ {f_meta['label']} Correct</span>")
                else:
                    prob_correct = False
                    prob_status.append(f"<span style='color:#c62828;'>❌ {f_meta['label']} Incorrect</span>")

            if prob_correct:
                earned_design_marks += m_per_d
                feedback_rows.append(f"<li><b>{prob['title']}</b>: {m_per_d}/{m_per_d} Marks — {' | '.join(prob_status)}</li>")
            else:
                feedback_rows.append(f"<li><b>{prob['title']}</b>: 0/{m_per_d} Marks — {' | '.join(prob_status)}</li>")

        if passed_fields < total_fields:
            with stage2_feedback:
                clear_output()
                display(HTML(f"""
                <div style="background:#fff3e0; border-left:5px solid #ef6c00; padding:14px; border-radius:6px; margin-top:12px;">
                    <h4 style="margin:0 0 8px 0; color:#e65100;">🔧 Stage 2 Score: {earned_design_marks} / {design_total_marks} Marks ({passed_fields}/{total_fields} Parameters Correct)</h4>
                    <p style="margin:0 0 8px 0;">Correct parameter boxes are locked. Recalculate the items marked with ❌ and click Verify again:</p>
                    <ul style="margin:0;">{''.join(feedback_rows)}</ul>
                </div>
                """))
        else:
            b.disabled = True
            ver_code = make_verification_code(roll_box.value, name_box.value, config)
            with stage2_feedback:
                clear_output()
                display(HTML(f"""
                <div style="background:linear-gradient(135deg, #e8f5e9, #c8e6c9); border:3px solid #2e7d32; padding:22px; border-radius:10px; margin-top:18px; text-align:center;">
                    <h2 style="color:#1b5e20; margin:0 0 10px 0;">🎉 Congratulations, {name_box.value.strip()}!</h2>
                    <p style="font-size:16px; margin:0 0 15px 0;">
                        You have mastered all {num_mcqs} MCQs ({mcq_total_marks} Marks) and solved all {num_designs} Circuit Design Problems ({design_total_marks} Marks)
                        for a total score of <b>{overall_marks} / {overall_marks} Marks</b>!
                    </p>
                    <div style="background:#ffffff; border:2px dashed #1b5e20; display:inline-block; padding:14px 28px; border-radius:8px; margin-bottom:12px;">
                        <span style="font-size:13px; color:#555; display:block;">FACULTY / TA VERIFICATION CODE</span>
                        <span style="font-size:24px; font-family:monospace; font-weight:bold; color:#0d47a1; letter-spacing:2px;">{ver_code}</span>
                    </div>
                    <p style="font-size:14px; color:#333; margin:0;">📋 Share this code with your Faculty/TA for verification.</p>
                </div>
                """))

    start_btn.on_click(on_start_clicked)
    display(header_html, widgets.HBox([roll_box, name_box, start_btn]), stage1_out, stage1_feedback, stage2_out, stage2_feedback)

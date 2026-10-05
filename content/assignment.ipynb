import hashlib
import random
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import schemdraw
import schemdraw.elements as elm

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
# 2. SCHEMATIC RENDERING ENGINE (SCHEMDRAW -> SVG)
# ==============================================================================
def render_circuit_svg(circuit_type, p):
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.3, fontsize=11)

        if circuit_type == "hwr":
            d.add(elm.SourceSin().up().label(f'$v_s(t)$\n$V_m = {p["Vm"]}$ V', loc='top'))
            d.add(elm.Diode().right().label('$D_1$ (Ideal)'))
            d.add(elm.Line().right().length(1.0))
            d.push()
            d.add(elm.Resistor().down().label(f'$R_L = {p["RL"]}$ k$\\Omega$', loc='bottom'))
            d.add(elm.Line().left().length(3.3))
            d.pop()
            d.add(elm.Dot(open=True).label('$+v_o(t)-$', loc='right'))

        elif circuit_type == "ctfwr":
            S1 = d.add(elm.SourceSin().up().label(f'$V_m = {p["Vm"]}$ V', loc='top'))
            d.add(elm.Diode().right().label('$D_1$'))
            d.add(elm.Line().right().length(1.2))
            top_node = d.here
            d.add(elm.Ground().at(S1.start))
            d.add(elm.Resistor().right().at(S1.start).label(f'$R_L = {p["RL"]}$ k$\\Omega$'))
            r_end = d.here
            d.add(elm.SourceSin().down().at(S1.start).label(f'$V_m = {p["Vm"]}$ V', loc='top'))
            d.add(elm.Diode().right().label('$D_2$'))
            d.add(elm.Line().right().length(1.2))
            d.add(elm.Line().up().to(top_node))
            d.add(elm.Line().at(top_node).to(r_end))

        elif circuit_type == "bridge":
            d.add(elm.SourceSin().up().label(f'$V_m = {p["Vm"]}$ V\n50 Hz', loc='top'))
            d.add(elm.Line().right().length(1.4))
            d.add(elm.Diode().theta(45).label('$D_1$'))
            dc_pos = d.here
            d.add(elm.Diode().theta(-45).reverse().label('$D_3$'))
            right_ac = d.here
            d.add(elm.Diode().theta(-135).at(right_ac).label('$D_2$'))
            dc_neg = d.here
            d.add(elm.Diode().theta(135).reverse().at(dc_neg).label('$D_4$'))
            d.add(elm.Line().right().at(dc_pos).length(2.2))
            d.add(elm.Resistor().down().label(f'$R_L = {p["RL"]}$ k$\\Omega$', loc='bottom'))
            d.add(elm.Line().left().to(dc_neg))
            d.add(elm.Ground().at(dc_neg))

        elif circuit_type == "filter_analysis":
            d.add(elm.SourceSin().up().label(f'FWR Input\n$V_m = {p["Vm"]}$ V, 50 Hz', loc='top'))
            d.add(elm.Diode().right().label('Bridge FWR'))
            d.add(elm.Line().right().length(1.0))
            d.push()
            d.add(elm.Capacitor(polar=True).down().label(f'$C = {p["C"]}\\,\\mu$F', loc='bottom'))
            d.pop()
            d.add(elm.Line().right().length(1.8))
            d.add(elm.Resistor().down().label(f'$R_L = {p["RL"]}\\,\\Omega$', loc='bottom'))
            d.add(elm.Line().left().length(5.1))

        elif circuit_type == "filter_design":
            d.add(elm.SourceSin().up().label(f'FWR Input\n$V_m = {p["Vm"]}$ V, 50 Hz', loc='top'))
            d.add(elm.Diode().right().label('Bridge FWR'))
            d.add(elm.Line().right().length(1.0))
            d.push()
            d.add(elm.Capacitor(polar=True).down().label(f'$C = ?\\,\\mu$F\n(Target $\\gamma={p["gamma"]}$)', loc='bottom'))
            d.pop()
            d.add(elm.Line().right().length(2.0))
            d.add(elm.Resistor().down().label(f'$R_L = {p["RL"]}\\,\\Omega$', loc='bottom'))
            d.add(elm.Line().left().length(5.3))

        elif circuit_type == "zener":
            d.add(elm.SourceV().up().label(f'$V_{{in}} = {p["Vin"]}$ V', loc='top'))
            d.add(elm.Resistor().right().label('$R_S = ?\\,\\Omega$\n(Design)'))
            d.add(elm.Line().right().length(0.6))
            d.push()
            d.add(elm.Zener().down().reverse().label(f'$V_Z = {p["VZ"]}$ V\n$I_Z = {p["IZ"]}$ mA', loc='bottom'))
            d.pop()
            d.add(elm.Line().right().length(2.0))
            d.add(elm.Resistor().down().label(f'$R_L = {p["RL"]}\\,\\Omega$', loc='bottom'))
            d.add(elm.Line().left().length(4.9))

        return d.get_imagedata('svg').decode('utf-8')

# ==============================================================================
# 3. TWO-STAGE GATED UI & AUTO-GRADER ENGINE
# ==============================================================================
def launch_assessment(config, mcq_bank, design_builder_fn):
    num_mcqs = min(config["NUM_MCQS"], len(mcq_bank))
    mcq_total_marks = num_mcqs * config["MARKS_PER_MCQ"]
    
    # Preview count of design problems using a dummy seed
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

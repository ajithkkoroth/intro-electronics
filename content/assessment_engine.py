import hashlib
import random
import traceback
import ipywidgets as widgets
from IPython.display import display

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
# 2. TEXTBOOK-QUALITY IEEE SVG CIRCUIT RENDERER
# ==============================================================================
def render_circuit_svg(circuit_type, p):
    defs_and_style = """
    <defs>
        <marker id="arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">
            <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#b71c1c"/>
        </marker>
    </defs>
    <style>
        .ckt-svg { background:#ffffff; border:1px solid #d0d7de; border-radius:8px; margin:10px 0; width:100%; max-width:640px; height:auto; display:block; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .wire { stroke:#111111; stroke-width:1.8; fill:none; stroke-linecap:round; stroke-linejoin:round; }
        .comp { stroke:#111111; stroke-width:2.0; fill:none; stroke-linecap:round; stroke-linejoin:round; }
        .core { stroke:#111111; stroke-width:1.6; }
        .diode-body { stroke:#111111; stroke-width:1.8; fill:#111111; stroke-linejoin:round; }
        .node { fill:#111111; }
        .term { fill:#ffffff; stroke:#111111; stroke-width:1.6; }
        .curr-arrow { stroke:#b71c1c; stroke-width:1.6; fill:none; marker-end:url(#arr); }
        .math { font-family:'Times New Roman', Times, Georgia, serif; font-size:15px; font-style:italic; fill:#111111; }
        .math-bold { font-family:'Times New Roman', Times, Georgia, serif; font-size:15px; font-style:italic; font-weight:bold; fill:#0d47a1; }
        .rom { font-family:'Times New Roman', Times, Georgia, serif; font-size:14px; font-style:normal; fill:#111111; }
        .val { font-family:'Times New Roman', Times, Georgia, serif; font-size:14px; font-style:normal; font-weight:bold; fill:#0d47a1; }
        .curr-lbl { font-family:'Times New Roman', Times, Georgia, serif; font-size:14px; font-style:italic; fill:#b71c1c; font-weight:bold; }
        .sub { font-size:10.5px; font-style:normal; }
        .sub-it { font-size:10.5px; font-style:italic; }
    </style>
    """

    if circuit_type == "hwr":
        return f"""
        <svg class="ckt-svg" viewBox="0 0 600 230">
            {defs_and_style}
            <circle cx="55" cy="115" r="20" class="comp"/>
            <path d="M 44 115 Q 49.5 103 55 115 T 66 115" class="comp"/>
            <text x="18" y="82" class="math">v<tspan dy="3" class="sub-it">in</tspan><tspan dy="-3" class="rom">(t)</tspan></text>
            <line x1="55" y1="95" x2="55" y2="55" class="wire"/>
            <line x1="55" y1="55" x2="125" y2="55" class="wire"/>
            <line x1="55" y1="135" x2="55" y2="175" class="wire"/>
            <line x1="55" y1="175" x2="125" y2="175" class="wire"/>

            <path d="M 125,55 L 125,75 A 9,7.5 0 0,1 125,95 A 9,7.5 0 0,1 125,115 A 9,7.5 0 0,1 125,135 A 9,7.5 0 0,1 125,155 L 125,175" class="comp"/>
            <line x1="142" y1="68" x2="142" y2="162" class="core"/>
            <line x1="148" y1="68" x2="148" y2="162" class="core"/>
            <path d="M 165,55 L 165,75 A 9,7.5 0 0,0 165,95 A 9,7.5 0 0,0 165,115 A 9,7.5 0 0,0 165,135 A 9,7.5 0 0,0 165,155 L 165,175" class="comp"/>
            <circle cx="116" cy="68" r="2.2" class="node"/>
            <circle cx="174" cy="68" r="2.2" class="node"/>

            <text x="178" y="80" class="rom">+</text>
            <text x="175" y="112" class="math">v<tspan dy="3" class="sub-it">s</tspan><tspan dy="-3" class="rom">(t)</tspan></text>
            <text x="175" y="130" class="val"><tspan class="math-bold">V<tspan dy="3" class="sub-it">m</tspan></tspan><tspan dy="-3"> = {p['Vm']} V</tspan></text>
            <text x="179" y="162" class="rom">−</text>

            <line x1="165" y1="55" x2="285" y2="55" class="wire"/>
            <polygon points="285,43 285,67 311,55" class="diode-body"/>
            <line x1="311" y1="41" x2="311" y2="69" class="comp"/>
            <text x="290" y="34" class="math">D<tspan dy="3" class="sub">1</tspan></text>
            <line x1="311" y1="55" x2="510" y2="55" class="wire"/>

            <line x1="340" y1="43" x2="380" y2="43" class="curr-arrow"/>
            <text x="348" y="35" class="curr-lbl">i<tspan dy="3" class="sub-it">d</tspan><tspan dy="-3" class="rom">(t)</tspan></text>

            <circle cx="430" cy="55" r="3" class="node"/>
            <line x1="430" y1="55" x2="430" y2="85" class="wire"/>
            <polyline points="430,85 439,90 421,100 439,110 421,120 439,130 421,140 430,145" class="comp"/>
            <line x1="430" y1="145" x2="430" y2="175" class="wire"/>
            <circle cx="430" cy="175" r="3" class="node"/>
            <text x="446" y="110" class="math">R<tspan dy="3" class="sub-it">L</tspan><tspan dy="-3" class="val"> = {p['RL']} kΩ</tspan></text>
            <line x1="415" y1="70" x2="415" y2="100" class="curr-arrow"/>
            <text x="392" y="90" class="curr-lbl">i<tspan dy="3" class="sub-it">L</tspan></text>

            <line x1="165" y1="175" x2="510" y2="175" class="wire"/>
            <circle cx="510" cy="55" r="3.5" class="term"/>
            <circle cx="510" cy="175" r="3.5" class="term"/>
            <text x="506" y="75" class="rom">+</text>
            <text x="500" y="118" class="math">v<tspan dy="3" class="sub-it">o</tspan><tspan dy="-3" class="rom">(t)</tspan></text>
            <text x="506" y="162" class="rom">−</text>

            <circle cx="290" cy="175" r="3" class="node"/>
            <line x1="290" y1="175" x2="290" y2="193" class="wire"/>
            <line x1="276" y1="193" x2="304" y2="193" class="comp"/>
            <line x1="281" y1="199" x2="299" y2="199" class="comp"/>
            <line x1="286" y1="205" x2="294" y2="205" class="comp"/>
        </svg>"""

    elif circuit_type == "ctfwr":
        return f"""
        <svg class="ckt-svg" viewBox="0 0 620 260">
            {defs_and_style}
            <circle cx="48" cy="130" r="20" class="comp"/>
            <path d="M 37 130 Q 42.5 118 48 130 T 59 130" class="comp"/>
            <text x="12" y="96" class="math">v<tspan dy="3" class="sub-it">in</tspan><tspan dy="-3" class="rom">(t)</tspan></text>
            <line x1="48" y1="110" x2="48" y2="45" class="wire"/>
            <line x1="48" y1="45" x2="110" y2="45" class="wire"/>
            <line x1="48" y1="150" x2="48" y2="215" class="wire"/>
            <line x1="48" y1="215" x2="110" y2="215" class="wire"/>

            <path d="M 110,45 L 110,80 A 9,8.5 0 0,1 110,105 A 9,8.5 0 0,1 110,130 A 9,8.5 0 0,1 110,155 A 9,8.5 0 0,1 110,180 L 110,215" class="comp"/>
            <line x1="126" y1="55" x2="126" y2="205" class="core"/>
            <line x1="132" y1="55" x2="132" y2="205" class="core"/>
            <path d="M 148,45 L 148,60 A 9,7 0 0,0 148,77.5 A 9,7 0 0,0 148,95 A 9,7 0 0,0 148,112.5 A 9,7 0 0,0 148,130 A 9,7 0 0,0 148,147.5 A 9,7 0 0,0 148,165 A 9,7 0 0,0 148,182.5 A 9,7 0 0,0 148,200 L 148,215" class="comp"/>

            <text x="158" y="62" class="rom">+</text>
            <text x="158" y="88" class="val"><tspan class="math-bold">V<tspan dy="3" class="sub-it">m</tspan></tspan><tspan dy="-3"> = {p['Vm']} V</tspan></text>
            <text x="158" y="118" class="rom">−</text>
            <text x="158" y="150" class="rom">+</text>
            <text x="158" y="178" class="val"><tspan class="math-bold">V<tspan dy="3" class="sub-it">m</tspan></tspan><tspan dy="-3"> = {p['Vm']} V</tspan></text>
            <text x="158" y="206" class="rom">−</text>

            <circle cx="148" cy="130" r="3.2" class="node"/>
            <line x1="148" y1="130" x2="290" y2="130" class="wire"/>
            <circle cx="255" cy="130" r="3" class="node"/>
            <line x1="255" y1="130" x2="255" y2="148" class="wire"/>
            <line x1="243" y1="148" x2="267" y2="148" class="comp"/>
            <line x1="247" y1="153" x2="263" y2="153" class="comp"/>
            <line x1="251" y1="158" x2="259" y2="158" class="comp"/>
            <text x="235" y="122" class="rom">CT</text>

            <line x1="148" y1="45" x2="310" y2="45" class="wire"/>
            <polygon points="310,33 310,57 336,45" class="diode-body"/>
            <line x1="336" y1="31" x2="336" y2="59" class="comp"/>
            <text x="315" y="25" class="math">D<tspan dy="3" class="sub">1</tspan></text>
            <line x1="336" y1="45" x2="495" y2="45" class="wire"/>
            <line x1="365" y1="34" x2="405" y2="34" class="curr-arrow"/>
            <text x="375" y="26" class="curr-lbl">i<tspan dy="3" class="sub">1</tspan></text>

            <line x1="148" y1="215" x2="310" y2="215" class="wire"/>
            <polygon points="310,203 310,227 336,215" class="diode-body"/>
            <line x1="336" y1="201" x2="336" y2="229" class="comp"/>
            <text x="315" y="195" class="math">D<tspan dy="3" class="sub">2</tspan></text>
            <line x1="336" y1="215" x2="495" y2="215" class="wire"/>
            <line x1="365" y1="204" x2="405" y2="204" class="curr-arrow"/>
            <text x="375" y="196" class="curr-lbl">i<tspan dy="3" class="sub">2</tspan></text>

            <line x1="495" y1="45" x2="495" y2="215" class="wire"/>
            <circle cx="495" cy="130" r="3.2" class="node"/>
            <line x1="495" y1="130" x2="435" y2="130" class="wire"/>
            <polyline points="435,130 430,121 420,139 410,121 400,139 390,121 380,139 375,130" class="comp"/>
            <line x1="375" y1="130" x2="290" y2="130" class="wire"/>
            <text x="470" y="124" class="rom">+</text>
            <text x="295" y="124" class="rom">−</text>
            <text x="368" y="108" class="math">R<tspan dy="3" class="sub-it">L</tspan><tspan dy="-3" class="val"> = {p['RL']} kΩ</tspan></text>
            <line x1="468" y1="142" x2="432" y2="142" class="curr-arrow"/>
            <text x="442" y="158" class="curr-lbl">I<tspan dy="3" class="sub-it">dc</tspan></text>
        </svg>"""

    elif circuit_type == "bridge":
        return f"""
        <svg class="ckt-svg" viewBox="0 0 620 260">
            {defs_and_style}
            <circle cx="45" cy="125" r="19" class="comp"/>
            <path d="M 35 125 Q 40 114 45 125 T 55 125" class="comp"/>
            <line x1="45" y1="106" x2="45" y2="55" class="wire"/>
            <line x1="45" y1="55" x2="98" y2="55" class="wire"/>
            <line x1="45" y1="144" x2="45" y2="195" class="wire"/>
            <line x1="45" y1="195" x2="98" y2="195" class="wire"/>
            <path d="M 98,55 L 98,85 A 8,7.5 0 0,1 98,105 A 8,7.5 0 0,1 98,125 A 8,7.5 0 0,1 98,145 A 8,7.5 0 0,1 98,165 L 98,195" class="comp"/>
            <line x1="112" y1="70" x2="112" y2="180" class="core"/>
            <line x1="118" y1="70" x2="118" y2="180" class="core"/>
            <path d="M 132,55 L 132,85 A 8,7.5 0 0,0 132,105 A 8,7.5 0 0,0 132,125 A 8,7.5 0 0,0 132,145 A 8,7.5 0 0,0 132,165 L 132,195" class="comp"/>
            <text x="142" y="118" class="val"><tspan class="math-bold">V<tspan dy="3" class="sub-it">m</tspan></tspan><tspan dy="-3"> = {p['Vm']} V</tspan></text>
            <text x="142" y="138" class="rom">(50 Hz)</text>

            <line x1="132" y1="55" x2="300" y2="55" class="wire"/>
            <line x1="132" y1="195" x2="300" y2="195" class="wire"/>
            <circle cx="300" cy="55" r="3.2" class="node"/>
            <circle cx="300" cy="195" r="3.2" class="node"/>
            <circle cx="230" cy="125" r="3.2" class="node"/>
            <circle cx="370" cy="125" r="3.2" class="node"/>

            <line x1="230" y1="125" x2="300" y2="55" class="wire"/>
            <line x1="300" y1="55" x2="370" y2="125" class="wire"/>
            <line x1="230" y1="125" x2="300" y2="195" class="wire"/>
            <line x1="300" y1="195" x2="370" y2="125" class="wire"/>

            <g transform="translate(265,90) rotate(-45)">
                <polygon points="-11,-9 -11,9 11,0" class="diode-body"/>
                <line x1="11" y1="-10" x2="11" y2="10" class="comp"/>
            </g>
            <text x="235" y="75" class="math">D<tspan dy="3" class="sub">4</tspan></text>

            <g transform="translate(335,90) rotate(45)">
                <polygon points="-11,-9 -11,9 11,0" class="diode-body"/>
                <line x1="11" y1="-10" x2="11" y2="10" class="comp"/>
            </g>
            <text x="348" y="75" class="math">D<tspan dy="3" class="sub">1</tspan></text>

            <g transform="translate(265,160) rotate(45)">
                <polygon points="-11,-9 -11,9 11,0" class="diode-body"/>
                <line x1="11" y1="-10" x2="11" y2="10" class="comp"/>
            </g>
            <text x="235" y="182" class="math">D<tspan dy="3" class="sub">3</tspan></text>

            <g transform="translate(335,160) rotate(-45)">
                <polygon points="-11,-9 -11,9 11,0" class="diode-body"/>
                <line x1="11" y1="-10" x2="11" y2="10" class="comp"/>
            </g>
            <text x="348" y="182" class="math">D<tspan dy="3" class="sub">2</tspan></text>

            <line x1="370" y1="125" x2="485" y2="125" class="wire"/>
            <line x1="485" y1="125" x2="485" y2="145" class="wire"/>
            <polyline points="485,145 494,150 476,160 494,170 476,180 494,190 476,200 485,205" class="comp"/>
            <line x1="485" y1="205" x2="485" y2="230" class="wire"/>
            <line x1="230" y1="125" x2="230" y2="230" class="wire"/>
            <line x1="230" y1="230" x2="485" y2="230" class="wire"/>

            <circle cx="230" cy="230" r="3" class="node"/>
            <line x1="230" y1="230" x2="230" y2="242" class="wire"/>
            <line x1="218" y1="242" x2="242" y2="242" class="comp"/>
            <line x1="223" y1="247" x2="237" y2="247" class="comp"/>
            <text x="415" y="114" class="curr-lbl">I<tspan dy="3" class="sub-it">dc</tspan></text>
            <line x1="400" y1="118" x2="445" y2="118" class="curr-arrow"/>
            <text x="502" y="172" class="math">R<tspan dy="3" class="sub-it">L</tspan><tspan dy="-3" class="val"> = {p['RL']} kΩ</tspan></text>
            <text x="468" y="142" class="rom">+</text>
            <text x="468" y="222" class="rom">−</text>
        </svg>"""

    elif circuit_type in ("filter_analysis", "filter_design"):
        c_str = f"{p['C']} μF" if circuit_type == "filter_analysis" else f"? μF (γ = {p['gamma']})"
        return f"""
        <svg class="ckt-svg" viewBox="0 0 640 240">
            {defs_and_style}
            <circle cx="55" cy="120" r="22" class="comp"/>
            <path d="M 43 120 Q 49 107 55 120 T 67 120" class="comp"/>
            <text x="15" y="75" class="val"><tspan class="math-bold">V<tspan dy="3" class="sub-it">m</tspan></tspan><tspan dy="-3"> = {p['Vm']} V</tspan></text>
            <text x="18" y="93" class="rom">f = 50 Hz</text>
            <line x1="55" y1="98" x2="55" y2="55" class="wire"/>
            <line x1="55" y1="55" x2="185" y2="55" class="wire"/>
            <line x1="55" y1="142" x2="55" y2="185" class="wire"/>
            <line x1="55" y1="185" x2="185" y2="185" class="wire"/>

            <circle cx="185" cy="55" r="3" class="node"/>
            <circle cx="185" cy="185" r="3" class="node"/>
            <circle cx="120" cy="120" r="3" class="node"/>
            <circle cx="250" cy="120" r="3" class="node"/>
            <line x1="120" y1="120" x2="185" y2="55" class="wire"/>
            <line x1="185" y1="55" x2="250" y2="120" class="wire"/>
            <line x1="120" y1="120" x2="185" y2="185" class="wire"/>
            <line x1="185" y1="185" x2="250" y2="120" class="wire"/>
            <g transform="translate(152.5,87.5) rotate(-45)">
                <polygon points="-9,-7.5 -9,7.5 9,0" class="diode-body"/>
                <line x1="9" y1="-8.5" x2="9" y2="8.5" class="comp"/>
            </g>
            <g transform="translate(217.5,87.5) rotate(45)">
                <polygon points="-9,-7.5 -9,7.5 9,0" class="diode-body"/>
                <line x1="9" y1="-8.5" x2="9" y2="8.5" class="comp"/>
            </g>
            <g transform="translate(152.5,152.5) rotate(45)">
                <polygon points="-9,-7.5 -9,7.5 9,0" class="diode-body"/>
                <line x1="9" y1="-8.5" x2="9" y2="8.5" class="comp"/>
            </g>
            <g transform="translate(217.5,152.5) rotate(-45)">
                <polygon points="-9,-7.5 -9,7.5 9,0" class="diode-body"/>
                <line x1="9" y1="-8.5" x2="9" y2="8.5" class="comp"/>
            </g>

            <line x1="250" y1="120" x2="280" y2="120" class="wire"/>
            <line x1="280" y1="120" x2="280" y2="55" class="wire"/>
            <line x1="280" y1="55" x2="545" y2="55" class="wire"/>
            <line x1="120" y1="120" x2="120" y2="205" class="wire"/>
            <line x1="120" y1="205" x2="545" y2="205" class="wire"/>

            <circle cx="365" cy="55" r="3" class="node"/>
            <circle cx="365" cy="205" r="3" class="node"/>
            <line x1="365" y1="55" x2="365" y2="118" class="wire"/>
            <line x1="346" y1="118" x2="384" y2="118" class="comp"/>
            <path d="M 346,130 Q 365,122 384,130" class="comp"/>
            <line x1="365" y1="126" x2="365" y2="205" class="wire"/>
            <text x="348" y="112" class="rom">+</text>
            <text x="388" y="118" class="math">C</text>
            <text x="388" y="136" class="val">{c_str}</text>

            <circle cx="495" cy="55" r="3" class="node"/>
            <circle cx="495" cy="205" r="3" class="node"/>
            <line x1="495" y1="55" x2="495" y2="95" class="wire"/>
            <polyline points="495,95 504,100 486,110 504,120 486,130 504,140 486,150 495,155" class="comp"/>
            <line x1="495" y1="155" x2="495" y2="205" class="wire"/>
            <text x="510" y="122" class="math">R<tspan dy="3" class="sub-it">L</tspan></text>
            <text x="510" y="142" class="val">{p['RL']} Ω</text>

            <circle cx="545" cy="55" r="3.5" class="term"/>
            <circle cx="545" cy="205" r="3.5" class="term"/>
            <text x="560" y="62" class="rom">+</text>
            <text x="558" y="135" class="math">V<tspan dy="3" class="sub-it">dc</tspan></text>
            <text x="560" y="208" class="rom">−</text>
        </svg>"""

    elif circuit_type == "zener":
        return f"""
        <svg class="ckt-svg" viewBox="0 0 600 230">
            {defs_and_style}
            <line x1="65" y1="50" x2="65" y2="98" class="wire"/>
            <line x1="48" y1="98" x2="82" y2="98" class="comp"/>
            <line x1="55" y1="106" x2="75" y2="106" stroke="#111" stroke-width="3.2"/>
            <line x1="48" y1="114" x2="82" y2="114" class="comp"/>
            <line x1="55" y1="122" x2="75" y2="122" stroke="#111" stroke-width="3.2"/>
            <line x1="65" y1="122" x2="65" y2="180" class="wire"/>
            <text x="38" y="93" class="rom">+</text>
            <text x="38" y="135" class="rom">−</text>
            <text x="88" y="108" class="math">V<tspan dy="3" class="sub-it">in</tspan></text>
            <text x="88" y="126" class="val">{p['Vin']} V</text>

            <line x1="65" y1="50" x2="155" y2="50" class="wire"/>
            <polyline points="155,50 160,41 170,59 180,41 190,59 200,41 210,59 215,50" class="comp"/>
            <text x="155" y="30" class="math">R<tspan dy="3" class="sub-it">S</tspan><tspan dy="-3" class="val"> = ? Ω</tspan></text>
            <line x1="215" y1="50" x2="515" y2="50" class="wire"/>

            <line x1="230" y1="38" x2="268" y2="38" class="curr-arrow"/>
            <text x="240" y="30" class="curr-lbl">I<tspan dy="3" class="sub-it">S</tspan></text>

            <circle cx="305" cy="50" r="3.2" class="node"/>
            <circle cx="305" cy="180" r="3.2" class="node"/>
            <line x1="305" y1="50" x2="305" y2="102" class="wire"/>
            <polyline points="290,96 294,102 316,102 320,108" class="comp"/>
            <polygon points="293,128 317,128 305,102" class="diode-body"/>
            <line x1="305" y1="128" x2="305" y2="180" class="wire"/>
            <line x1="288" y1="65" x2="288" y2="95" class="curr-arrow"/>
            <text x="265" y="84" class="curr-lbl">I<tspan dy="3" class="sub-it">Z</tspan></text>
            <text x="325" y="108" class="val"><tspan class="math-bold">V<tspan dy="3" class="sub-it">Z</tspan></tspan><tspan dy="-3"> = {p['VZ']} V</tspan></text>
            <text x="325" y="128" class="val"><tspan class="math-bold">I<tspan dy="3" class="sub-it">Z</tspan></tspan><tspan dy="-3"> = {p['IZ']} mA</tspan></text>

            <circle cx="445" cy="50" r="3.2" class="node"/>
            <circle cx="445" cy="180" r="3.2" class="node"/>
            <line x1="445" y1="50" x2="445" y2="85" class="wire"/>
            <polyline points="445,85 454,90 436,100 454,110 436,120 454,130 436,140 445,145" class="comp"/>
            <line x1="445" y1="145" x2="445" y2="180" class="wire"/>
            <line x1="428" y1="65" x2="428" y2="95" class="curr-arrow"/>
            <text x="405" y="84" class="curr-lbl">I<tspan dy="3" class="sub-it">L</tspan></text>
            <text x="462" y="112" class="math">R<tspan dy="3" class="sub-it">L</tspan></text>
            <text x="462" y="130" class="val">{p['RL']} Ω</text>

            <line x1="65" y1="180" x2="515" y2="180" class="wire"/>
            <circle cx="515" cy="50" r="3.5" class="term"/>
            <circle cx="515" cy="180" r="3.5" class="term"/>
            <text x="530" y="58" class="rom">+</text>
            <text x="526" y="118" class="math">V<tspan dy="3" class="sub-it">L</tspan><tspan dy="-3" class="rom"> = </tspan><tspan class="math">V<tspan dy="3" class="sub-it">Z</tspan></tspan></text>
            <text x="530" y="182" class="rom">−</text>

            <line x1="305" y1="180" x2="305" y2="196" class="wire"/>
            <line x1="291" y1="196" x2="319" y2="196" class="comp"/>
            <line x1="296" y1="202" x2="314" y2="202" class="comp"/>
            <line x1="301" y1="208" x2="309" y2="208" class="comp"/>
        </svg>"""
    return ""

# ==============================================================================
# 3. TWO-STAGE GATED UI & AUTO-GRADER ENGINE (MOBILE-RESPONSIVE)
# ==============================================================================
def launch_assessment(config, mcq_bank, design_builder_fn):
    num_mcqs = min(config["NUM_MCQS"], len(mcq_bank))
    mcq_total_marks = num_mcqs * config["MARKS_PER_MCQ"]
    
    sample_designs = design_builder_fn(1, random.Random(1))
    num_designs = len(sample_designs)
    design_total_marks = num_designs * config["MARKS_PER_DESIGN"]
    overall_marks = mcq_total_marks + design_total_marks

    faculty_name = config.get("FACULTY_NAME", "Dr. Ajith K K")
    department = config.get("DEPARTMENT", "Department of Electronics and Communication Engineering")
    college_name = config.get("COLLEGE_NAME", "Government College of Engineering Kannur")

    # --- MOBILE-RESPONSIVE CSS OVERRIDES FOR IPYWIDGETS ---
    mobile_css = widgets.HTML("""
    <style>
        /* Fix RadioButtons overlapping on mobile by allowing multi-line height & wrapping */
        .widget-radio-box {
            height: auto !important;
            max-height: none !important;
            width: 100% !important;
        }
        .widget-radio-box label {
            white-space: normal !important;
            height: auto !important;
            line-height: 1.45 !important;
            padding: 6px 4px !important;
            margin-bottom: 4px !important;
            display: flex !important;
            align-items: flex-start !important;
            word-break: break-word !important;
        }
        .widget-radio-box input[type="radio"] {
            margin-top: 4px !important;
            margin-right: 8px !important;
            flex-shrink: 0 !important;
        }
        /* Keep buttons & inputs inside mobile screen width */
        .jupyter-button {
            max-width: 100% !important;
            white-space: normal !important;
            height: auto !important;
            min-height: 40px !important;
            line-height: 1.3 !important;
        }
    </style>
    """)

    # --- TOP HEADER BANNER ---
    header_html = widgets.HTML(f"""
    <div style="background:linear-gradient(90deg, #1e3c72, #2a5298); color:white; padding:16px; border-radius:8px; margin-bottom:14px; font-family:'Segoe UI', Arial, sans-serif; box-shadow: 0 2px 6px rgba(0,0,0,0.12); box-sizing:border-box; width:100%;">
        <div style="font-size:12px; text-transform:uppercase; letter-spacing:0.8px; color:#bbdefb; font-weight:600; margin-bottom:4px; line-height:1.4;">
            {college_name} &nbsp;|&nbsp; {department}
        </div>
        <h2 style="margin:0 0 6px 0; font-size:20px; line-height:1.3;">{config['COURSE_TITLE']}</h2>
        <div style="font-size:14px; color:#e3f2fd; margin-bottom:10px;">
            <b>Course Faculty:</b> {faculty_name}
        </div>
        <div style="background:rgba(255,255,255,0.14); padding:8px 12px; border-radius:5px; font-size:13px; display:inline-block; line-height:1.5;">
            <b>Stage 1:</b> {num_mcqs} MCQs ({mcq_total_marks} Marks) &nbsp;|&nbsp;
            <b>Stage 2:</b> {num_designs} Circuit Design Problems ({design_total_marks} Marks) &nbsp;|&nbsp;
            <b>Total: {overall_marks} Marks</b>
        </div>
    </div>
    """)

    # --- BOTTOM FOOTER BAR ---
    footer_html = widgets.HTML(f"""
    <div style="margin-top:28px; padding:14px 14px; background:#f1f5f9; border-top:3px solid #1e3c72; border-radius:6px; text-align:center; font-family:'Segoe UI', Arial, sans-serif; color:#334155; font-size:12.5px; line-height:1.5; box-sizing:border-box; width:100%;">
        <div><b>{config['COURSE_TITLE']}</b> — Interactive Auto-Graded CIE Assessment</div>
        <div style="margin-top:4px; color:#0f172a;">
            <b>Faculty:</b> {faculty_name} &nbsp;|&nbsp; <b>{department}</b> &nbsp;|&nbsp; <b>{college_name}</b>
        </div>
    </div>
    """)

    # Responsive student input controls that wrap cleanly on mobile phones
    roll_box = widgets.Text(
        description="Roll No:",
        placeholder="e.g., 5",
        style={'description_width': '70px'},
        layout=widgets.Layout(width='240px', max_width='100%', margin='4px 8px 4px 0')
    )
    name_box = widgets.Text(
        description="Full Name:",
        placeholder="e.g., Rahul K C",
        style={'description_width': '75px'},
        layout=widgets.Layout(width='280px', max_width='100%', margin='4px 8px 4px 0')
    )
    start_btn = widgets.Button(
        description="Start Assignment",
        button_style='primary',
        icon='play',
        layout=widgets.Layout(width='200px', max_width='100%', height='40px', margin='6px 0')
    )

    student_bar = widgets.Box(
        [roll_box, name_box, start_btn],
        layout=widgets.Layout(
            display='flex',
            flex_flow='row wrap',
            align_items='center',
            width='100%',
            margin='4px 0 10px 0'
        )
    )

    stage1_box = widgets.VBox([], layout=widgets.Layout(width='100%'))
    stage1_feedback = widgets.HTML("")
    stage2_box = widgets.VBox([], layout=widgets.Layout(width='100%'))
    stage2_feedback = widgets.HTML("")

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
        try:
            if not roll_box.value.strip() or not name_box.value.strip():
                stage1_feedback.value = "<p style='color:#d32f2f; font-weight:bold;'>⚠️ Please enter both your Roll Number and Full Name.</p>"
                return

            stage1_feedback.value = ""
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
                f"<h3 style='margin:0; color:#0d47a1; font-size:17px;'>🔒 Stage 1: Conceptual MCQs ({num_mcqs} × {m_per_q} = {mcq_total_marks} Marks)</h3>"
                f"<p style='margin:4px 0 0 0; font-size:14px;'>Answer all {num_mcqs} questions correctly to unlock Stage 2 (Design Problems).</p></div>"
            )]

            for i, m in enumerate(state["active_mcqs"]):
                q_html = widgets.HTML(f"<p style='margin:14px 0 6px 0; line-height:1.45;'><b>Q{i+1}. {m['q']}</b> ({m_per_q} Mark)</p>")
                rb = widgets.RadioButtons(
                    options=m["options"],
                    value=None,
                    layout=widgets.Layout(width='100%', height='auto', margin='0 0 8px 0')
                )
                state["mcq_radios"].append(rb)
                ui_list.extend([q_html, rb])

            check_mcq_btn = widgets.Button(
                description="Verify MCQs & Unlock Stage 2",
                button_style='warning',
                icon='unlock',
                layout=widgets.Layout(width='280px', max_width='100%', height='44px', margin='16px 0')
            )
            check_mcq_btn.on_click(on_verify_mcqs)
            ui_list.append(check_mcq_btn)

            stage1_box.children = tuple(ui_list)
        except Exception:
            stage1_feedback.value = f"<pre style='color:red;'>Error: {traceback.format_exc()}</pre>"

    def on_verify_mcqs(b):
        try:
            total_q = len(state["active_mcqs"])
            correct_q = 0
            wrong_list = []

            for i, m in enumerate(state["active_mcqs"]):
                if state["mcq_radios"][i].value == m["ans"]:
                    correct_q += 1
                else:
                    wrong_list.append(f"Q{i+1}")

            if correct_q < total_q:
                stage1_feedback.value = (
                    f"<div style='background:#ffebee; border-left:5px solid #c62828; padding:12px; margin:10px 0;'>"
                    f"<b>❌ Stage 1 Score: {correct_q * config['MARKS_PER_MCQ']} / {mcq_total_marks} Marks.</b> "
                    f"Please review and correct: <b>{', '.join(wrong_list)}</b> to unlock Stage 2!</div>"
                )
            else:
                b.disabled = True
                for rb in state["mcq_radios"]:
                    rb.disabled = True
                stage1_feedback.value = (
                    f"<div style='background:#e8f5e9; border-left:5px solid #2e7d32; padding:12px; margin:10px 0;'>"
                    f"<b>✅ Stage 1 Complete ({mcq_total_marks} / {mcq_total_marks} Marks)!</b> "
                    f"Stage 2 (Circuit Analysis & Design) is now unlocked below.</div>"
                )
                render_stage2()
        except Exception:
            stage1_feedback.value = f"<pre style='color:red;'>Error: {traceback.format_exc()}</pre>"

    def render_stage2():
        state["design_inputs"] = {}
        m_per_d = config["MARKS_PER_DESIGN"]

        s2_ui = [widgets.HTML(
            f"<div style='background:#e8eaf6; padding:12px; border-radius:6px; margin-top:20px;'>"
            f"<h3 style='margin:0; color:#1a237e; font-size:17px;'>🔓 Stage 2: Circuit Analysis & Design ({num_designs} × {m_per_d} = {design_total_marks} Marks)</h3>"
            f"<p style='margin:4px 0 0 0; font-size:14px;'><i>Assigned to Roll No: <b>{roll_box.value.strip().upper()}</b>. Enter numerical values accurate to 2 decimal places.</i></p></div>"
        )]

        for prob in state["active_designs"]:
            svg_diagram = render_circuit_svg(prob["circuit_type"], prob["draw_params"])
            field_widgets = []
            for f_meta in prob["fields"]:
                w = widgets.FloatText(
                    description=f_meta["label"],
                    style={'description_width': '130px'},
                    layout=widgets.Layout(width='250px', max_width='100%', margin='4px 8px 4px 0')
                )
                state["design_inputs"][f_meta["key"]] = w
                field_widgets.append(w)

            card_box = widgets.VBox([
                widgets.HTML(
                    f"<div style='background:#fafafa; padding:12px; border:1px solid #ddd; border-left:4px solid #1976d2; border-radius:6px; margin-top:15px; box-sizing:border-box;'>"
                    f"<h4 style='margin:0 0 6px 0;'>{prob['title']} ({m_per_d} Marks)</h4>"
                    f"<p style='margin:0 0 10px 0; line-height:1.45;'>{prob['desc']}</p>{svg_diagram}</div>"
                ),
                widgets.Box(field_widgets, layout=widgets.Layout(display='flex', flex_flow='row wrap', width='100%', margin='8px 0 10px 0'))
            ], layout=widgets.Layout(width='100%'))
            s2_ui.append(card_box)

        verify_s2_btn = widgets.Button(
            description="Verify All Design Problems & Generate Code",
            button_style='success',
            icon='check-circle',
            layout=widgets.Layout(width='340px', max_width='100%', height='45px', margin='20px 0')
        )
        verify_s2_btn.on_click(on_verify_stage2)
        s2_ui.append(verify_s2_btn)

        stage2_box.children = tuple(s2_ui)

    def on_verify_stage2(b):
        try:
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
                stage2_feedback.value = f"""
                <div style="background:#fff3e0; border-left:5px solid #ef6c00; padding:14px; border-radius:6px; margin-top:12px;">
                    <h4 style="margin:0 0 8px 0; color:#e65100;">🔧 Stage 2 Score: {earned_design_marks} / {design_total_marks} Marks ({passed_fields}/{total_fields} Parameters Correct)</h4>
                    <p style="margin:0 0 8px 0;">Correct parameter boxes are locked. Recalculate the items marked with ❌ and click Verify again:</p>
                    <ul style="margin:0; padding-left:20px;">{''.join(feedback_rows)}</ul>
                </div>
                """
            else:
                b.disabled = True
                ver_code = make_verification_code(roll_box.value, name_box.value, config)
                stage2_feedback.value = f"""
                <div style="background:linear-gradient(135deg, #e8f5e9, #c8e6c9); border:3px solid #2e7d32; padding:18px; border-radius:10px; margin-top:18px; text-align:center; font-family:'Segoe UI', Arial, sans-serif; box-sizing:border-box;">
                    <div style="font-size:12px; color:#2e7d32; font-weight:bold; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;">
                        {college_name} • {department}
                    </div>
                    <h2 style="color:#1b5e20; margin:0 0 8px 0; font-size:20px;">🎉 Congratulations, {name_box.value.strip()}!</h2>
                    <p style="font-size:15px; margin:0 0 14px 0; line-height:1.45;">
                        You have mastered all {num_mcqs} MCQs ({mcq_total_marks} Marks) and solved all {num_designs} Circuit Design Problems ({design_total_marks} Marks)
                        for a total score of <b>{overall_marks} / {overall_marks} Marks</b>!
                    </p>
                    <div style="background:#ffffff; border:2px dashed #1b5e20; display:inline-block; padding:12px 18px; border-radius:8px; margin-bottom:12px; max-width:100%; box-sizing:border-box;">
                        <span style="font-size:11.5px; color:#555; display:block;">VERIFICATION CODE ({faculty_name})</span>
                        <span style="font-size:20px; font-family:monospace; font-weight:bold; color:#0d47a1; letter-spacing:1.5px; word-break:break-all;">{ver_code}</span>
                    </div>
                    <p style="font-size:13.5px; color:#333; margin:0;">📋 Share this code with <b>{faculty_name}</b> / TA for CIE verification.</p>
                </div>
                """
        except Exception:
            stage2_feedback.value = f"<pre style='color:red;'>Error: {traceback.format_exc()}</pre>"

    start_btn.on_click(on_start_clicked)
    main_container = widgets.VBox([
        mobile_css,
        header_html,
        student_bar,
        stage1_box,
        stage1_feedback,
        stage2_box,
        stage2_feedback,
        footer_html
    ], layout=widgets.Layout(width='100%', max_width='100%'))
    display(main_container)

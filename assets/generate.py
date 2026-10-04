"""Generate the hand-drawn "Pandora field journal" SVGs for the GitHub profile README.

Run from the repo root:  python assets/generate.py assets
Fonts (OFL) live in assets/fonts and are subset + embedded into each SVG, because
GitHub serves README images in a sandbox where external fonts never load.
"""
import base64, html, io, math, os, random, re, sys

from fontTools import subset

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT_FILES = {"Hand": "Caveat-SemiBold.ttf", "Serif": "Fraunces-Display.ttf", "SerifItalic": "Fraunces-Italic.ttf"}

HAND, SERIF, SERIF_I = "'Hand',cursive", "'Serif',Georgia,serif", "'SerifItalic',Georgia,serif"
BG, CARD = "#0e1517", "#131d1f"
CREAM, DIM, FAINT = "#e9dfc7", "#9c9482", "#263335"
TEAL, AMBER = "#7fd8c3", "#e3a857"


# ───────────────────────────── shared pieces ─────────────────────────────
def defs(extra=""):
    return f"""<defs>
    <filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="1" result="n">
        <animate attributeName="seed" values="1;4;7;2" dur="0.8s" calcMode="discrete" repeatCount="indefinite"/>
      </feTurbulence>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.4" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="wash" x="-40%" y="-40%" width="180%" height="180%">
      <feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="3" seed="8" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="46" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feGaussianBlur in="d" stdDeviation="2.5"/>
    </filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix values="0 0 0 0 .91  0 0 0 0 .87  0 0 0 0 .78  0 0 0 .06 0"/>
    </filter>
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="dotgrid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="#1f2b2c"/></pattern>
    <radialGradient id="vig" cx=".5" cy=".5" r=".75">
      <stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/>
    </radialGradient>
    {extra}
  </defs>"""


STYLE = """
  /*FONTS*/
  .boil{filter:url(#rough);}
  .pulse{animation:pulse var(--t,3s) ease-in-out infinite;}
  @keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
  .bob{animation:bob var(--t,9s) ease-in-out infinite;}
  @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
  .redraw{stroke-dasharray:var(--l);animation:redraw var(--t,9s) ease-in-out infinite;}
  @keyframes redraw{0%,62%{stroke-dashoffset:0;opacity:1}68%{stroke-dashoffset:0;opacity:0}69%{stroke-dashoffset:var(--l);opacity:1}100%{stroke-dashoffset:0}}
  .drift{animation:drift var(--t,26s) linear infinite;}
  @keyframes drift{0%{transform:translate(0,0);opacity:0}8%{opacity:1}50%{transform:translate(var(--dx),-120px)}92%{opacity:1}100%{transform:translate(0,-240px);opacity:0}}
  .blink{animation:blink 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
  @keyframes blink{0%,45%,49%,100%{transform:scaleY(1)}47%{transform:scaleY(.08)}}
  .sway{animation:sway 7s ease-in-out infinite;transform-box:fill-box;transform-origin:top center;}
  @keyframes sway{0%,100%{transform:rotate(-1.2deg)}50%{transform:rotate(1.2deg)}}
  .march{animation:march 2.2s linear infinite;}
  @keyframes march{to{stroke-dashoffset:-24}}
  @media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def paper(W, H, rx=14):
    return f"""<clipPath id="page"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>
  <g clip-path="url(#page)">
    <rect width="{W}" height="{H}" fill="{BG}"/>
    <rect width="{W}" height="{H}" fill="url(#dotgrid)"/>
    <rect width="{W}" height="{H}" filter="url(#grain)"/>
    <rect width="{W}" height="{H}" fill="url(#vig)"/>"""


def svg_open(W, H, label, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">\n  <title>{title}</title>')


def tape(x, y, w, rot):
    return (f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" fill="{CREAM}" opacity=".13" '
            f'transform="rotate({rot} {x} {y})" filter="url(#wash)"/>'
            f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" fill="{CREAM}" opacity=".08" '
            f'transform="rotate({rot} {x} {y})"/>')


def arrow(x1, y1, x2, y2, bend=30, color=DIM, width=1.6):
    """A loose hand-drawn arrow with a slightly open head."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / n * bend, my + dx / n * bend
    ang = math.atan2(y2 - cy, x2 - cx)
    h1 = (x2 - 11 * math.cos(ang - .45), y2 - 11 * math.sin(ang - .45))
    h2 = (x2 - 11 * math.cos(ang + .5), y2 - 11 * math.sin(ang + .5))
    return (f'<path d="M{x1:.0f} {y1:.0f} Q{cx:.0f} {cy:.0f} {x2:.0f} {y2:.0f} M{h1[0]:.1f} {h1[1]:.1f} L{x2} {y2} '
            f'L{h2[0]:.1f} {h2[1]:.1f}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def swoosh(x1, x2, y, color=TEAL, t=9, delay=0, width=3):
    """Hand-drawn underline that is periodically redrawn."""
    L = int((x2 - x1) * 1.15)
    q = (x2 - x1) / 4
    return (f'<path class="redraw" d="M{x1} {y + 2} C{x1 + q} {y - 4} {x1 + 2 * q} {y + 5} {x1 + 3 * q} {y - 1} '
            f'S{x2 - 10} {y - 3} {x2} {y + 1}" stroke="{color}" stroke-width="{width}" fill="none" '
            f'stroke-linecap="round" style="--l:{L};--t:{t}s;animation-delay:-{delay}s"/>')


def specks(rnd, n, W, H, avoid=None):
    out = []
    for _ in range(n):
        x, y = rnd.uniform(20, W - 20), rnd.uniform(20, H - 20)
        if avoid and avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3]:
            continue
        s = rnd.uniform(2, 4)
        out.append(f'<path class="pulse" d="M{x - s:.0f} {y:.0f} H{x + s:.0f} M{x:.0f} {y - s:.0f} V{y + s:.0f}" '
                   f'stroke="{DIM}" stroke-width="1" style="--t:{rnd.uniform(3, 7):.1f}s;animation-delay:-{rnd.uniform(0, 6):.1f}s"/>')
    return "".join(out)


def woodsprite(x, y, dx, t, delay, scale=1):
    """An atokirina seed, drawn in ink with a faint glowing heart."""
    legs = "".join(f'<path d="M0 0 C{a * .3:.1f} -6 {a * .7:.1f} -10 {a:.1f} {-14 + abs(a) * .4:.1f}"/>'
                   for a in (-12, -7, -2, 3, 8, 12))
    return (f'<g transform="translate({x} {y}) scale({scale})"><g class="drift" '
            f'style="--t:{t}s;--dx:{dx}px;animation-delay:-{delay}s">'
            f'<g stroke="{CREAM}" stroke-width=".9" fill="none" stroke-linecap="round" opacity=".85">{legs}</g>'
            f'<circle r="5" fill="{TEAL}" opacity=".25" filter="url(#glow)"/><circle r="1.8" fill="{CREAM}"/></g></g>')


def embed_fonts(svg):
    chars = set(html.unescape("".join(re.findall(r">([^<>]+)<", svg)))) | {" "}
    css = []
    for fam, fn in FONT_FILES.items():
        if f"'{fam}'" not in svg:
            continue
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["kern", "liga", "calt", "clig"]
        opts.name_IDs = []
        font = subset.load_font(os.path.join(FONT_DIR, fn), opts)
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(chars)))
        sub.subset(font)
        buf = io.BytesIO()
        subset.save_font(font, buf, opts)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff;base64,{b64}) format('woff');}}")
    return svg.replace("/*FONTS*/", "".join(css))


# ───────────────────────────── HEADER ─────────────────────────────
MOUNTAIN = ("M-62 0 C-55 -18 -38 -30 -14 -34 C8 -38 40 -30 62 -6 C66 4 58 10 50 18 C40 40 28 72 12 112 "
            "C6 126 -2 128 -6 112 C-16 76 -30 44 -48 22 C-58 14 -66 8 -62 0 Z")


def hatch(x0, y0, x1, y1, gap=6, color=DIM, opacity=.45):
    lines = []
    k = x0 - (y1 - y0)
    while k < x1:
        lines.append(f"M{k:.0f} {y1} L{k + (y1 - y0):.0f} {y0}")
        k += gap
    return f'<path d="{" ".join(lines)}" stroke="{color}" stroke-width=".8" opacity="{opacity}"/>'


def ink_mountain(rnd, cid, detail=True, stroke=CREAM):
    tufts = []
    x = -58
    while x < 58:
        h = rnd.uniform(4, 9)
        tufts.append(f"M{x:.0f} {-12 - (1 - (x / 62) ** 2) * 20:.0f} l2 -{h:.0f} l2 {h:.0f}")
        x += rnd.uniform(5, 9)
    trees = ""
    if detail:
        for tx, th in [(-30, 22), (-12, 30), (18, 26), (38, 18)]:
            ty = -12 - (1 - (tx / 62) ** 2) * 22
            trees += (f'<path d="M{tx} {ty:.0f} v-{th} M{tx} {ty - th * .6:.0f} q-8 -4 -10 -12 M{tx} {ty - th * .8:.0f} '
                      f'q7 -4 9 -10" stroke="{stroke}" stroke-width="1" fill="none"/>'
                      f'<path d="M{tx - 9} {ty - th:.0f} q9 -14 18 0 q-9 6 -18 0 z" stroke="{stroke}" stroke-width="1" fill="none"/>')
    vines = "".join(f'<path d="M{vx} {vy} q{rnd.uniform(-5, 5):.0f} {vl / 2:.0f} {rnd.uniform(-4, 4):.0f} {vl}" '
                    f'stroke="{DIM}" stroke-width=".9" fill="none"/>'
                    for vx, vy, vl in [(-44, 16, 34), (-30, 30, 50), (-16, 44, 62), (24, 40, 44), (40, 22, 30)])
    hatching = ""
    if detail:
        hatching = (f'<clipPath id="{cid}"><path d="{MOUNTAIN}"/></clipPath>'
                    f'<g clip-path="url(#{cid})">{hatch(8, -40, 70, 130)}{hatch(-70, 30, 70, 130, gap=9, opacity=.25)}</g>')
    return (f'{hatching}<path d="{MOUNTAIN}" stroke="{stroke}" stroke-width="1.6" fill="none" stroke-linejoin="round"/>'
            f'<path d="M-50 -2 C-30 6 -10 2 6 8 S40 4 56 10" stroke="{stroke}" stroke-width=".8" fill="none" opacity=".6"/>'
            f'<path d="{" ".join(tufts)}" stroke="{stroke}" stroke-width=".9" fill="none"/>{trees}{vines}')


IKRAN_INK = f"""<g>
      <g><animateTransform attributeName="transform" type="scale" values="1 1;1 .2;1 1" dur="1.2s" repeatCount="indefinite"/>
        <path d="M-6 -2 C-10 -20 -2 -36 14 -46 C8 -30 10 -16 12 -2" stroke="{CREAM}" stroke-width="1.3" fill="{BG}"/>
        <path d="M-6 2 C-10 20 -2 36 14 46 C8 30 10 16 12 2" stroke="{CREAM}" stroke-width="1.3" fill="{BG}"/>
        <path d="M0 -8 L8 -36 M0 8 L8 36" stroke="{DIM}" stroke-width=".8"/>
      </g>
      <path d="M-24 0 C-12 -4 12 -4 24 0 C12 4 -12 4 -24 0 Z" stroke="{CREAM}" stroke-width="1.3" fill="{BG}"/>
      <path d="M24 0 L36 -3 L32 0 L36 3 Z M-24 0 L-38 -4 M-24 0 L-38 4" stroke="{CREAM}" stroke-width="1.1" fill="none"/>
    </g>"""


def header():
    rnd = random.Random(3)
    W, H = 1200, 460
    body = f"""{svg_open(W, H, "Field notes of Shramik Masti, Java developer at Telusko", "Shramik Masti · Field Notes")}
  {defs()}
  <style>{STYLE}</style>
  {paper(W, H)}
    {specks(rnd, 26, W, H, avoid=(520, 90, 1180, 420))}

    <!-- fig. 1: floating mountains -->
    <ellipse cx="250" cy="200" rx="170" ry="150" fill="{TEAL}" opacity=".10" filter="url(#wash)"/>
    <g class="boil">
      <g transform="translate(440 112) scale(.62)"><g class="bob" style="--t:11s;animation-delay:-4s">{ink_mountain(rnd, "mc2", False, DIM)}</g></g>
      <g transform="translate(250 196) scale(1.75)"><g class="bob" style="--t:9s">
        {ink_mountain(rnd, "mc1")}
        <path class="march" d="M28 -6 C30 30 27 70 31 128" stroke="{TEAL}" stroke-width="1.2" stroke-dasharray="3 5" fill="none" opacity=".8"/>
        <path class="march" d="M33 -4 C35 30 33 70 36 120" stroke="{TEAL}" stroke-width=".8" stroke-dasharray="2 6" fill="none" opacity=".5" style="animation-delay:-.7s"/>
      </g></g>
      <g transform="translate(90 330) scale(.4)"><g class="bob" style="--t:12s;animation-delay:-7s">{ink_mountain(rnd, "mc3", False, DIM)}</g></g>
      <g><animateMotion dur="20s" repeatCount="indefinite" rotate="auto" path="M70 150 C110 40 400 30 450 140 C480 230 300 260 200 250 C100 240 40 230 70 150 Z"/>
        <g transform="scale(.75)">{IKRAN_INK}</g></g>
    </g>

    <g font-family="{HAND}" fill="{DIM}">
      <text x="372" y="318" font-size="25" transform="rotate(-4 372 318)">Hallelujah Mts.</text>
      <text x="380" y="343" font-size="20" transform="rotate(-4 380 343)">(gravity: optional)</text>
      <text x="64" y="72" font-size="21" transform="rotate(-3 64 72)">ikran, circling</text>
      <text x="200" y="440" font-size="20">fig. 1</text>
    </g>
    {arrow(370, 300, 330, 268, -18)}
    {arrow(110, 80, 150, 112, 14)}

    {woodsprite(470, 430, 26, 30, 4, 1.1)}
    {woodsprite(140, 470, -20, 36, 20, .8)}

    <!-- title block -->
    <g>
      <text x="566" y="140" font-family="{HAND}" font-size="34" fill="{TEAL}" transform="rotate(-3 566 140)">field notes of</text>
      <text x="556" y="232" font-family="{SERIF}" font-size="86" fill="{CREAM}" letter-spacing="-1">Shramik Masti</text>
      {swoosh(566, 1080, 256)}
      <text x="560" y="306" font-family="{SERIF_I}" font-size="29" fill="{CREAM}">Java developer at Telusko.</text>
      <text x="560" y="350" font-family="{HAND}" font-size="28" fill="{DIM}">I build backends with Spring Boot, and lately</text>
      <text x="560" y="382" font-family="{HAND}" font-size="28" fill="{DIM}">AI agents that actually make it to production.</text>
    </g>
    <g transform="rotate(-1.5 1010 420)">
      <rect class="boil" x="850" y="400" width="316" height="36" fill="none" stroke="{DIM}" stroke-width="1"/>
      <text x="1008" y="423" text-anchor="middle" font-family="{SERIF}" font-size="13" letter-spacing="3" fill="{DIM}">ENTRY Nº 01  ·  PUNE, EARTH  ·  2026</text>
    </g>
    {tape(70, 18, 120, -8)}{tape(1135, 20, 110, 7)}
  </g>
</svg>"""
    return body


# ───────────────────────────── JOURNEY (trail map) ─────────────────────────────
STOPS = [
    (120, 205, "2020", "BSc Computer Science", "Dr. Ghali College", "book"),
    (355, 128, "2023", "MCA", "D.Y. Patil Agri &amp; Tech University", "cap"),
    (595, 214, "Apr 2024", "Java Developer Intern", "Code Crafter Services", "tent"),
    (835, 122, "Mar 2025", "Java Developer", "Telusko", "tree"),
    (1070, 186, "now", "Agentic AI", "Spring AI, LangGraph, MCP", "flag"),
]


def icon(kind, x, y):
    s = f'stroke="{CREAM}" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "book":
        return (f'<path d="M{x - 22} {y - 6} q11 -6 22 0 q11 -6 22 0 v-26 q-11 -6 -22 0 q-11 -6 -22 0 z M{x} {y - 6} v-26 '
                f'M{x - 17} {y - 24} q6 -3 12 0 M{x - 17} {y - 17} q6 -3 12 0 M{x + 5} {y - 24} q6 -3 12 0" {s}/>')
    if kind == "cap":
        return (f'<path d="M{x - 26} {y - 26} L{x} {y - 38} L{x + 26} {y - 26} L{x} {y - 15} Z M{x - 14} {y - 21} v10 '
                f'q14 8 28 0 v-10 M{x + 20} {y - 23} v14 l-3 6 h6 l-3 -6" {s}/>')
    if kind == "tent":
        return (f'<path d="M{x - 26} {y - 6} L{x} {y - 42} L{x + 26} {y - 6} Z M{x} {y - 42} L{x - 6} {y - 6} M{x} {y - 42} '
                f'L{x + 7} {y - 6} M{x - 30} {y - 6} h60 M{x + 32} {y - 8} q4 -10 0 -16 q6 6 4 16" {s}/>')
    if kind == "tree":
        return (f'<path d="M{x - 4} {y - 6} q2 -16 -2 -30 M{x + 5} {y - 6} q-2 -16 2 -30 M{x - 8} {y - 6} q-6 -2 -10 2 '
                f'M{x + 9} {y - 6} q6 -2 10 2 M{x - 26} {y - 40} q-6 -14 10 -18 q4 -14 20 -10 q14 -8 22 6 q14 2 8 18 '
                f'q-10 10 -24 6 q-10 6 -22 0 q-12 2 -14 -2 z" {s}/>'
                f'<circle class="pulse" cx="{x - 10}" cy="{y - 48}" r="1.6" fill="{TEAL}" style="--t:3s"/>'
                f'<circle class="pulse" cx="{x + 12}" cy="{y - 52}" r="1.6" fill="{TEAL}" style="--t:4s;animation-delay:-1s"/>')
    return (f'<path d="M{x} {y - 6} v-44 M{x} {y - 50} q12 -6 24 0 q-12 6 0 12 q-12 -6 -24 0" {s}/>'
            f'<path d="M{x} {y - 50} q12 -6 24 0 q-12 6 0 12 q-12 -6 -24 0 z" fill="{TEAL}" opacity=".25"/>')


def contours(rnd, cx, cy, rings, base):
    out = []
    phases = [rnd.uniform(0, 6.28) for _ in range(3)]
    for r in range(rings):
        rad = base + r * 16
        pts = []
        for i in range(49):
            a = i / 48 * 2 * math.pi
            k = 1 + .12 * math.sin(3 * a + phases[0]) + .08 * math.sin(5 * a + phases[1]) + .05 * math.sin(2 * a + phases[2])
            pts.append(f"{cx + math.cos(a) * rad * k * 1.5:.0f} {cy + math.sin(a) * rad * k:.0f}")
        out.append("M" + " L".join(pts) + "Z")
    return f'<path d="{" ".join(out)}" stroke="{FAINT}" stroke-width="1" fill="none"/>'


def journey():
    rnd = random.Random(9)
    W, H = 1200, 360
    pts = [(-20, 250)] + [(x, y) for x, y, *_ in STOPS] + [(1230, 150)]
    d = f"M{pts[0][0]} {pts[0][1]}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx = (x1 - x0) * .45
        d += f" C{x0 + mx:.0f} {y0 + rnd.uniform(-30, 30):.0f} {x1 - mx:.0f} {y1 + rnd.uniform(-30, 30):.0f} {x1} {y1}"
    stops = []
    for x, y, year, title, place, kind in STOPS:
        stops.append(f"""<g class="boil">{icon(kind, x, y - 16)}
      <path d="M{x - 6} {y - 6} L{x + 6} {y + 6} M{x + 6} {y - 6} L{x - 6} {y + 6}" stroke="{TEAL}" stroke-width="2.4" stroke-linecap="round"/></g>
    <g text-anchor="middle">
      <text x="{x}" y="{y + 40}" font-family="{HAND}" font-size="27" fill="{TEAL}">{year}</text>
      <text x="{x}" y="{y + 64}" font-family="{SERIF}" font-size="17" fill="{CREAM}">{title}</text>
      <text x="{x}" y="{y + 86}" font-family="{HAND}" font-size="20" fill="{DIM}">{place}</text>
    </g>""")
    return f"""{svg_open(W, H, "The trail so far: BSc 2020, MCA 2023, intern at Code Crafter Services 2024, Java developer at Telusko 2025, now agentic AI", "The Trail So Far")}
  {defs()}
  <style>{STYLE}</style>
  {paper(W, H)}
    {contours(rnd, 250, 300, 5, 18)}{contours(rnd, 720, 60, 4, 20)}{contours(rnd, 1120, 330, 4, 14)}
    <text x="40" y="52" font-family="{HAND}" font-size="34" fill="{TEAL}" transform="rotate(-2 40 52)">the trail so far</text>
    <text x="44" y="78" font-family="{HAND}" font-size="20" fill="{DIM}">(not to scale)</text>
    <path class="boil" d="{d}" stroke="{DIM}" stroke-width="1.8" stroke-dasharray="1 9" stroke-linecap="round" fill="none"/>
    <g><circle r="9" fill="{TEAL}" opacity=".25" filter="url(#glow)"/><circle r="3.2" fill="{TEAL}"/>
      <animateMotion dur="18s" repeatCount="indefinite" path="{d}"/></g>
    {"".join(stops)}
    <text x="926" y="96" font-family="{HAND}" font-size="23" fill="{CREAM}" transform="rotate(-5 926 96)">you are here</text>
    {arrow(1034, 88, 1066, 116, -14, CREAM)}
    <g class="boil" transform="translate(1146 62)">
      <g><animateTransform attributeName="transform" type="rotate" values="-8;6;-8" dur="9s" repeatCount="indefinite"/>
        <path d="M0 -22 L5 0 L0 22 L-5 0 Z M-22 0 L0 -4 L22 0 L0 4 Z" stroke="{DIM}" stroke-width="1.1" fill="none"/>
        <path d="M0 -22 L5 0 L-5 0 Z" fill="{AMBER}" opacity=".7"/></g>
      <text x="0" y="40" text-anchor="middle" font-family="{HAND}" font-size="17" fill="{DIM}">N</text>
    </g>
    {tape(60, 14, 100, -6)}
  </g>
</svg>"""


# ───────────────────────────── HERO (Jake Sully sketch) ─────────────────────────────
NAVI_BODY = ("M150 58 C185 55 215 70 232 100 C238 110 240 118 238 126 C246 140 256 160 262 172 "
             "C265 178 262 184 254 185 C252 190 254 194 252 198 C248 200 246 201 247 204 "
             "C250 207 250 212 245 216 C246 224 242 232 232 236 C220 240 205 240 196 246 "
             "C192 270 196 290 206 306 C240 318 290 330 318 356 L326 380 L34 380 "
             "C40 352 70 330 112 316 C126 290 128 250 122 210 C108 180 98 150 100 120 "
             "C104 86 122 62 150 58 Z")
NAVI_HAIR = ("M232 98 C214 64 180 50 146 54 C116 58 96 84 94 120 C92 150 100 176 112 204 "
             "C116 186 112 160 114 140 C118 112 132 88 156 78 C186 68 214 78 232 98 Z")
NAVI_EAR = "M146 142 C136 118 130 86 128 52 C152 74 172 102 180 128 C174 146 156 150 146 142 Z"
NAVI_STRIPES = [
    "M196 72 C204 82 206 92 202 100", "M178 66 C186 78 188 90 184 98", "M214 84 C220 92 222 100 218 106",
    "M240 140 C234 146 232 152 234 158", "M206 150 C214 160 216 170 212 178", "M190 160 C196 170 198 180 194 188",
    "M150 214 C160 222 164 232 162 242", "M148 250 C160 258 164 268 162 278", "M150 286 C162 294 168 302 166 310",
]
NAVI_DOTS = [(244, 136), (249, 146), (253, 156), (256, 165), (226, 104), (216, 96), (205, 90), (218, 168),
             (210, 178), (200, 196), (176, 230), (172, 262), (178, 296), (262, 334)]


def jake_sketch(rnd):
    braids = "".join(
        f'<path class="sway" d="M{x0} 150 C{x0 - 20 + s} 220 {x1 + s} 280 {x1} 380" stroke="{CREAM}" stroke-width="{w}" '
        f'stroke-dasharray="5 2" fill="none" stroke-linecap="round" style="animation-delay:-{i * 1.4:.1f}s"/>'
        for i, (x0, x1, s, w) in enumerate([(106, 66, 10, 2.2), (112, 84, -8, 1.6), (100, 52, 6, 1.4)]))
    beads = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{CREAM}" stroke-width=".8"/>'
                    for x, y, r, c in [(88, 238, 3.4, AMBER), (78, 268, 3, TEAL), (72, 300, 3.2, AMBER), (98, 252, 2.6, CARD)])
    stripes = "".join(f'<path d="{d}" stroke="{DIM}" stroke-width="1.3" fill="none" stroke-linecap="round"/>' for d in NAVI_STRIPES)
    dots = "".join(f'<circle class="pulse" cx="{x}" cy="{y}" r="1.5" fill="{TEAL}" '
                   f'style="--t:{rnd.uniform(2.5, 5):.1f}s;animation-delay:-{rnd.uniform(0, 5):.1f}s"/>' for x, y in NAVI_DOTS)
    hair_lines = "".join(f'<path d="M{a}" stroke="{CREAM}" stroke-width=".9" fill="none" opacity=".7"/>' for a in [
        "216 84 C190 66 150 64 128 84", "206 80 C180 70 146 76 124 100", "140 66 C116 80 104 110 106 150",
        "130 72 C110 92 102 130 108 180"])
    necklace = "".join(f'<circle cx="{150 + i * 20}" cy="{322 + (i * 20 - 70) ** 2 / 520:.0f}" r="{3.6 if i % 2 else 2.8}" '
                       f'fill="{AMBER if i % 3 == 0 else CARD}" stroke="{CREAM}" stroke-width=".8"/>' for i in range(8))
    return f"""
      <clipPath id="bodyclip"><path d="{NAVI_BODY}"/></clipPath>
      <path d="M58 120 Q-4 250 66 386" stroke="{DIM}" stroke-width="2" fill="none"/>
      <path d="M58 120 L66 386" stroke="{DIM}" stroke-width=".7"/>
      {braids}{beads}
      <path d="{NAVI_BODY}" fill="{CARD}" fill-opacity=".55" stroke="{CREAM}" stroke-width="1.8" stroke-linejoin="round"/>
      <g clip-path="url(#bodyclip)">{hatch(90, 160, 170, 380, gap=5, opacity=.4)}{hatch(60, 300, 330, 380, gap=8, opacity=.25)}</g>
      {stripes}
      <path d="{NAVI_HAIR}" fill="{BG}" stroke="{CREAM}" stroke-width="1.6"/>
      {hair_lines}
      <path d="{NAVI_EAR}" fill="{CARD}" stroke="{CREAM}" stroke-width="1.6"/>
      <path d="M154 134 C146 114 140 90 136 68" stroke="{DIM}" stroke-width="1.2" fill="none"/>
      <path d="M204 118 C214 112 228 112 238 118" stroke="{CREAM}" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M208 128 C216 120 228 119 236 124 C230 132 218 134 208 128 Z" fill="{BG}" stroke="{CREAM}" stroke-width="1.2"/>
      <circle class="blink" cx="225" cy="126" r="4" fill="{AMBER}"/>
      <path d="M249 186 C245 184 243 180 246 177" stroke="{CREAM}" stroke-width="1.4" fill="none"/>
      <path d="M244 205 C240 205 236 204 232 202" stroke="{CREAM}" stroke-width="1.2" fill="none"/>
      {dots}
      <path d="M144 318 Q220 352 300 336" stroke="{DIM}" stroke-width="1.2" fill="none"/>
      {necklace}
    """


def hero():
    rnd = random.Random(12)
    W, H = 1200, 480
    return f"""{svg_open(W, H, "The one I follow: Jake Sully, Toruk Makto. A hand-drawn sketch of Jake in his Na'vi form.", "The One I Follow · Jake Sully")}
  {defs()}
  <style>{STYLE}</style>
  {paper(W, H)}
    {specks(rnd, 14, W, H, avoid=(40, 20, 1180, 460))}

    <!-- sketch card -->
    <g transform="rotate(-2.5 250 240)">
      <rect x="48" y="36" width="410" height="412" fill="{CARD}" stroke="{FAINT}"/>
      <ellipse cx="275" cy="200" rx="135" ry="140" fill="{TEAL}" opacity=".16" filter="url(#wash)"/>
      <ellipse cx="306" cy="168" rx="30" ry="26" fill="{AMBER}" opacity=".10" filter="url(#wash)"/>
      <g class="boil" transform="translate(76 46)">{jake_sketch(rnd)}</g>
      <g font-family="{HAND}" fill="{DIM}">
        <text x="330" y="74" font-size="21">ears up:</text>
        <text x="330" y="96" font-size="21">always listening</text>
        <text x="352" y="252" font-size="21">amber eyes,</text>
        <text x="352" y="274" font-size="21">sees everything</text>
        <text x="66" y="438" font-size="20">fig. 2 · J. Sully, Na’vi form</text>
      </g>
      {arrow(326, 80, 212, 88, -16)}
      {arrow(370, 240, 312, 182, 14)}
      {tape(90, 40, 90, -24)}{tape(420, 42, 90, 22)}
    </g>

    <!-- notes -->
    <g>
      <text x="566" y="104" font-family="{HAND}" font-size="34" fill="{TEAL}" transform="rotate(-2 566 104)">the one I follow</text>
      <text x="558" y="194" font-family="{SERIF}" font-size="88" fill="{CREAM}" letter-spacing="-1">Jake Sully</text>
      <text x="564" y="234" font-family="{SERIF_I}" font-size="21" fill="{DIM}">Toruk Makto  ·  Olo’eyktan of the Omatikaya</text>
      <text x="556" y="318" font-family="{SERIF}" font-size="96" fill="{TEAL}" opacity=".45">“</text>
      <text x="604" y="294" font-family="{SERIF_I}" font-size="27" fill="{CREAM}">Sometimes your whole life boils down</text>
      <text x="604" y="330" font-family="{SERIF_I}" font-size="27" fill="{CREAM}">to one insane move.</text>
      <text x="566" y="394" font-family="{HAND}" font-size="27" fill="{DIM}">He showed up knowing nothing and learned a whole world.</text>
      <text x="566" y="426" font-family="{HAND}" font-size="27" fill="{CREAM}">Same plan for every new stack I pick up.</text>
      {swoosh(566, 960, 438, TEAL, 10, 3, 2.4)}
    </g>
  </g>
</svg>"""


# ───────────────────────────── DIVIDER & FOOTER ─────────────────────────────
def divider():
    W, H = 1200, 48
    return f"""{svg_open(W, H, "divider", "divider")}
  {defs()}
  <style>{STYLE}</style>
  <g class="boil" stroke-linecap="round" fill="none">
    <path d="M120 26 C300 22 420 30 560 25" stroke="#5d6a66" stroke-width="1.4"/>
    <path d="M640 25 C780 30 900 22 1080 26" stroke="#5d6a66" stroke-width="1.4"/>
    <path d="M572 30 C584 24 592 16 600 8 C608 16 616 24 628 30" stroke="#8a9a92" stroke-width="1.3"/>
    <path d="M600 8 C590 14 586 22 588 30 M600 8 C610 14 614 22 612 30" stroke="#8a9a92" stroke-width="1"/>
  </g>
  <circle class="pulse" cx="600" cy="32" r="2.6" fill="{TEAL}" filter="url(#glow)" style="--t:3.5s"/>
</svg>"""


def footer():
    rnd = random.Random(4)
    W, H = 1200, 250
    ferns = []
    for bx, n, flip in [(60, 6, 1), (1140, 6, -1)]:
        for i in range(n):
            x = bx + flip * i * 14
            h = rnd.uniform(40, 90)
            lean = flip * rnd.uniform(4, 22)
            ferns.append(f'<path d="M{x:.0f} {H} Q{x + lean / 3:.0f} {H - h / 2:.0f} {x + lean:.0f} {H - h:.0f}" '
                         f'stroke="{DIM}" stroke-width="1.2" fill="none"/>')
            ferns.append(f'<circle class="pulse" cx="{x + lean:.0f}" cy="{H - h:.0f}" r="2" fill="{TEAL}" '
                         f'style="--t:{rnd.uniform(2.5, 5):.1f}s;animation-delay:-{rnd.uniform(0, 4):.1f}s"/>')
    return f"""{svg_open(W, H, "Oel ngati kameie. I see you. Thanks for reading.", "Oel ngati kameie")}
  {defs()}
  <style>{STYLE}</style>
  {paper(W, H)}
    {specks(rnd, 12, W, H, avoid=(300, 40, 900, 200))}
    <g class="boil">{"".join(ferns)}</g>
    <text x="600" y="108" text-anchor="middle" font-family="{HAND}" font-size="58" fill="{CREAM}">Oel ngati kameie.</text>
    <text x="600" y="148" text-anchor="middle" font-family="{SERIF_I}" font-size="21" fill="{DIM}">I see you. Thanks for reading my field notes.</text>
    <text x="842" y="206" font-family="{HAND}" font-size="40" fill="{TEAL}" transform="rotate(-4 842 206)">Shramik</text>
    {swoosh(838, 976, 214, TEAL, 8, 2, 2)}
    {woodsprite(330, 250, 18, 28, 6, .9)}
    {woodsprite(900, 260, -16, 34, 18, .7)}
  </g>
</svg>"""


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("header.svg", header), ("journey.svg", journey), ("hero.svg", hero),
                     ("divider.svg", divider), ("footer.svg", footer)]:
        svg = embed_fonts(fn())
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg) // 1024} KB)")

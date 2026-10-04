"""Generate Pandora (Avatar) themed animated SVGs for the GitHub profile README."""
import random, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
FONT = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"

COMMON_STYLE = """
  .twinkle{animation:twinkle var(--t,4s) ease-in-out infinite;}
  @keyframes twinkle{0%,100%{opacity:.15}50%{opacity:1}}
  .pulse{animation:pulse var(--t,3s) ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
  @keyframes pulse{0%,100%{opacity:.35;transform:scale(.85)}50%{opacity:1;transform:scale(1.15)}}
  .seed{animation:rise var(--t,14s) linear infinite;opacity:0;transform-box:fill-box;}
  @keyframes rise{
    0%{transform:translate(0,0);opacity:0}
    10%{opacity:1}
    25%{transform:translate(var(--s,14px),-25%)}
    50%{transform:translate(calc(var(--s,14px) * -1),-50%)}
    75%{transform:translate(var(--s,14px),-75%)}
    90%{opacity:.9}
    100%{transform:translate(0,-100%);opacity:0}
  }
  .sway{animation:sway var(--t,6s) ease-in-out infinite;transform-box:fill-box;transform-origin:bottom center;}
  @keyframes sway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
  @media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""

DEFS_COMMON = """
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="blur40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <radialGradient id="seedg">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset=".35" stop-color="#d6fbff"/>
      <stop offset="1" stop-color="#5ef2ff" stop-opacity="0"/>
    </radialGradient>
"""


def stars(rnd, n, w, h):
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([.6, .8, 1, 1.2, 1.6])
        t = rnd.uniform(2.5, 7)
        d = rnd.uniform(0, 6)
        out.append(f'<circle class="twinkle" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dff8ff" '
                   f'style="--t:{t:.1f}s;animation-delay:-{d:.1f}s"/>')
    return "\n    ".join(out)


def seeds(rnd, n, w, y0, travel):
    """Atokirina (woodsprite seeds) drifting upward."""
    out = []
    for _ in range(n):
        x = rnd.uniform(20, w - 20)
        t = rnd.uniform(11, 22)
        d = rnd.uniform(0, 22)
        s = rnd.uniform(8, 26)
        sc = rnd.uniform(.6, 1.15)
        out.append(
            f'<g transform="translate({x:.0f} {y0}) scale({sc:.2f})"><g class="seed" '
            f'style="--t:{t:.1f}s;--s:{s:.0f}px;animation-delay:-{d:.1f}s">'
            f'<rect x="-10" y="-{travel}" width="20" height="{travel}" fill="none"/>'
            f'<circle r="9" fill="url(#seedg)" opacity=".55"/>'
            f'<g stroke="#e8fdff" stroke-width=".7" stroke-linecap="round" opacity=".9">'
            f'<path d="M0 0 C-4 -5 -7 -8 -9 -12"/><path d="M0 0 C4 -5 7 -8 9 -12"/>'
            f'<path d="M0 0 C-1 -6 -1 -10 0 -14"/><path d="M0 0 C-6 -2 -9 -4 -12 -6"/>'
            f'<path d="M0 0 C6 -2 9 -4 12 -6"/></g>'
            f'<circle r="1.8" fill="#fff"/></g></g>')
    return "\n    ".join(out)


def mountain(x, y, s, t, delay, fill, rim, falls=True, rnd=None):
    """A floating Hallelujah mountain: grassy crown, rocky body tapering to a point."""
    vines = []
    for vx, vl in [(-38, 40), (-18, 70), (12, 55), (34, 35)]:
        vines.append(f'<path d="M{vx} 8 q4 {vl/2} -2 {vl}" stroke="#1f5c55" stroke-width="1.4" fill="none" opacity=".8"/>')
    fall = ''
    if falls:
        fall = ('<path class="fall" d="M22 4 C24 40 22 90 25 150" stroke="url(#fallg)" '
                'stroke-width="3" fill="none" stroke-dasharray="6 10"/>')
    return f'''<g transform="translate({x} {y}) scale({s})">
      <g class="float" style="--t:{t}s;animation-delay:-{delay}s">
        {fall}
        <path d="M-62 0 C-55 -18 -38 -30 -14 -34 C8 -38 40 -30 62 -6 C66 4 58 10 50 18 C40 40 28 72 12 112 C6 126 -2 128 -6 112 C-16 76 -30 44 -48 22 C-58 14 -66 8 -62 0 Z" fill="{fill}"/>
        <path d="M-62 0 C-55 -18 -38 -30 -14 -34 C8 -38 40 -30 62 -6" stroke="{rim}" stroke-width="2" fill="none" opacity=".75"/>
        <path d="M-58 -8 q6 -14 14 -6 q5 -16 15 -8 q6 -14 16 -4 q8 -12 16 -2 q8 -10 15 0 q8 -8 14 4 q4 6 0 10 L-58 4 Z" fill="#0d3b3a"/>
        <g class="pulse" style="--t:3.4s;animation-delay:-{delay}s">
          <circle cx="-30" cy="-12" r="2" fill="#5ef2ff" filter="url(#glow)"/>
          <circle cx="8" cy="-16" r="1.6" fill="#c084fc" filter="url(#glow)"/>
          <circle cx="36" cy="-8" r="1.8" fill="#5ef2ff" filter="url(#glow)"/>
        </g>
        {''.join(vines)}
      </g>
    </g>'''


def plant(x, base, h, color, rnd):
    """A bioluminescent frond with glowing pods."""
    lean = rnd.uniform(-25, 25)
    t = rnd.uniform(4, 8)
    d = rnd.uniform(0, 8)
    pods = []
    for i in range(rnd.randint(2, 4)):
        f = rnd.uniform(.35, .95)
        px = x + lean * f * f
        py = base - h * f
        pods.append(f'<circle class="pulse" cx="{px:.1f}" cy="{py:.1f}" r="{rnd.uniform(1.5, 3.2):.1f}" '
                    f'fill="{color}" filter="url(#glow)" style="--t:{rnd.uniform(2, 4.5):.1f}s;animation-delay:-{rnd.uniform(0, 4):.1f}s"/>')
    return (f'<g class="sway" style="--t:{t:.1f}s;animation-delay:-{d:.1f}s">'
            f'<path d="M{x:.0f} {base} Q{x + lean * .2:.0f} {base - h * .5:.0f} {x + lean:.0f} {base - h:.0f}" '
            f'stroke="{color}" stroke-opacity=".55" stroke-width="2" fill="none" stroke-linecap="round"/>'
            f'{"".join(pods)}</g>')


def forest(rnd, w, base, n, maxh):
    colors = ["#5ef2ff", "#5ef2ff", "#38bdf8", "#c084fc", "#e879f9", "#7cffcb"]
    out = []
    for _ in range(n):
        out.append(plant(rnd.uniform(0, w), base, rnd.uniform(maxh * .35, maxh), rnd.choice(colors), rnd))
    return "\n    ".join(out)


def ground(w, h, top, rnd, fill="#020a14"):
    pts = [f"M0 {h}", f"L0 {top}"]
    x = 0
    while x < w:
        nx = x + rnd.uniform(40, 90)
        pts.append(f"Q{(x + nx) / 2:.0f} {top - rnd.uniform(4, 22):.0f} {nx:.0f} {top + rnd.uniform(-4, 6):.0f}")
        x = nx
    pts.append(f"L{w} {h} Z")
    return f'<path d="{" ".join(pts)}" fill="{fill}"/>'


# An ikran (mountain banshee) seen from below, flapping while it flies along a motion path.
IKRAN = """<g opacity=".9"><g>
      <animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto" path="{path}"/>
      <g transform="scale({sc})">
        <g><animateTransform attributeName="transform" type="scale" values="1 1;1 .25;1 1" dur="1.1s" repeatCount="indefinite"/>
          <path d="M-6 -2 C-10 -22 -2 -40 14 -50 C8 -32 10 -16 12 -2 Z" fill="#0b1a2e" stroke="#5ef2ff" stroke-opacity=".7" stroke-width="1"/>
          <path d="M-6 2 C-10 22 -2 40 14 50 C8 32 10 16 12 2 Z" fill="#0b1a2e" stroke="#5ef2ff" stroke-opacity=".7" stroke-width="1"/>
          <path d="M0 -10 C2 -24 6 -34 12 -42 M0 10 C2 24 6 34 12 42" stroke="#c084fc" stroke-width="1" fill="none" opacity=".8"/>
        </g>
        <path d="M-26 0 C-12 -5 12 -5 26 0 C12 5 -12 5 -26 0 Z" fill="#0b1a2e" stroke="#5ef2ff" stroke-opacity=".8" stroke-width="1"/>
        <path d="M26 0 L40 -3 L35 0 L40 3 Z M-26 0 L-42 -5 L-37 0 L-42 5 Z" fill="#5ef2ff" opacity=".85"/>
        <circle cx="30" cy="0" r="1.6" fill="#e879f9" filter="url(#glow)"/>
      </g>
    </g></g>"""


# ───────────────────────────── HEADER ─────────────────────────────
def header():
    rnd = random.Random(7)
    W, H = 1200, 440
    mountains = "\n    ".join([
        mountain(150, 150, .75, 9, 1, "#0a1d33", "#1e6f8a", True),
        mountain(330, 95, .45, 11, 4, "#0b1a2e", "#18506a", False),
        mountain(880, 105, .5, 10, 2, "#0b1a2e", "#18506a", False),
        mountain(1040, 175, .9, 8, 0, "#0a1d33", "#1e6f8a", True),
        mountain(60, 300, .38, 12, 6, "#081626", "#16455c", False),
        mountain(1160, 70, .32, 13, 3, "#081626", "#16455c", False),
    ])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Shramik Masti, Java Developer and Agentic AI Engineer">
  <title>Shramik Masti · Java Developer &amp; Agentic AI Engineer</title>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#01040c"/>
      <stop offset=".55" stop-color="#04122a"/>
      <stop offset="1" stop-color="#062033"/>
    </linearGradient>
    <linearGradient id="namegrad" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="#5ef2ff"/>
      <stop offset=".5" stop-color="#e0fbff"/>
      <stop offset="1" stop-color="#c084fc"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.5 0;0.5 0;-0.5 0" dur="12s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="fallg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#bff7ff" stop-opacity=".9"/>
      <stop offset="1" stop-color="#5ef2ff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="planet" cx=".35" cy=".35" r=".8">
      <stop offset="0" stop-color="#9fd8ff"/>
      <stop offset=".6" stop-color="#3b6fa8"/>
      <stop offset="1" stop-color="#0d2547"/>
    </radialGradient>
    <radialGradient id="vignette" cx=".5" cy=".5" r=".55">
      <stop offset="0" stop-color="#01040c" stop-opacity=".75"/>
      <stop offset="1" stop-color="#01040c" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="shootg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#5ef2ff" stop-opacity="0"/></linearGradient>
    <clipPath id="planetclip"><circle cx="0" cy="0" r="78"/></clipPath>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {DEFS_COMMON}
  </defs>
  <style>{COMMON_STYLE}
    .float{{animation:float var(--t,9s) ease-in-out infinite;}}
    @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-14px)}}}}
    .fall{{animation:fall 1.2s linear infinite;}}
    @keyframes fall{{to{{stroke-dashoffset:-32}}}}
    .aurora{{animation:aurora 18s ease-in-out infinite alternate;}}
    @keyframes aurora{{0%{{transform:translate(-60px,0)}}100%{{transform:translate(60px,-20px)}}}}
    .fadeup{{animation:fadeup 1.6s cubic-bezier(.2,.7,.2,1) both;}}
    @keyframes fadeup{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
    .breath{{animation:breath 5s ease-in-out infinite;}}
    @keyframes breath{{0%,100%{{opacity:.75}}50%{{opacity:1}}}}
    .shoot{{animation:shoot 9s ease-in infinite;opacity:0;}}
    @keyframes shoot{{0%,78%{{transform:translate(260px,40px);opacity:0}}80%{{opacity:1}}92%{{transform:translate(620px,160px);opacity:0}}100%{{opacity:0}}}}
    .ring{{animation:spin 90s linear infinite;transform-box:fill-box;transform-origin:center;}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>

    <!-- aurora haze -->
    <g class="aurora" opacity=".55">
      <ellipse cx="300" cy="120" rx="260" ry="70" fill="#0ea5b7" filter="url(#blur40)" opacity=".45"/>
      <ellipse cx="820" cy="90" rx="300" ry="60" fill="#7c3aed" filter="url(#blur40)" opacity=".35"/>
      <ellipse cx="600" cy="300" rx="420" ry="80" fill="#0e7490" filter="url(#blur40)" opacity=".35"/>
    </g>

    <!-- stars -->
    {stars(rnd, 90, W, 300)}

    <!-- Polyphemus, the gas giant in Pandora's sky -->
    <g transform="translate(1010 92)" opacity=".85">
      <circle r="96" fill="#5ef2ff" opacity=".08" filter="url(#softglow)"/>
      <circle r="78" fill="url(#planet)"/>
      <g clip-path="url(#planetclip)" opacity=".35">
        <rect x="-80" y="-40" width="160" height="10" fill="#cfefff"/>
        <rect x="-80" y="-14" width="160" height="6" fill="#0b2a52"/>
        <rect x="-80" y="8" width="160" height="14" fill="#cfefff" opacity=".6"/>
        <rect x="-80" y="34" width="160" height="5" fill="#0b2a52"/>
      </g>
      <circle r="78" fill="none" stroke="#bff7ff" stroke-opacity=".35"/>
    </g>

    <!-- floating mountains -->
    {mountains}

    <!-- mist -->
    <rect y="300" width="{W}" height="140" fill="#0e7490" opacity=".08" filter="url(#blur40)"/>

    <!-- bioluminescent forest floor -->
    {forest(rnd, W, 420, 70, 70)}
    {ground(W, H, 418, rnd)}
    <g>
      {"".join(f'<circle class="pulse" cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(422, 438):.0f}" r="{rnd.uniform(1, 2.2):.1f}" fill="{rnd.choice(["#5ef2ff", "#c084fc", "#7cffcb"])}" filter="url(#glow)" style="--t:{rnd.uniform(2, 5):.1f}s;animation-delay:-{rnd.uniform(0, 5):.1f}s"/>' for _ in range(45))}
    </g>

    <!-- woodsprites -->
    {seeds(rnd, 22, W, 440, 440)}

    <!-- shooting star -->
    <g class="shoot"><path d="M0 0 L-120 -40" stroke="url(#shootg)" stroke-width="2" stroke-linecap="round"/><circle r="2.2" fill="#fff" filter="url(#glow)"/></g>

    <!-- ikran in flight -->
    {IKRAN.format(path="M-120 210 C 200 120, 420 90, 640 70 S 1050 140, 1340 60", dur=26, begin=0, sc=.9)}
    {IKRAN.format(path="M1320 120 C 1000 40, 760 60, 560 40 S 160 120, -140 70", dur=34, begin=-14, sc=.55)}

    <!-- title -->
    <ellipse cx="600" cy="205" rx="420" ry="120" fill="url(#vignette)"/>
    <g text-anchor="middle" font-family="{FONT}">
      <g>
        <text x="600" y="132" font-size="14" letter-spacing="7" fill="#7dd3fc" opacity=".9">OEL NGATI KAMEIE  ·  I SEE YOU</text>
      </g>
      <g>
        <text x="600" y="212" font-size="66" font-weight="800" letter-spacing="9" fill="#5ef2ff" opacity=".35" filter="url(#softglow)">SHRAMIK MASTI</text>
        <text class="breath" x="600" y="212" font-size="66" font-weight="800" letter-spacing="9" fill="url(#namegrad)">SHRAMIK MASTI</text>
      </g>
      <g>
        <path d="M430 240 H560 M640 240 H770" stroke="#5ef2ff" stroke-opacity=".45"/>
        <circle cx="600" cy="240" r="4" fill="#5ef2ff" filter="url(#glow)"/>
        <circle cx="600" cy="240" r="10" fill="none" stroke="#5ef2ff" stroke-opacity=".5" stroke-dasharray="3 4" class="ring"/>
      </g>
      <g>
        <text x="600" y="282" font-size="22" font-weight="600" letter-spacing="2" fill="#e0f2fe">Java Developer @ Telusko  ·  Spring AI  ·  Agentic AI</text>
        <text x="600" y="314" font-size="15" letter-spacing="1.5" fill="#94c9e0">Building AI powered, production grade systems with Spring Boot, LangChain &amp; LangGraph</text>
      </g>
    </g>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#5ef2ff" stroke-opacity=".18"/>
</svg>'''
    return svg


# ───────────────────────────── DIVIDER ─────────────────────────────
def divider():
    W, H = 1200, 36
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divider">
  <defs>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0" stop-color="#5ef2ff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#5ef2ff" stop-opacity=".6"/>
      <stop offset="1" stop-color="#c084fc" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="spark"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#5ef2ff"/><stop offset="1" stop-color="#5ef2ff" stop-opacity="0"/></radialGradient>
    {DEFS_COMMON}
  </defs>
  <style>{COMMON_STYLE}
    .travel{{animation:travel 6s cubic-bezier(.45,0,.55,1) infinite;}}
    @keyframes travel{{0%{{transform:translateX(120px);opacity:0}}15%{{opacity:1}}85%{{opacity:1}}100%{{transform:translateX(1080px);opacity:0}}}}
  </style>
  <path d="M60 18 H1140" stroke="url(#line)" stroke-width="1.5"/>
  <g class="travel"><ellipse cx="0" cy="18" rx="40" ry="6" fill="url(#spark)" opacity=".8"/><circle cx="0" cy="18" r="2.5" fill="#fff"/></g>
  <g transform="translate(600 18)">
    <path d="M-14 0 L0 -8 L14 0 L0 8 Z" fill="#04122a" stroke="#5ef2ff" stroke-opacity=".8"/>
    <circle class="pulse" r="3" fill="#5ef2ff" filter="url(#glow)" style="--t:2.6s"/>
  </g>
</svg>'''


# ───────────────────────────── FOOTER ─────────────────────────────
def footer():
    rnd = random.Random(21)
    W, H = 1200, 200
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thanks for visiting">
  <defs>
    <linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#062033"/>
      <stop offset=".45" stop-color="#04122a"/>
      <stop offset="1" stop-color="#01040c"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {DEFS_COMMON}
  </defs>
  <style>{COMMON_STYLE}</style>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#fsky)"/>
    {stars(rnd, 30, W, 90)}
    {forest(rnd, W, 196, 80, 90)}
    {ground(W, H, 192, rnd)}
    {seeds(rnd, 12, W, 200, 200)}
    <g text-anchor="middle" font-family="{FONT}">
      <text x="600" y="88" font-size="26" font-weight="700" letter-spacing="6" fill="#e0fbff" filter="url(#glow)">OEL NGATI KAMEIE</text>
      <text x="600" y="118" font-size="14" letter-spacing="3" fill="#7dd3fc">I SEE YOU  ·  THANKS FOR VISITING</text>
    </g>
  </g>
</svg>'''


def braid(x0, x1, y, amp=7, waves=7):
    """Two interleaved sine strands, like a Na'vi queue."""
    import math
    out = []
    for phase in (0, math.pi):
        pts = []
        for i in range(61):
            t = i / 60
            x = x0 + (x1 - x0) * t
            pts.append(f"{x:.1f} {y + amp * math.sin(t * waves * 2 * math.pi + phase):.1f}")
        out.append("M" + " L".join(pts))
    return out


def tendrils(x, y, direction, color):
    out = []
    for i, dy in enumerate([-18, -11, -5, 0, 5, 11, 18]):
        ex = x + direction * (34 + abs(dy) * .4)
        out.append(f'<path class="tend" d="M{x} {y} C{x + direction * 14} {y} {ex - direction * 12} {y + dy} {ex} {y + dy}" '
                   f'stroke="{color}" stroke-width="1.2" fill="none" style="animation-delay:-{i * .3:.1f}s"/>')
    return "".join(out)


NAVI_DOTS = [(-14, -14, 2.4, "#5ef2ff", 2.6, 0), (-6, -20, 1.8, "#7cffcb", 3, 1), (4, -22, 1.6, "#5ef2ff", 2.2, .5),
             (14, -14, 2.4, "#5ef2ff", 2.8, 1.5), (-18, 0, 1.8, "#c084fc", 3.2, .8), (18, 0, 1.8, "#c084fc", 3.4, .2),
             (-12, 14, 2, "#5ef2ff", 2.4, 1.2), (0, 18, 2.2, "#7cffcb", 3, .4), (12, 14, 2, "#5ef2ff", 2.6, 2)]


# Original illustration of Jake Sully in his Na'vi form, drawn as a side-profile bust facing right.
NAVI_BODY = ("M150 58 C185 55 215 70 232 100 C238 110 240 118 238 126 C246 140 256 160 262 172 "
             "C265 178 262 184 254 185 C252 190 254 194 252 198 C248 200 246 201 247 204 "
             "C250 207 250 212 245 216 C246 224 242 232 232 236 C220 240 205 240 196 246 "
             "C192 270 196 290 206 306 C240 318 290 330 318 356 L326 380 L34 380 "
             "C40 352 70 330 112 316 C126 290 128 250 122 210 C108 180 98 150 100 120 "
             "C104 86 122 62 150 58 Z")
NAVI_FRONT_RIM = ("M150 58 C185 55 215 70 232 100 C238 110 240 118 238 126 C246 140 256 160 262 172 "
                  "C265 178 262 184 254 185 C252 190 254 194 252 198 C248 200 246 201 247 204 "
                  "C250 207 250 212 245 216 C246 224 242 232 232 236 C220 240 205 240 196 246 "
                  "C192 270 196 290 206 306 C240 318 290 330 318 356")
NAVI_HAIR = ("M232 98 C214 64 180 50 146 54 C116 58 96 84 94 120 C92 150 100 176 112 204 "
             "C116 186 112 160 114 140 C118 112 132 88 156 78 C186 68 214 78 232 98 Z")
NAVI_EAR = "M150 142 C134 116 122 80 114 36 C142 64 166 100 174 132 C170 146 158 148 150 142 Z"
NAVI_STRIPES = [
    "M196 72 C204 82 206 92 202 100", "M178 66 C186 78 188 90 184 98", "M214 84 C220 92 222 100 218 106",
    "M240 140 C234 146 232 152 234 158", "M206 150 C214 160 216 170 212 178", "M190 160 C196 170 198 180 194 188",
    "M150 214 C160 222 164 232 162 242", "M148 250 C160 258 164 268 162 278", "M150 286 C162 294 168 302 166 310",
]
NAVI_DOTS2 = [(244, 136, 1.8), (249, 146, 1.6), (253, 156, 1.6), (256, 165, 1.4), (226, 104, 1.6), (216, 96, 1.4),
              (205, 90, 1.6), (218, 168, 1.8), (210, 178, 1.5), (224, 186, 1.4), (200, 196, 1.6),
              (176, 230, 1.6), (172, 262, 1.6), (178, 296, 1.8), (232, 320, 1.6), (262, 334, 1.8)]


def navi_portrait(rnd):
    braids = []
    for i, (x0, x1, sway) in enumerate([(106, 66, 10), (112, 84, -8), (100, 52, 6)]):
        braids.append(f'<path class="hairsway" d="M{x0} 150 C{x0 - 20 + sway} 220 {x1 + sway} 280 {x1} 380" '
                      f'stroke="#081428" stroke-width="{7 - i * 1.5}" fill="none" stroke-linecap="round" '
                      f'style="animation-delay:-{i * 1.3:.1f}s"/>')
    beads = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in [
        (88, 238, 3.2, "#f59e0b"), (78, 268, 3, "#5ef2ff"), (72, 300, 3.2, "#e11d48"), (98, 252, 2.6, "#f8fafc")])
    stripes = "".join(f'<path d="{d}" stroke="#0a1730" stroke-width="3.2" fill="none" stroke-linecap="round" opacity=".55"/>'
                      for d in NAVI_STRIPES)
    dots = "".join(f'<circle class="pulse" cx="{x}" cy="{y}" r="{r}" fill="{"#7cffcb" if i % 4 == 0 else "#5ef2ff"}" '
                   f'filter="url(#glow)" style="--t:{rnd.uniform(2, 4):.1f}s;animation-delay:-{rnd.uniform(0, 4):.1f}s"/>'
                   for i, (x, y, r) in enumerate(NAVI_DOTS2))
    necklace = "".join(f'<circle cx="{150 + i * 20}" cy="{322 + (i * 20 - 70) ** 2 / 520:.0f}" r="{4 if i % 2 else 3}" '
                       f'fill="{"#f59e0b" if i % 3 == 0 else "#5ef2ff" if i % 3 == 1 else "#f8fafc"}"/>' for i in range(8))
    return f"""
      <circle cx="190" cy="170" r="150" fill="url(#halo)"/>
      <circle cx="190" cy="170" r="162" fill="none" stroke="#5ef2ff" stroke-opacity=".25" stroke-dasharray="2 7" class="spin"/>
      <circle cx="190" cy="170" r="176" fill="none" stroke="#c084fc" stroke-opacity=".18" stroke-dasharray="14 10" class="spinr"/>
      <path d="M58 120 Q-4 250 66 386" stroke="#c084fc" stroke-width="3" fill="none" opacity=".75"/>
      <path d="M58 120 L66 386" stroke="#e9d5ff" stroke-width=".8" opacity=".5"/>
      {"".join(braids)}
      {beads}
      <path d="{NAVI_BODY}" fill="url(#skin)"/>
      {stripes}
      <path d="{NAVI_HAIR}" fill="#081428"/>
      <path d="M150 62 C126 70 110 92 106 120" stroke="#1e3a5f" stroke-width="1.5" fill="none"/>
      <path d="{NAVI_EAR}" fill="url(#skin)" stroke="#5ef2ff" stroke-opacity=".45" stroke-width="1.2"/>
      <path d="M154 134 C142 114 132 86 126 58" stroke="#0a1730" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".6"/>
      <path class="rim" d="{NAVI_FRONT_RIM}" stroke="#5ef2ff" stroke-width="2" fill="none" filter="url(#glow)"/>
      <path d="M204 118 C214 112 228 112 238 118" stroke="#0a1730" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M208 128 C216 120 228 119 236 124 C230 132 218 134 208 128 Z" fill="#06101f"/>
      <circle class="eye" cx="226" cy="126" r="4.2" fill="#fcd34d" filter="url(#glow)"/>
      <circle cx="227" cy="125" r="1.4" fill="#06101f"/>
      <path d="M249 186 C245 184 243 180 246 177" stroke="#0a1730" stroke-width="1.8" fill="none"/>
      {dots}
      <path d="M144 318 Q220 352 300 336" stroke="#c2410c" stroke-width="1.5" fill="none"/>
      {necklace}
    """


# ───────────────────────────── HERO (Jake Sully) ─────────────────────────────
def hero():
    rnd = random.Random(11)
    W, H = 1200, 420
    left = "".join(f'<path class="strand" d="{d}" stroke="#5ef2ff" stroke-width="1.6" fill="none" opacity=".8"/>'
                   for d in braid(610, 740, 352, amp=5, waves=5))
    right = "".join(f'<path class="strand" d="{d}" stroke="#c084fc" stroke-width="1.6" fill="none" opacity=".8" '
                    f'style="animation-direction:reverse"/>' for d in braid(800, 930, 352, amp=5, waves=5))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="The hero I follow: Jake Sully, Toruk Makto. Original illustration of Jake in his Na'vi form.">
  <title>The Hero I Follow · Jake Sully</title>
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#030b1a"/><stop offset=".6" stop-color="#06182e"/><stop offset="1" stop-color="#0d1033"/>
    </linearGradient>
    <linearGradient id="skin" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1d4e89"/><stop offset=".55" stop-color="#16467a"/><stop offset="1" stop-color="#0c2a52"/>
    </linearGradient>
    <radialGradient id="halo" cx=".55" cy=".45" r=".6">
      <stop offset="0" stop-color="#0ea5b7" stop-opacity=".45"/><stop offset=".7" stop-color="#0e7490" stop-opacity=".12"/><stop offset="1" stop-color="#0e7490" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="jake" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="#5ef2ff"/><stop offset=".5" stop-color="#e0fbff"/><stop offset="1" stop-color="#c084fc"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.5 0;0.5 0;-0.5 0" dur="10s" repeatCount="indefinite"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {DEFS_COMMON}
  </defs>
  <style>{COMMON_STYLE}
    .strand{{stroke-dasharray:4 3;animation:flow 2.4s linear infinite;}}
    @keyframes flow{{to{{stroke-dashoffset:-28}}}}
    .tend{{animation:reach 3s ease-in-out infinite;}}
    @keyframes reach{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
    .spin{{animation:spin 40s linear infinite;transform-box:fill-box;transform-origin:center;}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .spinr{{animation:spin 60s linear infinite reverse;transform-box:fill-box;transform-origin:center;}}
    .rim{{animation:rim 4s ease-in-out infinite;}}
    @keyframes rim{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
    .eye{{animation:eye 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}}
    @keyframes eye{{0%,46%,54%,100%{{transform:scaleY(1)}}50%{{transform:scaleY(.1)}}}}
    .hairsway{{animation:hair 6s ease-in-out infinite;transform-box:fill-box;transform-origin:top center;}}
    @keyframes hair{{0%,100%{{transform:rotate(-1.5deg)}}50%{{transform:rotate(1.5deg)}}}}
    .breathe{{animation:breathe 7s ease-in-out infinite;}}
    @keyframes breathe{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#hbg)"/>
    <ellipse cx="860" cy="170" rx="320" ry="120" fill="#7c3aed" opacity=".14" filter="url(#blur40)"/>
    {stars(rnd, 55, W, H)}

    <!-- Jake Sully, Na'vi form (original illustration) -->
    <g transform="translate(60 34)"><g class="breathe">{navi_portrait(rnd)}</g></g>
    {seeds(rnd, 8, 460, 420, 420)}

    <!-- text -->
    <g font-family="{FONT}">
      <text x="512" y="92" font-size="13" letter-spacing="6" fill="#7dd3fc">THE HERO I FOLLOW</text>
      <text x="508" y="158" font-size="66" font-weight="800" letter-spacing="6" fill="#5ef2ff" opacity=".3" filter="url(#softglow)">JAKE SULLY</text>
      <text x="508" y="158" font-size="66" font-weight="800" letter-spacing="6" fill="url(#jake)">JAKE SULLY</text>
      <text x="512" y="194" font-size="16" font-weight="600" letter-spacing="1.5" fill="#e9d5ff">Toruk Makto  ·  Olo'eyktan of the Omatikaya</text>
      <path d="M512 216 H1150" stroke="#5ef2ff" stroke-opacity=".25"/>
      <text x="512" y="252" font-size="19" font-style="italic" fill="#e0f2fe">"Sometimes your whole life boils down to one insane move."</text>
      <text x="512" y="286" font-size="14" letter-spacing=".5" fill="#94c9e0">He arrived knowing nothing and learned a whole world. That is how I approach every new stack.</text>
    </g>

    <!-- tsaheylu: Na'vi and code, bonded -->
    <g transform="translate(560 352)">
      <circle r="20" fill="#04122a" stroke="#5ef2ff" stroke-opacity=".6"/>
      <circle r="8" fill="url(#seedg)"/><circle r="2" fill="#fff"/>
    </g>
    {left}{right}
    {tendrils(740, 352, 1, "#bff7ff")}
    {tendrils(800, 352, -1, "#e9d5ff")}
    <circle r="3" fill="#fff" filter="url(#glow)"><animateMotion dur="2.4s" repeatCount="indefinite" path="M580 352 L960 352"/></circle>
    <g transform="translate(980 352)">
      <circle r="20" fill="#04122a" stroke="#c084fc" stroke-opacity=".6"/>
      <text y="5" text-anchor="middle" font-family="Consolas,'Fira Code',monospace" font-size="13" font-weight="700" fill="#e9d5ff">&lt;/&gt;</text>
    </g>
    <text x="1020" y="348" font-family="{FONT}" font-size="11" letter-spacing="3" fill="#94c9e0">TSAHEYLU</text>
    <text x="1020" y="364" font-family="{FONT}" font-size="11" letter-spacing="1" fill="#64748b">Na'vi meets code</text>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#5ef2ff" stroke-opacity=".18"/>
</svg>"""


# ───────────────────────────── JOURNEY ─────────────────────────────
JOURNEY = [
    ("2020", "BSc Computer Science", "Dr. Ghali College", "THE ARRIVAL"),
    ("2023", "MCA", "D.Y. Patil Agri &amp; Tech University", "LEARNING THE WAYS"),
    ("APR 2024", "Java Developer Intern", "Code Crafter Services", "FIRST IKRAN"),
    ("MAR 2025", "Java Developer", "Telusko", "JOINING THE CLAN"),
    ("NOW", "Agentic AI Engineering", "Spring AI · LangGraph · MCP", "TORUK MAKTO, NEXT"),
]


def journey():
    rnd = random.Random(5)
    W, H = 1200, 250
    xs = [130 + i * 235 for i in range(len(JOURNEY))]
    y = 132
    vine = (f"M40 {y} " + " ".join(f"Q{x - 60} {y - 26 if i % 2 else y + 26} {x} {y}" for i, x in enumerate(xs))
            + f" Q{xs[-1] + 60} {y - 26} 1160 {y}")
    cycle = 10
    nodes = []
    for i, (x, (year, title, place, saga)) in enumerate(zip(xs, JOURNEY)):
        delay = cycle * (x - 40) / 1120
        color = "#c084fc" if i == len(JOURNEY) - 1 else "#5ef2ff"
        nodes.append(f"""<g transform="translate({x} {y})">
      <circle r="16" fill="none" stroke="{color}" stroke-opacity=".35"/>
      <circle class="lit" r="22" fill="{color}" filter="url(#softglow)" style="animation-delay:{delay - cycle:.2f}s"/>
      <circle r="7" fill="#04122a" stroke="{color}" stroke-width="2"/>
      <circle r="3" fill="{color}" filter="url(#glow)"/>
    </g>
    <g text-anchor="middle" font-family="{FONT}">
      <text x="{x}" y="{y - 70}" font-size="10" letter-spacing="2.5" fill="#a78bfa">{saga}</text>
      <text x="{x}" y="{y - 46}" font-size="13" font-weight="700" letter-spacing="3" fill="{color}">{year}</text>
      <text x="{x}" y="{y + 48}" font-size="15" font-weight="700" fill="#e0f2fe">{title}</text>
      <text x="{x}" y="{y + 68}" font-size="12" fill="#94c9e0">{place}</text>
    </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="My journey from BSc Computer Science to Java Developer at Telusko">
  <title>My Journey</title>
  <defs>
    <linearGradient id="jbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#030b1a"/><stop offset="1" stop-color="#06182e"/></linearGradient>
    <linearGradient id="vineg" x1="0" x2="1"><stop offset="0" stop-color="#5ef2ff" stop-opacity=".2"/><stop offset=".8" stop-color="#5ef2ff" stop-opacity=".7"/><stop offset="1" stop-color="#c084fc" stop-opacity=".8"/></linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {DEFS_COMMON}
  </defs>
  <style>{COMMON_STYLE}
    .lit{{opacity:.15;animation:lit {cycle}s linear infinite;}}
    @keyframes lit{{0%{{opacity:.85}}12%{{opacity:.15}}100%{{opacity:.15}}}}
    .vdash{{stroke-dasharray:2 8;animation:vflow 3s linear infinite;}}
    @keyframes vflow{{to{{stroke-dashoffset:-40}}}}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#jbg)"/>
    <ellipse cx="600" cy="132" rx="520" ry="70" fill="#0e7490" opacity=".14" filter="url(#blur40)"/>
    {stars(rnd, 40, W, H)}
    <path d="{vine}" stroke="url(#vineg)" stroke-width="2.5" fill="none"/>
    <path class="vdash" d="{vine}" stroke="#bff7ff" stroke-width="1.5" fill="none" opacity=".6"/>
    <g>
      <circle r="10" fill="#5ef2ff" opacity=".35" filter="url(#softglow)"/><circle r="3.5" fill="#fff"/>
      <animateMotion dur="{cycle}s" repeatCount="indefinite" path="{vine}"/>
    </g>
    {"".join(nodes)}
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#5ef2ff" stroke-opacity=".18"/>
</svg>"""


for name, fn in [("header.svg", header), ("divider.svg", divider), ("footer.svg", footer),
                 ("hero.svg", hero), ("journey.svg", journey)]:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
    print("wrote", name)

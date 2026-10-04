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
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Shramik Masti — Java and Agentic AI Engineer">
  <title>Shramik Masti — Java &amp; Agentic AI Engineer</title>
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
        <text x="600" y="282" font-size="22" font-weight="600" letter-spacing="2" fill="#e0f2fe">Java Engineer  ·  Spring AI  ·  Agentic AI  ·  Cloud</text>
        <text x="600" y="314" font-size="15" letter-spacing="1.5" fill="#94c9e0">Building intelligent, production-grade systems with Spring Boot, LangChain &amp; LLM agents</text>
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
      <text x="600" y="118" font-size="14" letter-spacing="3" fill="#7dd3fc">I SEE YOU — THANKS FOR VISITING</text>
    </g>
  </g>
</svg>'''


for name, fn in [("header.svg", header), ("divider.svg", divider), ("footer.svg", footer)]:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
    print("wrote", name)

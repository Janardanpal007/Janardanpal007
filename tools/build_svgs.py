"""Build the profile's animated 3D-style SVGs.

Run from the repo root:  python -I tools/build_svgs.py
Artwork in assets/src is embedded as base64 so each SVG renders on its own
when GitHub shows it as an <img>. GitHub allows CSS keyframes inside SVG but
no scripts or CSS 3D, so depth is faked with extruded faces and shadows.
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SRC = ASSETS / "src"

BG = "#0B0F15"          # matches the artwork's backdrop; near GitHub dark #0d1117
NAVY = "#14264A"
ORANGE = "#FF8A24"
GOLD = "#FFD166"
BLUE = "#48BFFF"
WHITE = "#F4F7FF"
MUTED = "#B8C4D9"
SANS = "'Segoe UI', Arial, sans-serif"
MONO = "Consolas, 'Courier New', monospace"

POP = "cubic-bezier(.22,1,.36,1)"
REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"

# front, top, side faces of the extruded power bars
MARKETING_FACES = (ORANGE, GOLD, "#A84B12")
BUILDING_FACES = (BLUE, "#A1DFFF", "#236A99")

POWER_LEVELS = [
    ("Publisher Power", "Affiliate relations", 90, MARKETING_FACES),
    ("Campaign Charge", "Meta Ads", 85, MARKETING_FACES),
    ("Signal Focus", "Conversion tracking", 85, MARKETING_FACES),
    ("Search Momentum", "SEO", 80, MARKETING_FACES),
    ("Builder Training", "Kotlin", 60, BUILDING_FACES),
    ("Interface Practice", "Jetpack Compose", 55, BUILDING_FACES),
]

# (technique, app, description lines, icon file, accent)
TECHNIQUES = [
    ("Velocity Split", "FastDownloader",
     ["Segmented download manager for", "Windows, macOS and Linux."], "icon-1.jpg", ORANGE),
    ("Quiet Current", "Ghostream",
     ["Android browser with video and", "torrent downloads + ad blocker."], "icon-2.jpg", BLUE),
    ("Balance Field", "FinTrack",
     ["Private, offline personal", "finance app for Android."], "icon-3.jpg", GOLD),
    ("Clarity Pulse", "ProScan: Doc, PDF",
     ["On-device Android scanner", "and PDF toolkit."], "icon-4.jpg", BLUE),
    ("Command Spark", "Mobile Handler",
     ["One private Android app", "to handle your phone."], "icon-5.jpg", ORANGE),
]
CARD_W, CARD_H, CARD_DEPTH = 352, 266, 10
CARD_POSITIONS = [(48, 40), (424, 40), (800, 40), (236, 338), (612, 338)]


def embed(name: str) -> str:
    data = base64.b64encode((SRC / name).read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{data}"


def svg_open(width: int, height: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="t">\n'
        f"  <title id=\"t\">{title}</title>\n"
    )


# ---------------------------------------------------------------- header
HEADER_STYLE = f"""  <style>
    .win  {{ transform-origin: 860px 210px; animation: winIn .5s {POP} both; }}
    .hero {{ transform-origin: 860px 230px; animation: heroPop .75s {POP} .14s both; }}
    .shard {{ transform-box: fill-box; transform-origin: center; animation: shardOut .6s {POP} both; }}
    .copy {{ animation: copyIn .5s {POP} both; }}
    .aura {{ transform-origin: 740px 215px; animation: pulse 4s ease-in-out .8s infinite; }}
    .charge {{ transform-origin: 48px 0; animation: charge 1.2s {POP} .7s both; }}
    @keyframes winIn {{ from {{ opacity: 0; transform: translateY(18px) scale(.94); }} }}
    @keyframes heroPop {{ 0% {{ opacity: 0; transform: translateY(26px) scale(.92); }}
      65% {{ opacity: 1; transform: translateY(-3px) scale(1.035); }} 100% {{ transform: none; }} }}
    @keyframes shardOut {{ from {{ opacity: 0; transform: translate(40px, 10px) scale(.4) rotate(-30deg); }} }}
    @keyframes copyIn {{ from {{ opacity: 0; transform: translateY(6px); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: .25; transform: scale(1); }} 50% {{ opacity: .55; transform: scale(1.12); }} }}
    @keyframes charge {{ from {{ transform: scaleX(0); }} }}
    {REDUCED_MOTION}
  </style>"""

# (points, delay) glass shards that fly out over the text side
SHARDS = [
    ("528,92 552,80 548,104", 0.30), ("470,300 500,284 492,318", 0.38),
    ("560,330 578,322 572,344", 0.46), ("505,180 520,174 516,192", 0.54),
]


def header_defs() -> str:
    return f"""  <defs>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".22" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="edge"><rect x="200" width="1000" height="400" fill="url(#fade)"/></mask>
    <radialGradient id="glow">
      <stop offset="0" stop-color="{GOLD}" stop-opacity=".7"/>
      <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="gold" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
    <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{ORANGE}"/><stop offset=".6" stop-color="{GOLD}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DFF4FF" stop-opacity=".9"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".35"/></linearGradient>
  </defs>"""


def header_copy() -> str:
    lines = [
        (0.38, f'<text x="48" y="96" fill="{ORANGE}" font-size="16" font-weight="700" letter-spacing="6">JANARDAN PAL</text>'),
        (0.46, f'<text x="48" y="156" fill="{WHITE}" font-size="46" font-weight="800">Marketing Instinct.</text>'),
        (0.54, f'<text x="48" y="210" fill="url(#gold)" font-size="46" font-weight="800">Builder Energy.</text>'),
        (0.62, f'<text x="48" y="250" fill="{MUTED}" font-size="18">Marketer and indie app builder · Lucknow, India</text>'),
    ]
    out = [f'<g class="copy" style="animation-delay:{d}s">{t}</g>' for d, t in lines]
    out.append(f"""<g class="copy" style="animation-delay:.7s" font-family="{MONO}" font-size="13" fill="{MUTED}">
      <text x="48" y="304" letter-spacing="2">POWER LEVEL</text>
      <rect x="48" y="314" width="300" height="9" rx="4.5" fill="{NAVY}"/>
      <rect class="charge" x="48" y="314" width="300" height="9" rx="4.5" fill="url(#bar)"/>
      <text x="362" y="323" fill="{GOLD}">MAX</text>
    </g>""")
    return "\n    ".join(out)


def header_svg() -> str:
    shards = "\n    ".join(
        f'<polygon class="shard" points="{p}" fill="url(#glass)" style="animation-delay:{d}s"/>'
        for p, d in SHARDS
    )
    return f"""{svg_open(1200, 400, "Janardan Pal: Marketing Instinct. Builder Energy.")}  <desc>An original anime-style martial artist punches out of a glowing glass window showing the Lucknow skyline at dusk.</desc>
{HEADER_STYLE}
{header_defs()}
  <rect width="1200" height="400" rx="22" fill="{BG}"/>
  <g class="win">
    <ellipse class="aura" cx="740" cy="215" rx="130" ry="110" fill="url(#glow)"/>
    <g class="hero" mask="url(#edge)">
      <image x="200" width="1000" height="400" xlink:href="{embed('hero-3d.jpg')}"/>
    </g>
  </g>
  <g>
    {shards}
  </g>
  <g font-family="{SANS}">
    {header_copy()}
  </g>
</svg>
"""


# ---------------------------------------------------------------- power levels
def extruded_bar(x: float, y: float, w: float, h: float, depth: float, faces: tuple) -> str:
    front, top, side = faces
    return (
        f'<polygon points="{x},{y} {x + depth},{y - depth} {x + w + depth},{y - depth} {x + w},{y}" fill="{top}"/>'
        f'<polygon points="{x + w},{y} {x + w + depth},{y - depth} {x + w + depth},{y + h - depth} {x + w},{y + h}" fill="{side}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{front}"/>'
    )


def power_svg() -> str:
    row_h, top, width, depth = 52, 84, 1200, 8
    height = top + row_h * len(POWER_LEVELS) + 20
    bar_x, bar_w, bar_h = 520, 540, 16
    track = (NAVY, "#1E3563", "#0E1B36")
    rows = []
    for i, (label, skill, value, faces) in enumerate(POWER_LEVELS):
        y = top + i * row_h
        fill_w = bar_w * value / 100
        rows.append(f"""  <g transform="translate(0 {y})">
    <text x="48" y="22" fill="{WHITE}" font-family="{SANS}" font-size="18" font-weight="700">{skill}</text>
    <text x="300" y="22" fill="{faces[0]}" font-family="{MONO}" font-size="14" letter-spacing="1">{label.upper()}</text>
    <g opacity=".9">{extruded_bar(bar_x, 8, bar_w, bar_h, depth, track)}</g>
    <g class="fill" style="animation-delay:{0.2 + i * 0.07:.2f}s">{extruded_bar(bar_x, 8, fill_w, bar_h, depth, faces)}</g>
    <text x="{bar_x + bar_w + 26}" y="24" fill="{GOLD}" font-family="{MONO}" font-size="16" font-weight="700">{value}</text>
  </g>""")
    body = "\n".join(rows)
    return f"""{svg_open(width, height, "Power levels, self-rated: marketing skills in orange, building skills in blue")}  <style>
    .card {{ animation: rise .5s {POP} both; }}
    .fill {{ transform-box: fill-box; transform-origin: left center; animation: grow .45s {POP} both; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(16px); }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} }}
    {REDUCED_MOTION}
  </style>
  <g class="card">
    <rect x="10" y="14" width="{width - 10}" height="{height - 14}" rx="20" fill="#05080D"/>
    <rect width="{width - 10}" height="{height - 14}" rx="20" fill="{BG}" stroke="{NAVY}" stroke-width="2"/>
    <text x="48" y="46" fill="{MUTED}" font-family="{MONO}" font-size="14" letter-spacing="3">KI READING · SELF-RATED</text>
    <text x="{width - 58}" y="46" text-anchor="end" font-family="{MONO}" font-size="14"><tspan fill="{ORANGE}">■ MARKETING</tspan><tspan fill="{BLUE}" dx="18">■ BUILDING</tspan></text>
{body}
  </g>
</svg>
"""


# ---------------------------------------------------------------- techniques
def card_svg(i: int, x: int, y: int, technique: tuple) -> str:
    name, app, lines, icon, accent = technique
    d = CARD_DEPTH
    desc = "".join(
        f'<text x="{CARD_W / 2}" y="{214 + n * 22}" text-anchor="middle" fill="{MUTED}" font-size="15">{line}</text>'
        for n, line in enumerate(lines)
    )
    return f"""  <g transform="translate({x} {y})">
   <g class="pop" style="animation-delay:{0.1 + i * 0.1:.1f}s">
    <ellipse cx="{CARD_W / 2 + 8}" cy="{CARD_H + 16}" rx="{CARD_W / 2 - 20}" ry="10" fill="#000" opacity=".55"/>
    <rect x="{d}" y="{d}" width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0A1530" stroke="#1B3A73" stroke-width="1.5"/>
    <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="url(#face)" stroke="{NAVY}" stroke-width="2"/>
    <rect x="18" y="1" width="{CARD_W - 36}" height="3" rx="1.5" fill="{accent}" opacity=".9"/>
    <image x="{CARD_W / 2 - 62}" y="18" width="124" height="124" mask="url(#soft)" xlink:href="{embed(icon)}"/>
    <text x="{CARD_W / 2}" y="166" text-anchor="middle" fill="{accent}" font-family="{MONO}" font-size="13" letter-spacing="3">{name.upper()}</text>
    <text x="{CARD_W / 2}" y="192" text-anchor="middle" fill="{WHITE}" font-size="21" font-weight="800">{app}</text>
    {desc}
   </g>
  </g>"""


def techniques_svg() -> str:
    width, height = 1200, 650
    cards = "\n".join(
        card_svg(i, x, y, t) for i, ((x, y), t) in enumerate(zip(CARD_POSITIONS, TECHNIQUES))
    )
    return f"""{svg_open(width, height, "Techniques: five apps by Janardan Pal shown as 3D cards")}  <style>
    .pop {{ animation: pop .55s {POP} both; }}
    @keyframes pop {{ 0% {{ opacity: 0; transform: translateY(22px) scale(.94); }}
      65% {{ opacity: 1; transform: translateY(-2px) scale(1.025); }} 100% {{ transform: none; }} }}
    {REDUCED_MOTION}
  </style>
  <defs>
    <linearGradient id="face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121C33"/><stop offset="1" stop-color="{BG}"/></linearGradient>
    <radialGradient id="softg"><stop offset=".62" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="soft" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#softg)"/></mask>
  </defs>
  <g font-family="{SANS}">
{cards}
  </g>
</svg>
"""


# ---------------------------------------------------------------- divider
def divider_svg() -> str:
    return f"""{svg_open(1200, 48, "Section divider")}  <rect x="48" y="23" width="520" height="2" rx="1" fill="{NAVY}"/>
  <rect x="632" y="23" width="520" height="2" rx="1" fill="{NAVY}"/>
  <polygon points="606,6 590,28 600,28 594,44 614,20 603,20 610,6" fill="#236A99" transform="translate(4 3)"/>
  <polygon points="606,6 590,28 600,28 594,44 614,20 603,20 610,6" fill="{GOLD}"/>
</svg>
"""


def main() -> None:
    outputs = {
        "header.svg": header_svg(),
        "power-levels.svg": power_svg(),
        "techniques.svg": techniques_svg(),
        "divider.svg": divider_svg(),
    }
    for name, content in outputs.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"wrote assets/{name} ({len(content) // 1024} KB)")


if __name__ == "__main__":
    main()

"""Generate the hand-drawn SVG thumbnails for the homepage publication list.

Writes one SVG snippet per paper into assets/img/art/*.svg. The snippets are
inlined into index.html (between <!--art:NAME--> markers) by inline_art.py so
they can use the page's CSS variables (light/dark) and hover animations.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "art"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 320, 220


def svg(label, body):
    return (
        f'<svg class="art" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
        f'<rect class="art-bg" width="{W}" height="{H}"/>{body}</svg>'
    )


# ---------------------------------------------------------------- SLP
def slp():
    b = []
    b.append('<g class="art-badge" transform="translate(228 17)"><rect width="76" height="25" rx="12.5"/>'
             '<text x="38" y="17">12 / 12 ↑</text></g>')
    blocks = [("v", 20, "V", "1", ""), ("t", 92, "T", "1", ""),
              ("v", 164, "V", "2", " strong a-pop"), ("t", 236, "T", "2", " strong a-pop")]
    for i, (k, x, letter, sub, extra) in enumerate(blocks):
        d = f' style="--d:{0.08 + 0.14 * (i - 2):.2f}s"' if "a-pop" in extra else ""
        b.append(f'<g class="blk b-{k}{extra}"{d}><rect x="{x}" y="96" width="62" height="46" rx="11"/>'
                 f'<text x="{x + 31}" y="126">{letter}<tspan dy="4">{sub}</tspan></text></g>')
    # V2 -> T1 : question-guided look (above)
    b.append('<path class="arc arc-g a-draw" d="M195 96 C195 58 123 58 123 96"/>')
    b.append('<path class="arc arc-g" d="M117.5 88 L123 96 L128.5 88"/>')
    b.append('<text class="art-note n-g" x="159" y="56">question-guided look</text>')
    # T2 -> V2 : reads the scratchpad (below)
    b.append('<path class="arc arc-a a-draw" style="--d:.45s" d="M267 142 C267 180 195 180 195 142"/>')
    b.append('<path class="arc arc-a" d="M189.5 150 L195 142 L200.5 150"/>')
    b.append('<text class="art-note n-a" x="231" y="200">reads the scratchpad</text>')
    b.append('<text class="art-note n-f" x="87" y="168">standard prompt</text>')
    b.append('<path class="art-brace" d="M22 152 V156 H152 V152"/>')
    return svg("Second-Look Prompting: the image and question are replayed; the second image attends to the question and the second question reads it.", "".join(b))


# ---------------------------------------------------------------- MLS-Bench
def mls():
    b = []
    xs, ys = [26, 95, 164, 233], [20, 67, 114]
    tw, th = 60, 38
    # (human, agent) bar widths out of 42 — agents mostly short of human SOTA
    bars = [(42, 29), (40, 33), (42, 22), (38, 31),
            (42, 35), (41, 26), (0, 0), (39, 21),
            (42, 28), (36, 39), (42, 25), (38, 30)]
    k = 0
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            hw, aw = bars[k]
            if (r, c) == (1, 2):
                b.append(f'<g class="tile tile-hl"><rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8"/>'
                         f'<text x="{x + tw / 2}" y="{y + 24}">ML Sys</text></g>')
            else:
                b.append(f'<g class="tile"><rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8"/>'
                         f'<rect class="bar-h" x="{x + 9}" y="{y + 11}" width="{hw}" height="6" rx="3"/>'
                         f'<rect class="bar-a a-grow" style="--d:{0.04 * k:.2f}s" x="{x + 9}" y="{y + 21}" width="{aw}" height="6" rx="3"/></g>')
            k += 1
    b.append('<rect class="bar-h" x="76" y="173" width="14" height="6" rx="3"/>'
             '<text class="art-note n-f" x="96" y="179.5" text-anchor="start">human SOTA</text>'
             '<rect class="bar-a" x="186" y="173" width="14" height="6" rx="3"/>'
             '<text class="art-note n-f" x="206" y="179.5" text-anchor="start">AI agent</text>')
    b.append('<text class="art-title" x="160" y="206" text-anchor="middle">140 research tasks · 12 domains</text>')
    return svg("MLS-Bench: 140 research tasks across 12 domains; AI agents mostly fall short of human state-of-the-art methods.", "".join(b))


# ---------------------------------------------------------------- DPA
def dpa():
    b = []

    def row(y, label, mid, tok_cls, ok, label_cls):
        g = [f'<text class="art-note {label_cls}" x="20" y="{y - 10}" text-anchor="start">{label}</text>']
        # image glyph
        g.append(f'<g class="img-glyph"><rect x="20" y="{y}" width="32" height="34" rx="7"/>'
                 f'<path d="M25 {y + 27} L32 {y + 17} L37 {y + 23} L40 {y + 20} L47 {y + 27} Z"/>'
                 f'<circle cx="41" cy="{y + 10}" r="2.6"/></g>')
        for x0, x1 in [(52, 60), (108, 116), (182, 190)]:
            g.append(f'<path class="arrow" d="M{x0 + 1} {y + 17} H{x1 - 1} M{x1 - 4} {y + 14} L{x1 - 1} {y + 17} L{x1 - 4} {y + 20}"/>')
        g.append(f'<g class="blk b-n"><rect x="60" y="{y}" width="48" height="34" rx="8"/><text class="sm" x="84" y="{y + 21.5}">ViT</text></g>')
        g.append(f'<g class="blk {mid[1]}"><rect x="116" y="{y}" width="66" height="34" rx="8"/><text class="sm" x="149" y="{y + 21.5}">{mid[0]}</text></g>')
        for i in range(3):
            g.append(f'<rect class="tok {tok_cls} a-flow" style="--d:{0.1 * i:.1f}s" x="{192 + 12 * i}" y="{y + 12.5}" width="9" height="9" rx="2"/>')
        g.append(f'<g class="blk b-t"><rect x="230" y="{y}" width="70" height="34" rx="8"/><text x="265" y="{y + 22}">LLM</text></g>')
        if ok:
            g.append(f'<path class="mark-ok" d="M199 {y - 7} L204 {y - 2} L213 {y - 12}"/>')
        else:
            g.append(f'<path class="mark-bad" d="M201 {y - 11} L211 {y - 1} M211 {y - 11} L201 {y - 1}"/>')
        return "".join(g)

    b.append(row(40, "LLaVA-style", ("Projector", "b-n"), "tok-v", False, "n-f"))
    b.append(row(130, "Deep Pre-Alignment", ("Small VLM", "b-v"), "tok-t", True, "n-v"))
    b.append('<text class="art-note n-f" x="160" y="204">visual tokens arrive in the text space</text>')
    return svg("Deep Pre-Alignment: a small VLM replaces the projector, so visual tokens reach the LLM already aligned with its text space.", "".join(b))


# ---------------------------------------------------------------- Survey
def survey():
    b = []
    pitch, cell = 10, 8

    def grid(gx, gy, fill_fn, label, hl=False):
        g = []
        for i in range(6):
            for j in range(6):
                cls = fill_fn(i, j)
                g.append(f'<rect class="{cls}" x="{gx + pitch * j}" y="{gy + pitch * i}" width="{cell}" height="{cell}" rx="1.5"/>')
        lab_cls = "art-note n-v strong-lbl" if hl else "art-note n-f"
        g.append(f'<text class="{lab_cls}" x="{gx + 29}" y="{gy + 74}">{label}</text>')
        return "".join(g)

    # Hardware-efficient: dense matrix, computed tile by tile
    b.append(grid(56, 18, lambda i, j: "c-n", "Hardware"))
    for bi in range(3):
        for bj in range(3):
            b.append(f'<rect class="tile-outline" x="{56 + 20 * bj - 1}" y="{18 + 20 * bi - 1}" width="20" height="20" rx="3"/>')
    b.append('<rect class="tile-cur a-tile" x="55" y="17" width="20" height="20" rx="3"/>')
    # Sparse: causal sliding window + attention sink
    b.append(grid(206, 18, lambda i, j: "c-v" if (j <= i and (i - j <= 1 or j == 0)) else "c-empty", "Sparse", hl=True))
    # Compact: compressed KV — only a few columns stored
    b.append(grid(56, 116, lambda i, j: "c-t" if j < 2 else "c-empty", "Compact"))
    # Linear: N×N replaced by a small d×d state
    b.append(grid(206, 116, lambda i, j: "c-t" if (i < 3 and j < 3) else "c-empty", "Linear"))
    b.append('<path class="divider" d="M160 22 V186 M36 108 H284"/>')
    return svg("Efficient attention taxonomy: hardware-efficient, sparse, compact and linear attention.", "".join(b))


for name, fn in {"second-look": slp, "mls-bench": mls, "deep-pre-alignment": dpa, "attention-survey": survey}.items():
    (OUT / f"{name}.svg").write_text(fn() + "\n", encoding="utf-8")
    print("wrote", OUT / f"{name}.svg")

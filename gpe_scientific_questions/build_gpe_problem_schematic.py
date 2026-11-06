"""Slide figure: classes of conventional gel/quasi-solid electrolytes -> common root problem -> science question.
Same primitives / palette as build_mechanism_schematic.py (single axes, absolute coordinates). English labels
(no CJK font in sandbox); Chinese captions go on the slide itself. Run from gpe_scientific_questions/.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, FancyArrowPatch
from scipy.ndimage import gaussian_filter1d

C = dict(li="#E57373", li_e="#B71C1C", pf6="#F0A868", pf6_e="#B9742B", dmtfa="#5DA9E9", dmtfa_e="#1F5F9F",
         ether="#8D5A2B", ester="#2E7D6B", fluoro="#6D6D9E", poly_o="#C62828", grey="#3C4858", red="#C0392B",
         navy="#1F2A44", bg="#F3F6FA", bg2="#FBF7EE")

W, H = 12.4, 6.6
fig = plt.figure(figsize=(W, H), dpi=250)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

def dmtfa(x, y, ang, s=1.0, z=4, alpha=1):
    ax.add_patch(Ellipse((x, y), 0.30 * s, 0.15 * s, angle=ang, fc=C["dmtfa"], ec=C["dmtfa_e"], lw=0.7, zorder=z, alpha=alpha))
def anion(x, y, s=1.0, z=5):
    ax.add_patch(Circle((x, y), 0.075 * s, fc=C["pf6"], ec=C["pf6_e"], lw=0.7, zorder=z))
    ax.text(x, y, "P", ha="center", va="center", fontsize=5 * s, color="white", fontweight="bold", zorder=z + 1)
def li(x, y, s=1.0, z=6):
    ax.add_patch(Circle((x, y), 0.065 * s, fc=C["li"], ec=C["li_e"], lw=0.7, zorder=z))
    ax.text(x, y, "Li⁺", ha="center", va="center", fontsize=4.2 * s, color="white", fontweight="bold", zorder=z + 1)
def polygroup(x, y, s=1.0, label="O", color=C["poly_o"], z=5):
    ax.add_patch(Circle((x, y), 0.07 * s, fc="white", ec=color, lw=1.2, zorder=z))
    ax.text(x, y, label, ha="center", va="center", fontsize=4.6 * s, color=color, fontweight="bold", zorder=z + 1)
def chain(pts, color, lw=1.8, z=3, smooth=5):
    pts = np.asarray(pts); t = np.linspace(0, 1, len(pts)); tt = np.linspace(0, 1, 200)
    xs = gaussian_filter1d(np.interp(tt, t, pts[:, 0]), smooth); ys = gaussian_filter1d(np.interp(tt, t, pts[:, 1]), smooth)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=z); return xs, ys
def arrow(p, q, color=C["grey"], lw=1.3, ms=10, z=8):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, zorder=z))
def panel(x, y, w, h, color, bg=C["bg"]):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=bg, ec=color, lw=1.0, zorder=1))
def txt(x, y, s, **k):
    k.setdefault("ha", "center"); k.setdefault("va", "center"); k.setdefault("color", C["grey"]); k.setdefault("zorder", 12)
    ax.text(x, y, s, **k)

def solvate(x, y, s=1.0, rot=0, n_solv=3, poly=None, poly_color=C["poly_o"], poly_label="O"):
    """Li+ with n_solv DMTFA + 1 anion; if poly, one site is taken by a polymer group (label)."""
    R = 0.34 * s
    ax.add_patch(Circle((x, y), R, fc="white", ec="#8A8F98", lw=0.6, ls=(0, (2, 2)), alpha=0.95, zorder=2))
    slots = 4 if poly is None else 5
    angs = np.linspace(0, 360, slots, endpoint=False) + rot
    k = 0
    for i, a in enumerate(angs):
        r = np.deg2rad(a); px, py = x + 0.21 * s * np.cos(r), y + 0.21 * s * np.sin(r)
        if i == slots - 1: anion(px, py, s)
        elif poly is not None and i == 0: polygroup(px, py, s, poly_label, poly_color)
        else: dmtfa(px, py, a + 90, s)
    li(x, y, s)

# ================= header
txt(W / 2, H - 0.32, "Conventional gel / quasi-solid electrolytes share one root problem", fontsize=13, fontweight="bold", color=C["navy"])

# ================= row 1: three classes
classes = [
    ("Ether-based", "PEO / PEGDA / PDOL", C["ether"], "O", "C–O–C strongly coordinates Li⁺\noxidation limit ≈ 4.0–4.3 V"),
    ("Ester / nitrile-based", "PMMA / PAN / PETEA", C["ester"], "O", "C=O / C≡N coordinate Li⁺\nion pairing ↑, σ ↓"),
    ("Fluoropolymer-based", "PVDF-HFP", C["fluoro"], "F", "weak coordination, but swelling-\nbased uptake: leakage, soft, interface"),
]
x0, pw, gap, py, ph = 0.45, 3.65, 0.25, 3.35, 2.45
for i, (name, ex, col, lab, issue) in enumerate(classes):
    x = x0 + i * (pw + gap); panel(x, py, pw, ph, col)
    txt(x + 0.15, py + ph - 0.22, name, ha="left", fontsize=10.5, fontweight="bold", color=col)
    txt(x + 0.15, py + ph - 0.47, ex, ha="left", fontsize=8, color=C["grey"])
    # polymer chain across panel with pendant groups, one of which enters the Li+ shell
    xs, ys = chain([(x + 0.25, py + 0.55), (x + 0.9, py + 0.85), (x + 1.5, py + 0.5), (x + 2.1, py + 0.9), (x + 2.7, py + 0.55), (x + 3.4, py + 0.8)], col, lw=2.2)
    for j in range(20, 200, 45):
        polygroup(xs[j], ys[j] + 0.13, 0.9, lab, col)
    # solvate sitting on the chain: polymer group replaces a DMTFA
    cx, cy = x + 1.95, py + 1.45
    if lab == "F":
        solvate(cx, cy, 1.0, rot=15)
        for dx, dy, a in [(0.75, 0.05, 30), (0.95, -0.25, -20), (0.7, -0.4, 60)]:
            dmtfa(cx + dx, cy + dy, a, 0.9, alpha=0.5)
        txt(cx + 1.0, cy + 0.42, "free liquid\n(leakage)", fontsize=6.3, color="#6B7280")
    else:
        solvate(cx, cy, 1.0, rot=250, poly=True, poly_color=col, poly_label=lab)
        dmtfa(cx + 0.62, cy + 0.22, 20, 1.0, alpha=0.55); arrow((cx + 0.36, cy + 0.12), (cx + 0.5, cy + 0.2), color="#8A8F98", lw=0.8, ms=7)
        txt(cx + 0.95, cy + 0.42, "displaced\nsolvent", fontsize=6.3, color="#6B7280")
    txt(x + pw / 2, py + 0.22, issue, fontsize=7.4, color=C["grey"])

# ================= row 2: common root (liquid solvate -> gel solvate) + costs
y2, h2 = 1.25, 1.85
panel(0.45, y2, 7.3, h2, C["red"], bg=C["bg2"])
txt(0.6, y2 + h2 - 0.2, "Common root: polar groups of the network compete with the solvent for Li⁺ → the solvation structure is rebuilt", ha="left", fontsize=8.3, fontweight="bold", color=C["red"])
solvate(1.45, y2 + 0.72, 1.15, rot=15)
txt(1.45, y2 + 0.12, "liquid electrolyte\nLi⁺(solvent)ₙ · anion", fontsize=7, color=C["grey"])
arrow((2.15, y2 + 0.72), (2.85, y2 + 0.72), color=C["red"], lw=1.8, ms=14)
txt(2.5, y2 + 0.95, "gelation", fontsize=7.5, color=C["red"])
solvate(3.55, y2 + 0.72, 1.15, rot=15, poly=True)
chain([(2.95, y2 + 0.25), (3.3, y2 + 0.4), (3.75, y2 + 0.3), (4.15, y2 + 0.45)], C["ether"], lw=2.0)
txt(3.55, y2 + 0.12, "gel electrolyte\npolymer group in the shell", fontsize=7, color=C["grey"])
costs = ["σ drops 1–2 orders of magnitude", "slower desolvation, higher R_ct", "anion pairing / interphase chemistry changed", "gel performance < its own liquid electrolyte"]
for k, s in enumerate(costs):
    txt(4.55, y2 + h2 - 0.55 - 0.3 * k, "•  " + s, ha="left", fontsize=8, color=C["grey"])
txt(4.55, y2 + 0.22, "…usually presented as “regulation”; rarely tested:\nhow much did gelation actually change?", ha="left", fontsize=7.0, color="#6B7280", style="italic")

# right: what liquid vs gel typically looks like (conceptual bars)
panel(8.0, y2, 3.95, h2, C["grey"])
txt(8.15, y2 + h2 - 0.2, "Typical penalty vs. the parent liquid", ha="left", fontsize=9, fontweight="bold", color=C["navy"])
items = [("σ (25 °C)", 1.0, 0.2), ("t⁺ / kinetics", 1.0, 0.6), ("4.5 V retention", 1.0, 0.7)]
for k, (lab, lq, gl) in enumerate(items):
    yy = y2 + h2 - 0.55 - 0.38 * k
    txt(8.15, yy, lab, ha="left", fontsize=7.5)
    ax.add_patch(FancyBboxPatch((9.35, yy - 0.07), 2.3 * lq, 0.13, boxstyle="square,pad=0", fc="#1F1F1F", ec="none", zorder=5))
    ax.add_patch(FancyBboxPatch((9.35, yy - 0.22), 2.3 * gl, 0.13, boxstyle="square,pad=0", fc=C["ether"], ec="none", zorder=5))
txt(8.15, y2 + 0.17, "■ liquid   ■ conventional gel   (schematic, not to scale)", ha="left", fontsize=6.5, color="#6B7280")

# ================= bottom: science question
ax.add_patch(FancyBboxPatch((0.45, 0.22), 11.5, 0.78, boxstyle="round,pad=0.02,rounding_size=0.12", fc=C["navy"], ec="none", zorder=1))
txt(0.7, 0.78, "Science question", ha="left", fontsize=8.5, color="#C9D3E6", fontweight="bold")
txt(0.7, 0.47, "Can a polymer network solidify a 4.5 V liquid electrolyte without entering the Li⁺ solvation shell — quasi-solid at minimal transport cost?",
    ha="left", fontsize=9.3, color="white", fontweight="bold")

fig.savefig("figures/GPE_Common_Problem_Schematic.png", facecolor="white")
fig.savefig("figures/GPE_Common_Problem_Schematic.svg", facecolor="white")
print("saved")

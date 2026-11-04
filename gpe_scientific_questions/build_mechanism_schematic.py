"""Journal-style mechanism schematic for the MBA in-situ gel electrolyte (single-axes, absolute coordinates).
Top row: molecular level (before / after polymerization). Bottom row: cell level (ether-gel control / MBA gel).
Claims follow project boundaries: solvation preserved (7Li/Raman/sigma); N-H...anion = design expectation.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch
from scipy.ndimage import gaussian_filter1d

C = dict(li="#E57373", li_e="#B71C1C", pf6="#F0A868", pf6_e="#B9742B", dfob="#8FBF7F", dfob_e="#3E7A3A",
         dmtfa="#5DA9E9", dmtfa_e="#1F5F9F", tte="#A7D8D8", tte_e="#4A9598", mba="#B39DDB", mba_e="#5E35B1",
         pmba="#1F2A44", pegda="#8D5A2B", hb="#C62828", bg_l="#F3F6FA", bg_r="#F7F4EC",
         anode="#8E9AA6", cathode="#3F4460", sei_org="#D9C7B8", sei_inorg="#F2C14E", lif="#BFE0F5",
         red="#C0392B", teal="#0E8A7A", grey="#3C4858")

W, H = 12.4, 7.0
fig = plt.figure(figsize=(W, H), dpi=250)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# ---------------------------------------------------------------- primitives (absolute sizes, inches ~ data units)
def dmtfa(x, y, ang, s=1.0, z=4):
    ax.add_patch(Ellipse((x, y), 0.30 * s, 0.15 * s, angle=ang, fc=C["dmtfa"], ec=C["dmtfa_e"], lw=0.7, zorder=z))

def tte(x, y, ang, s=1.0, z=3):
    ax.add_patch(Ellipse((x, y), 0.28 * s, 0.10 * s, angle=ang, fc=C["tte"], ec=C["tte_e"], lw=0.6, zorder=z))

def anion(x, y, kind="pf6", s=1.0, z=5):
    ax.add_patch(Circle((x, y), 0.075 * s, fc=C[kind], ec=C[kind + "_e"], lw=0.7, zorder=z))
    ax.text(x, y, "P" if kind == "pf6" else "B", ha="center", va="center", fontsize=5 * s, color="white",
            fontweight="bold", zorder=z + 1)

def li(x, y, s=1.0, z=6):
    ax.add_patch(Circle((x, y), 0.065 * s, fc=C["li"], ec=C["li_e"], lw=0.7, zorder=z))
    ax.text(x, y, "Li⁺", ha="center", va="center", fontsize=4.2 * s, color="white", fontweight="bold", zorder=z + 1)

def solvate(x, y, s=1.0, kind="pf6", rot=0, n=3):
    """Li+ + n DMTFA + 1 contact anion inside a dashed shell."""
    R = 0.33 * s
    ax.add_patch(Circle((x, y), R, fc="white", ec="#8A8F98", lw=0.6, ls=(0, (2, 2)), alpha=0.9, zorder=2))
    angs = np.linspace(0, 360, n + 1, endpoint=False)[:n] + rot
    for a in angs:
        r = np.deg2rad(a); dmtfa(x + 0.21 * s * np.cos(r), y + 0.21 * s * np.sin(r), a + 90, s)
    r = np.deg2rad(angs[-1] + 360 / (n + 1)); anion(x + 0.20 * s * np.cos(r), y + 0.20 * s * np.sin(r), kind, s)
    li(x, y, s)

def mba(x, y, s=1.0, ang=0):
    """MBA monomer: two acrylamide ends (dots) bridged by CH2 (V)."""
    t = np.deg2rad(ang); c, sn = np.cos(t), np.sin(t)
    P = np.array([(-0.09, 0.04), (0, -0.03), (0.09, 0.04)]) * s
    P = P @ np.array([[c, -sn], [sn, c]]).T + (x, y)
    ax.plot(P[:, 0], P[:, 1], color=C["mba_e"], lw=1.4, zorder=4)
    ax.plot(P[[0, 2], 0], P[[0, 2], 1], "o", ms=2.6, mfc=C["mba"], mec=C["mba_e"], mew=0.6, zorder=5)

def chain(pts, color, lw=1.8, marks=None, nh=False, z=3, smooth=5):
    pts = np.asarray(pts); t = np.linspace(0, 1, len(pts)); tt = np.linspace(0, 1, 240)
    xs = gaussian_filter1d(np.interp(tt, t, pts[:, 0]), smooth); ys = gaussian_filter1d(np.interp(tt, t, pts[:, 1]), smooth)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=z)
    if marks:
        for i in range(18, 230, marks):
            ax.plot(xs[i], ys[i], "o", ms=2.8, mfc="white", mec=color, mew=0.8, zorder=z + 1)
            if nh: ax.text(xs[i], ys[i] + 0.055, "N–H", fontsize=4.2, ha="center", color=color, zorder=z + 1)
    return xs, ys

def arrow(p, q, color=C["grey"], lw=1.2, style="-|>", ls="-", ms=9, z=8):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, color=color, lw=lw, mutation_scale=ms, ls=ls, zorder=z))

def panel(x, y, w, h, title, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", fc="white", ec=color,
                                lw=1.0, ls=(0, (4, 2)), zorder=0))
    ax.text(x + 0.15, y + h - 0.12, title, fontsize=8.5, fontweight="bold", color=color, va="top", zorder=9)

def txt(x, y, s, **k):
    kk = dict(fontsize=6.3, color="#333", ha="center", va="center", zorder=9); kk.update(k); ax.text(x, y, s, **kk)

# ---------------------------------------------------------------- layout
PW, PH = 4.7, 3.05
X1, X2 = 0.25, 6.05
YT, YB = 3.7, 0.3

# ============================ TOP-LEFT : before polymerization
x0, y0 = X1, YT
panel(x0, y0, PW, PH, "Before polymerization: liquid precursor", C["grey"])
ax.add_patch(Rectangle((x0 + 0.15, y0 + 0.45), PW - 0.3, PH - 0.85, fc=C["bg_l"], ec="none", zorder=0.5))
for (x, y, k, r) in [(1.35, 5.75, "pf6", 15), (2.75, 5.95, "dfob", 60), (3.95, 5.55, "pf6", 100),
                     (1.75, 4.75, "pf6", 40), (3.3, 4.75, "pf6", 80)]:
    solvate(x, y, 1.0, k, r)
for (x, y, a) in [(0.75, 5.1, 30), (4.55, 6.2, -20), (4.6, 4.6, 60), (2.2, 6.4, 10), (0.7, 6.3, -40),
                  (2.5, 5.35, -30), (4.35, 5.05, 35), (1.0, 4.45, -60), (3.9, 6.45, 25)]:
    tte(x, y, a, 1.0)
for (x, y, a) in [(2.2, 5.5, 10), (4.3, 6.05, -30), (0.95, 4.85, 35), (2.6, 4.45, -15), (4.4, 5.3, 60)]:
    mba(x, y, 1.0, a)
txt(x0 + PW / 2, y0 + 0.27, "1.0 M LiPF₆ + 0.2 M LiDFOB in DMTFA : TTE (1 : 1, v/v)  +  MBA", fontweight="bold")
txt(x0 + PW / 2, y0 + 0.1, "Li⁺(DMTFA)ₙ·anion solvates (CIP-rich, weakly solvating) · TTE stays outside the shell",
    fontsize=5.6, color="#666")

# ============================ TOP-RIGHT : after polymerization
x0, y0 = X2, YT
panel(x0, y0, PW, PH, "After polymerization: amide network locks the liquid", C["teal"])
ax.add_patch(Rectangle((x0 + 0.15, y0 + 0.45), PW - 0.3, PH - 0.85, fc=C["bg_r"], ec="none", zorder=0.5))
xa, ya = chain([(6.25, 6.3), (7.0, 6.0), (7.8, 6.35), (8.7, 5.95), (9.6, 6.3), (10.6, 6.05)], C["pmba"], marks=38, nh=True)
xb, yb = chain([(6.25, 4.85), (7.1, 5.2), (8.0, 4.75), (8.9, 5.15), (9.8, 4.8), (10.6, 5.1)], C["pmba"], marks=38, nh=True)
chain([(7.45, 6.2), (7.6, 5.7), (7.45, 5.25), (7.55, 4.95)], C["pmba"], lw=1.3)
chain([(9.25, 6.1), (9.1, 5.6), (9.3, 5.2), (9.15, 4.95)], C["pmba"], lw=1.3)
for (x, y, k, r) in [(6.95, 5.55, "pf6", 15), (8.35, 5.6, "dfob", 60), (9.95, 5.5, "pf6", 100)]:
    solvate(x, y, 1.0, k, r)
for (x, y, a) in [(6.55, 6.55, 20), (8.4, 6.6, -25), (10.3, 6.6, 35), (6.6, 4.55, -30), (8.2, 4.5, 25),
                  (10.2, 4.55, -10), (7.95, 6.1, 50), (9.4, 6.05, -45)]:
    tte(x, y, a, 1.0)
# N-H ... anion (design expectation)
arrow((xa[94], ya[94]), (7.2, 5.72), color=C["hb"], lw=0.9, style="-", ls=(0, (2, 2)))
arrow((xb[170], yb[170]), (10.12, 5.3), color=C["hb"], lw=0.9, style="-", ls=(0, (2, 2)))
txt(7.55, 5.95, "N–H···anion\n(design, to verify)", fontsize=5.2, color=C["hb"], ha="left")
arrow((6.5, 4.33), (10.45, 4.33), color=C["li_e"], lw=1.5, ms=11)
txt(8.45, 4.45, "Li⁺ transport through retained liquid solvates", fontsize=5.6, color=C["li_e"])
txt(x0 + PW / 2, y0 + 0.27, "Solvation shell unchanged", fontweight="bold", color=C["teal"], fontsize=7)
txt(x0 + PW / 2, y0 + 0.1, "⁷Li Δδ ≈ 0.02 ppm vs liquid · DMTFA δs(CF₃) 760 cm⁻¹ unchanged · σ ≈ liquid",
    fontsize=5.6, color=C["teal"])

# ============================ BOTTOM cells
def cell(x0, y0, title, color, bg, sei_c, cei_c, sei_w, cei_w, bad):
    panel(x0, y0, PW, PH, title, color)
    xl, xr, yb_, yt_ = x0 + 0.15, x0 + PW - 0.15, y0 + 0.4, y0 + PH - 0.45
    ax.add_patch(Rectangle((xl, yb_), 0.32, yt_ - yb_, fc=C["anode"], ec="none", zorder=1))
    ax.text(xl + 0.16, (yb_ + yt_) / 2, "Li metal", rotation=90, ha="center", va="center", fontsize=6.5, color="white", zorder=2)
    ax.add_patch(Rectangle((xr - 0.32, yb_), 0.32, yt_ - yb_, fc=C["cathode"], ec="none", zorder=1))
    ax.text(xr - 0.16, (yb_ + yt_) / 2, "NCM811 · 4.5 V", rotation=90, ha="center", va="center", fontsize=6.5, color="white", zorder=2)
    ax.add_patch(Rectangle((xl + 0.32, yb_), sei_w, yt_ - yb_, fc=sei_c, ec="none", zorder=1))
    ax.add_patch(Rectangle((xr - 0.32 - cei_w, yb_), cei_w, yt_ - yb_, fc=cei_c, ec="none", zorder=1))
    ex0, ex1 = xl + 0.32 + sei_w, xr - 0.32 - cei_w
    ax.add_patch(Rectangle((ex0, yb_), ex1 - ex0, yt_ - yb_, fc=bg, ec="none", zorder=0.5))
    # cathode particles
    for yy in (yb_ + 0.55, (yb_ + yt_) / 2, yt_ - 0.55):
        ax.add_patch(Circle((ex1 - 0.14, yy), 0.16, fc="#6E7390", ec="#2F3250", lw=0.6, zorder=3))
        if bad:
            ax.plot([ex1 - 0.26, ex1 - 0.04], [yy - 0.08, yy + 0.1], color="#111", lw=0.8, zorder=4)
            ax.plot([ex1 - 0.2, ex1 - 0.1], [yy + 0.1, yy - 0.12], color="#111", lw=0.6, zorder=4)
    if bad:  # dendrites + Li debris
        for yy in (yb_ + 0.45, (yb_ + yt_) / 2, yt_ - 0.5):
            ax.add_patch(Polygon([(ex0 - sei_w, yy - 0.16), (ex0 + 0.45, yy + 0.03), (ex0 - sei_w, yy + 0.18)],
                                 fc="#B0B8C1", ec="#5F6B78", lw=0.6, zorder=3))
    else:  # smooth deposit
        ax.add_patch(Rectangle((xl + 0.32, yb_), 0.05, yt_ - yb_, fc="#C7CDD4", ec="none", zorder=2))
    return ex0, ex1, yb_, yt_

# ---- bottom-left : ether-type gel control
x0, y0 = X1, YB
ex0, ex1, yb_, yt_ = cell(x0, y0, "Conventional ether-type gel (PEGDA control)", C["red"], "#EEF2F7",
                          C["sei_org"], C["sei_org"], 0.26, 0.26, True)
for (yy, ph) in [(yt_ - 0.5, 0), (yb_ + 1.1, 1.6), (yb_ + 0.45, 3.1)]:
    xs = np.linspace(ex0 + 0.5, ex1 - 0.35, 150); ys = yy + 0.12 * np.sin(5 * xs + ph)
    ax.plot(xs, ys, color=C["pegda"], lw=1.8, zorder=3)
    for xx in np.linspace(ex0 + 0.7, ex1 - 0.55, 5):
        ax.plot(xx, yy + 0.12 * np.sin(5 * xx + ph), "o", ms=2.8, mfc="white", mec=C["pegda"], mew=0.8, zorder=4)
# Li+ captured by ether O (dashed brown shell), DMTFA displaced, anions free
for (x, y) in [(ex0 + 1.05, yt_ - 0.62), (ex0 + 2.1, yb_ + 1.22), (ex0 + 1.4, yb_ + 0.4)]:
    li(x, y, 1.0); ax.add_patch(Circle((x, y), 0.3, fc="none", ec=C["pegda"], lw=0.7, ls=(0, (2, 2)), zorder=2))
for (x, y, a) in [(ex0 + 1.9, yt_ - 0.45, 20), (ex0 + 0.75, yb_ + 1.0, -30), (ex0 + 2.5, yb_ + 0.55, 40), (ex0 + 2.4, yt_ - 0.9, -60)]:
    dmtfa(x, y, a, 1.0)
anion(ex0 + 0.6, yb_ + 1.45, "pf6"); anion(ex0 + 1.6, yt_ - 1.05, "pf6"); anion(ex0 + 2.7, yb_ + 1.3, "dfob")
txt(ex0 + 0.1, yt_ + 0.1, "dendrites · thick organic SEI", fontsize=5.4, color=C["red"], ha="left")
txt(ex1 + 0.1, yt_ + 0.1, "particle cracking · TM dissolution", fontsize=5.4, color=C["red"], ha="right")
txt(x0 + PW / 2, y0 + 0.27, "Polymer –O– enters the Li⁺ shell", fontweight="bold", color=C["red"], fontsize=7)
txt(x0 + PW / 2, y0 + 0.1, "⁷Li upfield 0.22 ppm + shoulder · σ ↓ · Eₐ ↑ · interphases dominated by solvent/polymer decomposition",
    fontsize=5.4, color=C["red"])

# ---- bottom-right : MBA in-situ gel
x0, y0 = X2, YB
ex0, ex1, yb_, yt_ = cell(x0, y0, "MBA in-situ gel: solvation preserved · dual interphases", C["teal"], C["bg_r"],
                          C["lif"], C["sei_inorg"], 0.12, 0.12, False)
chain([(ex0 + 0.1, yt_ - 0.45), (ex0 + 0.9, yt_ - 0.75), (ex0 + 1.7, yt_ - 0.4), (ex0 + 2.5, yt_ - 0.75), (ex1 - 0.4, yt_ - 0.45)],
      C["pmba"], marks=42)
chain([(ex0 + 0.1, yb_ + 0.45), (ex0 + 0.9, yb_ + 0.75), (ex0 + 1.7, yb_ + 0.4), (ex0 + 2.5, yb_ + 0.75), (ex1 - 0.4, yb_ + 0.45)],
      C["pmba"], marks=42)
chain([(ex0 + 1.3, yt_ - 0.6), (ex0 + 1.4, (yb_ + yt_) / 2), (ex0 + 1.3, yb_ + 0.6)], C["pmba"], lw=1.3)
chain([(ex0 + 2.1, yt_ - 0.6), (ex0 + 2.0, (yb_ + yt_) / 2), (ex0 + 2.1, yb_ + 0.6)], C["pmba"], lw=1.3)
ym = (yb_ + yt_) / 2
solvate(ex0 + 0.75, ym, 0.85, "pf6", 15); solvate(ex0 + 1.7, ym, 0.85, "dfob", 60); solvate(ex0 + 2.65, ym, 0.85, "pf6", 100)
for (x, y, a) in [(ex0 + 0.4, yt_ - 0.25, 20), (ex0 + 2.3, yt_ - 0.2, -25), (ex0 + 0.45, yb_ + 0.2, -30), (ex0 + 2.9, yb_ + 0.22, 35)]:
    tte(x, y, a, 0.9)
txt(ex0 + 0.05, yt_ + 0.1, "uniform Li deposition · LiF / B–O-rich thin SEI", fontsize=5.4, color=C["teal"], ha="left")
txt(ex1 + 0.1, yt_ + 0.1, "thin CEI", fontsize=5.4, color=C["teal"], ha="right")
txt(x0 + PW / 2, y0 + 0.27, "Li⁺(DMTFA)ₙ solvates retained inside the network", fontweight="bold", color=C["teal"], fontsize=7)
txt(x0 + PW / 2, y0 + 0.1, "stable Li‖Li · 4.5 V Li‖NCM811 at 1C / 3C · LiF / B–O origin to be confirmed by XPS (C3 control)",
    fontsize=5.4, color=C["teal"])

# ============================ between-panel arrows
for yy, lab in [(YT + PH / 2, "Free-radical\nin-situ polymerization"), (YB + PH / 2, "Same electrolyte\namide vs ether network")]:
    ax.add_patch(FancyArrowPatch((X1 + PW + 0.12, yy), (X2 - 0.12, yy), arrowstyle="simple,head_width=9,head_length=7",
                                 color=C["grey"], lw=0, zorder=20))
    txt((X1 + PW + X2) / 2, yy + 0.32, lab, fontsize=6.2, color=C["grey"])

# ============================ legend
lx = 10.9; ly = 6.65
ax.text(lx, ly, "Legend", fontsize=8, fontweight="bold", va="center")
items = [("li", "Li⁺"), ("pf6", "PF₆⁻"), ("dfob", "DFOB⁻"), ("dmtfa", "DMTFA"), ("tte", "TTE"), ("mba", "MBA monomer"),
         ("pmba", "PMBA amide chain\n○ –CO–NH–"), ("pegda", "Ether-type chain\n○ –O–"), ("shell", "Li⁺ solvation shell"),
         ("hb", "N–H···anion\n(design, to verify)"), ("sei", "LiF/B–O-rich
SEI / CEI"), ("org", "Organic-rich
SEI / CEI")]
y = ly
for k, lab in items:
    y -= 0.46 if "\n" in lab else 0.36
    x = lx + 0.22
    if k == "li": li(x, y, 1.1)
    elif k in ("pf6", "dfob"): anion(x, y, k, 1.1)
    elif k == "dmtfa": dmtfa(x, y, 0, 1.0)
    elif k == "tte": tte(x, y, 0, 1.0)
    elif k == "mba": mba(x, y, 1.1)
    elif k in ("pmba", "pegda"):
        xs = np.linspace(x - 0.2, x + 0.2, 60); ax.plot(xs, y + 0.04 * np.sin(25 * (xs - x)), color=C[k], lw=1.8)
        ax.plot([x - 0.1, x + 0.1], [y + 0.04 * np.sin(-2.5), y + 0.04 * np.sin(2.5)], "o", ms=2.8, mfc="white", mec=C[k], mew=0.8)
    elif k == "shell": ax.add_patch(Circle((x, y), 0.14, fc="none", ec="#8A8F98", lw=0.6, ls=(0, (2, 2))))
    elif k == "hb": ax.plot([x - 0.18, x + 0.18], [y, y], color=C["hb"], lw=1.0, ls=(0, (2, 2)))
    elif k == "sei": ax.add_patch(Rectangle((x - 0.18, y - 0.06), 0.36, 0.12, fc=C["sei_inorg"], ec="none"))
    elif k == "org": ax.add_patch(Rectangle((x - 0.18, y - 0.06), 0.36, 0.12, fc=C["sei_org"], ec="none"))
    ax.text(lx + 0.55, y, lab, fontsize=6.2, va="center")

fig.savefig("figures/MBA_GPE_Mechanism_Schematic.png", facecolor="white")
fig.savefig("figures/MBA_GPE_Mechanism_Schematic.svg", facecolor="white")
print("saved")

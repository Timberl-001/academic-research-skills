"""Backup slides: why PMBA leaves the Li+ solvation shell intact while ether networks do not.
Produces figures/Why_PMBA_Schematic.png and MBA_GPE_Backup_Why_PMBA.pptx (2 slides, editable text).
Run from gpe_scientific_questions/.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, FancyArrowPatch
from scipy.ndimage import gaussian_filter1d

C = dict(li="#E57373", li_e="#B71C1C", pf6="#F0A868", pf6_e="#B9742B", dmtfa="#5DA9E9", dmtfa_e="#1F5F9F",
         pmba="#1F2A44", pegda="#8D5A2B", hb="#C62828", teal="#0E8A7A", red="#C0392B", grey="#3C4858")

# ------------------------------------------------------------------ schematic
W, H = 11.0, 4.6
fig = plt.figure(figsize=(W, H), dpi=250)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

def dmtfa(x, y, ang, s=1.0): ax.add_patch(Ellipse((x, y), 0.34 * s, 0.17 * s, angle=ang, fc=C["dmtfa"], ec=C["dmtfa_e"], lw=0.7, zorder=4))
def anion(x, y, s=1.0):
    ax.add_patch(Circle((x, y), 0.085 * s, fc=C["pf6"], ec=C["pf6_e"], lw=0.7, zorder=5)); ax.text(x, y, "P", ha="center", va="center", fontsize=5.5, color="white", fontweight="bold", zorder=6)
def li(x, y, s=1.0):
    ax.add_patch(Circle((x, y), 0.075 * s, fc=C["li"], ec=C["li_e"], lw=0.7, zorder=6)); ax.text(x, y, "Li⁺", ha="center", va="center", fontsize=4.8, color="white", fontweight="bold", zorder=7)
def solvate(x, y, s=1.0, rot=0):
    ax.add_patch(Circle((x, y), 0.37 * s, fc="white", ec="#8A8F98", lw=0.6, ls=(0, (2, 2)), zorder=2))
    for a in np.array([0, 120, 240]) + rot:
        r = np.deg2rad(a); dmtfa(x + 0.23 * s * np.cos(r), y + 0.23 * s * np.sin(r), a + 90, s)
    r = np.deg2rad(rot + 60); anion(x + 0.22 * s * np.cos(r), y + 0.22 * s * np.sin(r), s); li(x, y, s)
def chain(pts, color, lw=1.8, z=3, smooth=4):
    pts = np.asarray(pts); t = np.linspace(0, 1, len(pts)); tt = np.linspace(0, 1, 200)
    xs = gaussian_filter1d(np.interp(tt, t, pts[:, 0]), smooth); ys = gaussian_filter1d(np.interp(tt, t, pts[:, 1]), smooth)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=z); return xs, ys
def panel(x, y, w, h, title, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", fc="white", ec=color, lw=1.0, ls=(0, (4, 2)), zorder=0))
    ax.text(x + 0.15, y + h - 0.12, title, fontsize=9.5, fontweight="bold", color=color, va="top", zorder=9)
def amide(x, y, o_ang, h_ang, s=1.0):
    """-CO-NH- unit: C=O stick (red O) at o_ang, N-H stick (blue H) at h_ang (degrees)."""
    r = np.deg2rad(o_ang); ox, oy = x + 0.15 * s * np.cos(r), y + 0.15 * s * np.sin(r)
    ax.plot([x, ox], [y, oy], color=C["red"], lw=1.4, zorder=5); ax.plot(ox, oy, "o", ms=3.4, color=C["red"], zorder=6)
    r = np.deg2rad(h_ang); hx, hy = x + 0.16 * s * np.cos(r), y + 0.16 * s * np.sin(r)
    ax.plot([x, hx], [y, hy], color="#2B6CB0", lw=1.2, zorder=5); ax.plot(hx, hy, "o", ms=2.6, color="#2B6CB0", zorder=6)
    return (ox, oy), (hx, hy)

PW, PH = 5.25, 4.3
# ---------------- left: PMBA
x0, y0 = 0.15, 0.15
panel(x0, y0, PW, PH, "PMBA amide network: Li⁺ stays on DMTFA", C["teal"])
ax.add_patch(FancyBboxPatch((x0 + 0.15, y0 + 0.5), PW - 0.3, PH - 0.95, boxstyle="round,pad=0", fc="#F7F4EC", ec="none", zorder=0.3))
# short rigid crosslinked chains with amide units; N-H...O=C self association between chains
xa, ya = chain([(0.5, 3.55), (1.3, 3.4), (2.1, 3.6), (2.9, 3.4), (3.7, 3.6), (4.5, 3.45), (5.1, 3.6)], C["pmba"], lw=2.2)
xb, yb = chain([(0.5, 2.85), (1.3, 3.0), (2.1, 2.8), (2.9, 3.0), (3.7, 2.8), (4.5, 2.95), (5.1, 2.8)], C["pmba"], lw=2.2)
chain([(1.75, 3.55), (1.8, 3.2), (1.75, 2.85)], C["pmba"], lw=1.6); chain([(3.95, 3.55), (3.9, 3.2), (3.95, 2.85)], C["pmba"], lw=1.6)
pairs = []
for i in (30, 80, 130, 180):
    o1, h1 = amide(xa[i], ya[i], -90, 150, 0.9)   # top chain: O down, H up-left
    o2, h2 = amide(xb[i], yb[i], -30, 90, 0.9)    # bottom chain: H up, O down-right
    pairs.append((o1, h2))
for (o, h) in pairs:   # C=O...H-N self-association dashed
    ax.plot([o[0], h[0]], [o[1], h[1]], color=C["hb"], lw=0.9, ls=(0, (2, 2)), zorder=5)
ax.text(0.75, 3.15, "C=O", fontsize=6, color=C["red"]); ax.text(0.75, 2.62, "N–H", fontsize=6, color="#2B6CB0")
ax.text(2.7, 2.45, "N–H···O=C self-association occupies C=O;\nshort rigid links cannot chelate", ha="center", fontsize=7.5, color=C["hb"], zorder=9)
# liquid domain below with intact solvates (far from network)
solvate(1.3, 1.45, 1.0, 10); solvate(2.75, 1.4, 1.0, 70); solvate(4.2, 1.45, 1.0, 130)
ax.text(2.75, 0.78, "Li⁺(DMTFA)₃·PF₆⁻ solvates unchanged  ·  solvent amide : network amide ≈ 3–7 : 1", ha="center", fontsize=7.2, color=C["teal"], fontweight="bold", zorder=9)
ax.text(2.75, 0.35, "⁷Li Δδ ≈ 0.02 ppm · Raman 1526 ratio 0.55 vs 0.59 (liquid) · σ ≈ liquid", ha="center", fontsize=6.8, color="#555", zorder=9)

# ---------------- right: PEGDA
x0, y0 = 5.6, 0.15
panel(x0, y0, PW, PH, "Ether network (PEGDA): Li⁺ chelated by –O–", C["red"])
ax.add_patch(FancyBboxPatch((x0 + 0.15, y0 + 0.5), PW - 0.3, PH - 0.95, boxstyle="round,pad=0", fc="#EEF2F7", ec="none", zorder=0.3))
# flexible chain wrapping Li+ (crown-like loops)
def loop(cx, cy, r=0.42, n_o=5, ang0=110, span=320):
    th = np.deg2rad(np.linspace(ang0, ang0 + span, 120)); xs, ys = cx + r * np.cos(th), cy + r * np.sin(th)
    ax.plot(xs, ys, color=C["pegda"], lw=2.2, zorder=3)
    for a in np.linspace(ang0 + 20, ang0 + span - 20, n_o):
        rr = np.deg2rad(a); ax.plot(cx + r * np.cos(rr), cy + r * np.sin(rr), "o", ms=4, mfc="white", mec=C["pegda"], mew=1.0, zorder=4)
        ax.plot([cx + r * np.cos(rr), cx + 0.12 * np.cos(rr)], [cy + r * np.sin(rr), cy + 0.12 * np.sin(rr)], color=C["pegda"], lw=0.6, ls=":", zorder=3)
    li(cx, cy, 1.1)
    return xs, ys
l1 = loop(7.0, 3.0); l2 = loop(9.4, 3.05)
chain([(5.9, 3.6), (6.4, 3.5), (l1[0][0], l1[1][0])], C["pegda"], lw=2.2, smooth=2)
chain([(l1[0][-1], l1[1][-1]), (7.6, 3.75), (8.2, 3.3), (8.8, 3.75), (l2[0][0], l2[1][0])], C["pegda"], lw=2.2, smooth=2)
chain([(l2[0][-1], l2[1][-1]), (10.1, 3.7), (10.7, 3.5)], C["pegda"], lw=2.2, smooth=2)
# displaced / added: DMTFA partly outside
for (x, y, a) in [(6.3, 2.35, 30), (8.2, 2.75, -20), (10.4, 2.5, 50)]: dmtfa(x, y, a, 1.0)
anion(7.7, 2.3); anion(9.9, 2.4)
ax.text(8.2, 1.85, "flexible –O–C–C–O– backbone → 4–6 ether O chelate one Li⁺;\nno H-bond donor, O always exposed", ha="center", fontsize=7.5, color=C["red"], zorder=9)
solvate(6.9, 1.2, 0.85, 20); solvate(9.5, 1.2, 0.85, 80)
ax.text(8.2, 0.78, "ether O enters the Li⁺ shell (extra ligand) → new slow-exchange Li⁺ site", ha="center", fontsize=7.2, color=C["red"], fontweight="bold", zorder=9)
ax.text(8.2, 0.35, "⁷Li Δδ = −0.22 ppm + shoulder + broad base · Raman solvent markers ≈ liquid · σ ↓", ha="center", fontsize=6.8, color="#555", zorder=9)

fig.savefig("figures/Why_PMBA_Schematic.png", facecolor="white"); fig.savefig("figures/Why_PMBA_Schematic.svg", facecolor="white")

# ------------------------------------------------------------------ pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY = RGBColor(0x17, 0x2B, 0x46); TEAL = RGBColor(0x0E, 0x8A, 0x7A); GREY = RGBColor(0x66, 0x66, 0x66)
RED = RGBColor(0xC0, 0x39, 0x2B); LIGHT = RGBColor(0xF4, 0xF7, 0xFA); LINE = RGBColor(0xDF, 0xE7, 0xEF)
prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

def box(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = fill
    else: sh.fill.background()
    if line: sh.line.color.rgb = line; sh.line.width = Pt(1)
    else: sh.line.fill.background()
    sh.shadow.inherit = False; return sh

def text(s, x, y, w, h, runs, size=12, color=NAVY, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.06); tf.margin_top = tf.margin_bottom = Inches(0.03)
    first = True
    for r in runs:
        if isinstance(r, str): r = {"t": r}
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False; p.alignment = align
        run = p.add_run(); run.text = r["t"]; f = run.font; f.size = Pt(r.get("size", size)); f.bold = r.get("bold", bold); f.color.rgb = r.get("color", color); f.name = "微软雅黑"
    return tb

def title(s, t, tag):
    box(s, 0.4, 0.35, 0.08, 0.6, fill=TEAL)
    text(s, 0.55, 0.28, 10.5, 0.7, [{"t": t, "size": 26, "bold": True}])
    box(s, 11.3, 0.4, 1.6, 0.38, fill=RGBColor(0xFC, 0xF0, 0xEB), line=RGBColor(0xE9, 0xC9, 0xBE))
    text(s, 11.3, 0.4, 1.6, 0.38, [{"t": tag, "size": 10, "bold": True, "color": RGBColor(0xD6, 0x76, 0x61)}], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---- slide 1
s = prs.slides.add_slide(prs.slide_layouts[6])
title(s, "备用：为什么 PMBA 不改变 Li⁺ 溶剂化结构？", "答辩备用页")
s.shapes.add_picture("figures/Why_PMBA_Schematic.png", Inches(0.4), Inches(1.15), width=Inches(8.6))
cards = [("① 位点少", "MBA 每分子仅 2 个酰胺；溶剂酰胺 : 网络酰胺 ≈ 3–7 : 1，Li⁺ 的 3–4 个配位位早被 DMTFA / 阴离子占满", "待验证：MBA 含量梯度 → δ(⁷Li)、1526 比值应为水平线"),
         ("② 够不着", "酰胺间仅隔 CH₂、主链为碳链且高交联 → 无法像 –O–C–C–O– 那样 4–6 齿螯合；单齿 C=O 竞争不过可自由取向的 DMTFA", "待验证：DFT 结合能与螯合几何；MD 酰胺-O 配位数"),
         ("③ 被自己占了", "仲酰胺 N–H···O=C 自缔合占住 C=O 孤对；同时导致相分离（白色），网络与液相接触面积小", "待验证：无盐 vs 含盐 PMBA 凝胶的酰胺 I / N–H 位置")]
y = 1.15
for h, d, todo in cards:
    box(s, 9.2, y, 3.75, 1.6, fill=LIGHT, line=LINE)
    text(s, 9.3, y + 0.05, 3.6, 0.35, [{"t": h, "size": 13, "bold": True, "color": TEAL}])
    text(s, 9.3, y + 0.4, 3.6, 0.8, [{"t": d, "size": 9.5}])
    text(s, 9.3, y + 1.2, 3.6, 0.38, [{"t": todo, "size": 8.5, "color": GREY}])
    y += 1.72
box(s, 0.4, 6.45, 12.55, 0.7, fill=RGBColor(0xEA, 0xF6, 0xF3), line=LINE)
text(s, 0.5, 6.45, 12.35, 0.7, [{"t": "口径：酰胺 C=O 是强供体，不是靠\"弱配位\"；靠的是 位点数 × 可及性 × 自缔合 三者叠加。PEGDA 的醚氧是\"加入\"配位壳（溶剂侧拉曼不变、⁷Li 变），不是置换 DMTFA。", "size": 11, "bold": True, "color": TEAL}], anchor=MSO_ANCHOR.MIDDLE)
s.notes_slide.notes_text_frame.text = ("不是因为酰胺C=O配位弱——它其实是强供体。PMBA做到不改变靠三件事叠加：位点少、位点够不着、位点被自己占了。"
    "MBA一个分子只有两个酰胺，聚合后是短而刚性的交联网络，C=O之间隔着亚甲基和主链，无法像聚醚那样多齿螯合；相邻链的N–H···O=C自缔合把C=O占住；而DMTFA的酰胺浓度是网络酰胺的几倍，Li⁺从一开始就被DMTFA包好。"
    "聚醚恰恰相反：柔性主链、氧原子密集、能形成5–6配位螯合环，热力学上优于小分子溶剂。⁷Li、拉曼1526带、σ三组数据都指向这个判断；含量梯度、无盐凝胶红外和DFT/MD是后续验证。")

# ---- slide 2
s = prs.slides.add_slide(prs.slide_layouts[6])
title(s, "备用：其它骨架为什么做不到？", "答辩备用页")
rows = [("骨架类型", "配位位点与拓扑", "对溶剂化结构的影响", "文献 / 本工作证据"),
        ("聚醚（PEGDA, PEO, PDOL）", "醚氧密集、主链柔性、无 H 供体 → 4–6 齿螯合", "醚氧进入 Li⁺ 壳，出现慢交换新位点；σ↓、Eₐ↑", "Ionics 2022 PDOL：⁷Li 高场移、D_Li 降 2 个数量级；本工作 C1：Δδ −0.22 ppm + 肩峰"),
        ("聚酯 / 聚碳酸酯（PCL, PTMC, PVCA）", "酯 C=O 单齿但密度高、链柔", "部分配位；⁷Li 位移方向随聚合物而异", "ChemRxiv 2025 PCL 凝胶：⁷Li 低场移"),
        ("聚腈 / 聚酰亚胺（PAN, PI）", "C≡N、酰亚胺 C=O 强配位，骨架刚性", "Li⁺ 易被固定，传输受限", "PAN 基 GPE 文献普遍报道 Li⁺–CN 配位"),
        ("氟聚合物（PVDF-HFP）", "不配位，仅物理溶胀", "溶剂化由液相决定，但非原位、保液与力学差", "常作惰性骨架对照"),
        ("PMBA 酰胺网络（本工作）", "位点少 · 短刚性链不能螯合 · N–H···O=C 自缔合 · 相分离减少接触", "Li⁺ 保留在 DMTFA 溶剂化壳中", "⁷Li Δδ ≈ 0.02 ppm；Raman 1526 比值 0.55 vs 0.59；σ ≈ 液态")]
widths = [2.4, 3.3, 3.1, 3.75]; x0 = 0.4; y = 1.2; rh = [0.5, 0.85, 0.75, 0.7, 0.7, 0.9]
for i, r in enumerate(rows):
    x = x0; h = rh[i]
    for j, cell in enumerate(r):
        fill = TEAL if i == 0 else (RGBColor(0xEA, 0xF6, 0xF3) if i == len(rows) - 1 else (LIGHT if i % 2 else RGBColor(255, 255, 255)))
        box(s, x, y, widths[j], h, fill=fill, line=LINE, shape=MSO_SHAPE.RECTANGLE)
        text(s, x, y, widths[j], h, [{"t": cell, "size": 11 if i == 0 else 9.5, "bold": (i == 0 or i == len(rows) - 1), "color": RGBColor(255, 255, 255) if i == 0 else NAVY}], anchor=MSO_ANCHOR.MIDDLE)
        x += widths[j]
    y += h
box(s, 0.4, y + 0.25, 12.55, 1.1, fill=LIGHT, line=LINE)
text(s, 0.5, y + 0.28, 12.35, 1.05, [
    {"t": "判据：网络能否在一个 Li⁺ 周围同时排布 ≥3 个供体原子，且这些供体在液相中是否已被更多、更自由的溶剂配体占据。", "size": 11, "bold": True},
    {"t": "追问预案：\"N–H 为什么不配 Li⁺？\" → N–H 是氢键供体而非 Li⁺ 配体，作用对象是阴离子（PF₆⁻ 的 F、DFOB⁻ 的 C=O），这是创新点②的出发点（待 ¹⁹F / FTIR 验证）。", "size": 10, "color": GREY}], anchor=MSO_ANCHOR.MIDDLE)
s.notes_slide.notes_text_frame.text = ("分类回答：聚醚靠柔性链和高密度醚氧螯合，热力学上优于小分子溶剂；聚酯、聚腈配位能力不低且密度高；PVDF-HFP不配位但只是物理溶胀、非原位。"
    "PMBA的特殊性在于位点少、不能螯合、自缔合占位、相分离减少接触四者叠加，在酰胺溶剂中数量与几何决定了Li⁺留在DMTFA上。")
prs.save("MBA_GPE_Backup_Why_PMBA.pptx"); print("saved")

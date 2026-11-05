"""Composite 'solvation preserved' evidence figure for PPT page 8:
(a) 7Li NMR overlay, (b) Raman PF6-/CF3 region, (c) FTIR C=O region (user's screenshot placeholder).
Run from gpe_scientific_questions/.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import image as mpimg

col = {"liquid": "#1f1f1f", "PMBA": "#d62728", "PEGDA": "#1f77b4", "DMTFA": "#7f7f7f"}
lab = {"liquid": "Liquid (C0)", "PMBA": "PMBA gel (S)", "PEGDA": "PEGDA gel (C1)", "DMTFA": "DMTFA"}
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})

fig = plt.figure(figsize=(13.3, 4.9), dpi=220)
gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1], wspace=0.28, left=0.04, right=0.985, top=0.83, bottom=0.16)

# ---------------- (a) 7Li
ax = fig.add_subplot(gs[0])
off, step = 0, 1.2
for k in ["PEGDA", "PMBA", "liquid"]:
    d = np.loadtxt(f"data/7Li/processed/7Li-{k}_ppm_vs_ref.txt")
    ppm, y = d[:, 0], d[:, 1]
    m = (ppm > -0.32) & (ppm < 0.52); pp, yy = ppm[m], y[m].copy()
    yy = yy / yy[np.abs(pp) > 0.025].max(); yy = np.minimum(yy, 1.05)
    ax.plot(pp, yy + off, color=col[k], lw=1.5)
    ax.text(0.51, off + 0.7, lab[k], color=col[k], fontsize=9.5, fontweight="bold", ha="left")
    off += step
ax.axvline(0.172, ls="--", color="#1f1f1f", lw=0.8, alpha=0.5)
ax.axvline(-0.048, ls="--", color="#1f77b4", lw=0.8, alpha=0.6)
ax.text(0.172, 2 * step + 1.1, "0.17", ha="center", fontsize=8.5)
ax.text(0.19, step + 1.1, "Δδ = +0.02 ppm", ha="center", fontsize=8.5, color="#d62728", fontweight="bold")
ax.text(-0.13, 0.55, "Δδ = −0.22 ppm\n+ shoulder\n+ broad base", ha="left", fontsize=8.5, color="#1f77b4", fontweight="bold")
ax.text(0.0, 2 * step + 1.1, "ext. ref.", ha="center", fontsize=7.5, color="gray")
ax.set_xlim(0.52, -0.32); ax.set_ylim(-0.1, 2 * step + 1.45); ax.set_yticks([])
ax.set_xlabel("$^7$Li chemical shift (ppm vs. ext. ref.)")
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
ax.set_title("(a) $^7$Li NMR: Li⁺ environment", loc="left", fontsize=10.5, fontweight="bold")

# ---------------- (b) Raman
ax = fig.add_subplot(gs[1])
fmap = {"DMTFA": "DMTFA", "liquid": "LE", "PMBA": "PMBA_gel", "PEGDA": "PEGDA_gel"}
for k in ["DMTFA", "liquid", "PMBA", "PEGDA"]:
    d = np.loadtxt(f"data/Raman/processed/Raman_{fmap[k]}_baseline_corrected.txt")
    x, y = d[:, 0], d[:, 1]
    m = (x > 700) & (x < 800); ref = y[(x > 750) & (x < 770)].max()
    ax.plot(x[m], y[m] / ref, color=col[k], lw=1.4, marker="o", ms=2.5, label=lab[k])
ax.axvspan(736, 750, color="#1f77b4", alpha=0.08)
ax.text(743, 0.58, "PF$_6^-$ ν$_1$", ha="center", fontsize=8.5, color="#1f77b4")
ax.annotate("DMTFA δs(CF$_3$)\n758 → 760–761 cm$^{-1}$\n(same in liquid & both gels)", xy=(761, 1.0), xytext=(785, 0.75),
            fontsize=8, ha="center", arrowprops=dict(arrowstyle="->", lw=0.7))
ax.set_xlim(700, 800); ax.set_ylim(-0.08, 1.1)
ax.set_xlabel("Raman shift (cm$^{-1}$)"); ax.set_ylabel("Intensity (norm. to 760 cm$^{-1}$)")
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
ax.set_title("(b) Raman: solvent-side probe", loc="left", fontsize=10.5, fontweight="bold")

# ---------------- (c) FTIR (user's figure as placeholder; replace with replotted ATR data later)
ax = fig.add_subplot(gs[2])
img = mpimg.imread("figures/FTIR_CO_region_user.png")
ax.imshow(img); ax.axis("off")
ax.set_title("(c) FTIR: C=C consumed; DMTFA C=O\n     unchanged at 1688 cm$^{-1}$ (PEGDA)", loc="left", fontsize=10.5, fontweight="bold")
ax.text(0.5, -0.03, "PMBA \"1680\" = overlap with polymer amide I\n(to be deconvoluted with salt-free control)", transform=ax.transAxes,
        ha="center", va="top", fontsize=7.5, color="#666")

fig.suptitle("Amide network does not rewrite the Li⁺ solvation structure; ether network does",
             fontsize=12, fontweight="bold", y=0.97)
fig.text(0.5, 0.015, "S ≈ C0 in all three probes · C1 deviates in all three   |   pending: MBA-content series, ¹H N(CH₃)₂ shift, salt-free PMBA FTIR, Eₐ,σ",
         ha="center", fontsize=8.5, color="#0E8A7A")
fig.savefig("figures/Solvation_Evidence_Composite.png", facecolor="white")
fig.savefig("figures/Solvation_Evidence_Composite.svg", facecolor="white")
print("saved")

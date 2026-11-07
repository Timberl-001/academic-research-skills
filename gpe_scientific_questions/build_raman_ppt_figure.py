"""PPT-ready Raman figure (minimal text): (a) stacked spectra 1380-1780, (b) difference spectra.
Same pipeline as build_raman_solvation_figure.py (ALS baseline, normalise to DMTFA CH3 1400-1445 area).
Run from gpe_scientific_questions/."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve

tr = np.trapezoid
files = {"Solvent": "DMTFA+TTE", "LE_PF6": "LiPF6+DMTFA+TTE", "LE": "LiDFOB+LiPF6+DMTFA+TTE",
         "PMBA": "PMBA+LE", "PEGDA": "PEGDA+LE"}
lab = {"Solvent": "DMTFA:TTE (no salt)", "LE_PF6": "+1.0 M LiPF₆", "LE": "Liquid LE",
       "PMBA": "PMBA gel", "PEGDA": "PEGDA gel"}
col = {"Solvent": "#B5A400", "LE_PF6": "#2E8B57", "LE": "#1f1f1f", "PMBA": "#d62728", "PEGDA": "#1f77b4"}
order = ["Solvent", "LE_PF6", "LE", "PMBA", "PEGDA"]
RAW = {k: np.loadtxt(f"data/Raman_v2/raw/{f}.txt", comments="#", encoding="latin-1").T for k, f in files.items()}


def als(y, lam=1e6, p=0.005, n=10):
    L = len(y); D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2), format="csc"); w = np.ones(L)
    for _ in range(n):
        W = sparse.spdiags(w, 0, L, L, format="csc"); z = spsolve(W + lam * D.dot(D.T), w * y); w = p * (y > z) + (1 - p) * (y < z)
    return z


def area(x, y, lo, hi): m = (x > lo) & (x < hi); return tr(np.clip(y[m], 0, None), x[m])


B = {}
for k, (x, y) in RAW.items():
    yb = y - als(y); B[k] = (x, yb / area(x, yb, 1400, 1445) * 1000)
x = B["LE"][0]
ratio = {k: area(*B[k], 1500, 1550) / area(*B[k], 1400, 1445) for k in order}

plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans"})
fig, axs = plt.subplots(1, 2, figsize=(12.5, 5), dpi=220, gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.22))

# (a) stacked spectra
ax = axs[0]; w = (x > 1380) & (x < 1780)
for i, k in enumerate(order):
    xx, yy = B[k]; off = (len(order) - 1 - i) * 26
    ax.plot(xx[w], yy[w] + off, color=col[k], lw=1.4)
    ax.text(1600, off + 6, lab[k], ha="center", va="bottom", color=col[k], fontsize=10, fontweight="bold")
for v, t in [(1430, "δ(CH₃)\nref."), (1526, "Li⁺–DMTFA\n1526"), (1690, "ν(C=O)\n1690")]:
    ax.axvline(v, color="#BBB", lw=0.8, ls=":", zorder=0); ax.text(v, 26 * (len(order) - 1) + 36, t, ha="center", va="bottom", fontsize=8.5, color="#555")
ax.set_xlim(1380, 1780); ax.set_ylim(-3, 26 * (len(order) - 1) + 52); ax.set_yticks([])
ax.set_xlabel("Raman shift (cm⁻¹)"); ax.spines[["top", "right", "left"]].set_visible(False)

# (b) difference spectra
ax = axs[1]; w = (x > 1380) & (x < 1780)
d_salt = B["LE"][1] - B["Solvent"][1]; d_pmba = B["PMBA"][1] - B["LE"][1]; d_pegda = B["PEGDA"][1] - B["LE"][1]
ax.axhline(0, color="#999", lw=0.8)
for sp in ([1500, 1550], [1650, 1750]): ax.axvspan(*sp, color="#EEE", zorder=0)
ax.plot(x[w], d_salt[w], color="#1f1f1f", lw=1.6, label="LE − solvent   (what 1.2 M salt does)")
ax.plot(x[w], d_pmba[w], color="#d62728", lw=1.6, label="PMBA gel − LE   (what PMBA adds)")
ax.plot(x[w], d_pegda[w], color="#1f77b4", lw=1.6, label="PEGDA gel − LE   (what PEGDA adds)")
ax.text(1526, 10.6, "1526 ↑", ha="center", fontsize=9); ax.text(1690, -9.2, "C=O 1690 ↓", ha="center", fontsize=9)
ax.text(1629, 6.4, "residual\nC=C", ha="center", fontsize=8.5, color="#d62728")
ax.set_xlim(1380, 1780); ax.set_ylim(-10.5, 17); ax.set_xlabel("Raman shift (cm⁻¹)"); ax.set_ylabel("Δ intensity (norm.)")
ax.legend(fontsize=9, frameon=False, loc="lower left"); ax.spines[["top", "right"]].set_visible(False)
# ratio inset text
txt = "A(1526)/A(1430)\n" + "\n".join(f"{lab[k]:<20s}{ratio[k]:.2f}" for k in ["Solvent", "LE", "PMBA", "PEGDA"])
ax.text(0.985, 0.985, txt, transform=ax.transAxes, ha="right", va="top", fontsize=8.5, family="DejaVu Sans Mono",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#CCC"))

fig.savefig("figures/Raman_PPT_Solvation.png", bbox_inches="tight", facecolor="white")
fig.savefig("figures/Raman_PPT_Solvation.svg", bbox_inches="tight", facecolor="white")
print({k: round(v, 3) for k, v in ratio.items()})

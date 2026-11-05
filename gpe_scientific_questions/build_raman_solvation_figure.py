"""Publication-style Raman figure supporting 'solvation structure preserved' (innovation point 1).
Uses the high-S/N v2 data set (6 samples). Run from gpe_scientific_questions/.
Panels: (a) full spectra, (b) salt-induced difference spectra, (c) 1526 marker zoom, (d) marker ratios with
uncertainty from baseline/window variation.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve

tr = np.trapezoid
files = {"DMTFA": "DMTFA", "Solvent": "DMTFA+TTE", "LE_PF6": "LiPF6+DMTFA+TTE", "LE": "LiDFOB+LiPF6+DMTFA+TTE",
         "PMBA": "PMBA+LE", "PEGDA": "PEGDA+LE"}
lab = {"DMTFA": "DMTFA", "Solvent": "DMTFA : TTE (no salt)", "LE_PF6": "+1.0 M LiPF₆", "LE": "Liquid C0\n(+0.2 M LiDFOB)",
       "PMBA": "PMBA gel (S)", "PEGDA": "PEGDA gel (C1)"}
lab1 = {k: v.replace("\n", " ") for k, v in lab.items()}
col = {"DMTFA": "#9E9E9E", "Solvent": "#B5A400", "LE_PF6": "#2E8B57", "LE": "#1f1f1f", "PMBA": "#d62728", "PEGDA": "#1f77b4"}
order = ["DMTFA", "Solvent", "LE_PF6", "LE", "PMBA", "PEGDA"]
RAW = {k: np.loadtxt(f"data/Raman_v2/raw/{f}.txt", comments="#", encoding="latin-1").T for k, f in files.items()}


def als(y, lam=1e6, p=0.005, n=10):
    L = len(y); D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2), format="csc"); w = np.ones(L)
    for _ in range(n):
        W = sparse.spdiags(w, 0, L, L, format="csc"); z = spsolve(W + lam * D.dot(D.T), w * y); w = p * (y > z) + (1 - p) * (y < z)
    return z


def proc(lam=1e6, p=0.005):
    out = {}
    for k, (x, y) in RAW.items():
        yb = y - als(y, lam, p); m = (x > 1400) & (x < 1445); out[k] = (x, yb / tr(np.clip(yb[m], 0, None), x[m]) * 1000)  # norm to CH3 1430 area
    return out


def area(x, y, lo, hi): m = (x > lo) & (x < hi); return tr(np.clip(y[m], 0, None), x[m])


B = proc()
# ---- uncertainty: vary baseline stiffness & integration windows
ratios = {k: {"1526": [], "CO": []} for k in order}
for lam in (3e5, 1e6, 3e6):
    for p in (0.003, 0.005, 0.01):
        Bb = proc(lam, p)
        for k in order:
            x, y = Bb[k]
            for (lo, hi) in ((1500, 1550), (1505, 1548), (1498, 1555)):
                ratios[k]["1526"].append(area(x, y, lo, hi) / 1000)
            for (lo, hi) in ((1650, 1750), (1655, 1745), (1645, 1755)):
                ratios[k]["CO"].append(area(x, y, lo, hi) / 1000)
stats = {k: {m: (np.mean(v), np.std(v)) for m, v in d.items()} for k, d in ratios.items()}
for k in order:
    print(f"{k:8s} A1526/A1430 = {stats[k]['1526'][0]:.3f} ± {stats[k]['1526'][1]:.3f}   A(C=O)/A1430 = {stats[k]['CO'][0]:.3f} ± {stats[k]['CO'][1]:.3f}")

# ------------------------------------------------------------------ figure
plt.rcParams.update({"font.size": 9.5, "font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(12.5, 7.6), dpi=250)
gs = fig.add_gridspec(2, 3, width_ratios=[1.35, 1, 1], height_ratios=[1, 1], wspace=0.3, hspace=0.38,
                      left=0.05, right=0.985, top=0.93, bottom=0.08)

# (a) full spectra stack
ax = fig.add_subplot(gs[:, 0]); off = 0
for k in order:
    x, y = B[k]; m = (x > 300) & (x < 1800); yy = y[m] / y[m].max()
    ax.plot(x[m], yy + off, color=col[k], lw=1.0)
    ax.text(1795, off + 0.55, lab1[k], ha="right", fontsize=8, color=col[k], fontweight="bold")
    off += 1.02
for v, t, dy in [(760, "δs(CF₃)", 0.02), (855, "TTE", 0.22), (1430, "δ(CH₃) ref.", 0.02), (1526, "1526", 0.22), (1690, "ν(C=O)", 0.02)]:
    ax.axvline(v, color="#BBB", ls=":", lw=0.7, zorder=0); ax.text(v, off + dy, t, ha="center", va="bottom", fontsize=7, color="#555")
ax.set_xlim(300, 1800); ax.set_ylim(-0.05, off + 0.45); ax.set_yticks([]); ax.set_xlabel("Raman shift (cm$^{-1}$)")
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.set_title("(a) Raman spectra (532 nm), baseline-corrected", loc="left", fontsize=10, fontweight="bold")

# (b) difference spectra: what salt does vs what gelation does
ax = fig.add_subplot(gs[0, 1:])
xs, y_solv = B["Solvent"]; y_le = B["LE"][1]; y_pf6 = B["LE_PF6"][1]; y_s = B["PMBA"][1]; y_c1 = B["PEGDA"][1]
m = (xs > 1380) & (xs < 1780)
ax.plot(xs[m], (y_le - y_solv)[m], color="#1f1f1f", lw=1.3, label="C0 − solvent  (effect of 1.2 M salt)")
ax.plot(xs[m], (y_s - y_le)[m], color="#d62728", lw=1.3, label="S − C0  (effect of PMBA network)")
ax.plot(xs[m], (y_c1 - y_le)[m], color="#1f77b4", lw=1.3, label="C1 − C0  (effect of PEGDA network)")
ax.axhline(0, color="#999", lw=0.6)
ax.axvspan(1500, 1550, color="#999", alpha=0.08); ax.axvspan(1650, 1750, color="#999", alpha=0.08)
ax.annotate("1526 ↑", xy=(1526, (y_le - y_solv)[(xs > 1520) & (xs < 1532)].max()), xytext=(1560, 7.5), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.7))
ax.annotate("C=O 1690 ↓ / ~1712 ↑", xy=(1690, (y_le - y_solv)[(xs > 1686) & (xs < 1694)].min()), xytext=(1600, -8.5), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.7))
ax.text(1629, (y_s - y_le)[(xs > 1625) & (xs < 1633)].max() + 0.8, "1629 residual C=C\n(PMBA only)", ha="center", fontsize=7, color="#d62728")
ax.set_xlim(1380, 1780); ax.set_xlabel("Raman shift (cm$^{-1}$)"); ax.set_ylabel("Δ intensity (norm. to 1430)")
ax.legend(fontsize=7.5, frameon=False, loc="lower left")
ax.set_title("(b) Difference spectra: salt changes DMTFA bands, PMBA gelation does not", loc="left", fontsize=10, fontweight="bold")

# (c) 1526 zoom
ax = fig.add_subplot(gs[1, 1])
for k in order:
    x, y = B[k]; m = (x > 1495) & (x < 1560); ax.plot(x[m], y[m], color=col[k], lw=1.3, label=lab1[k])
ax.axvline(1526, color="#BBB", ls=":", lw=0.7)
ax.set_xlim(1495, 1560); ax.set_xlabel("Raman shift (cm$^{-1}$)"); ax.set_ylabel("Intensity (norm. to 1430)")
ax.set_title("(c) Li⁺-induced DMTFA band", loc="left", fontsize=10, fontweight="bold")

# (d) marker ratios
ax = fig.add_subplot(gs[1, 2])
xi = np.arange(len(order)); w = 0.38
m1 = [stats[k]["1526"][0] for k in order]; e1 = [stats[k]["1526"][1] for k in order]
m2 = [stats[k]["CO"][0] for k in order]; e2 = [stats[k]["CO"][1] for k in order]
ax.bar(xi - w / 2, m1, w, yerr=e1, capsize=2, color=[col[k] for k in order], ec="none", label="A(1526) / A(1430)")
ax.bar(xi + w / 2, m2, w, yerr=e2, capsize=2, color=[col[k] for k in order], alpha=0.35, ec="none", label="A(C=O) / A(1430)")
for i, v in enumerate(m1): ax.text(xi[i] - w / 2, v + 0.02, f"{v:.2f}", ha="center", fontsize=6.5)
ax.axhspan(m1[3] - e1[3], m1[3] + e1[3], color="#1f1f1f", alpha=0.08)
ax.set_xticks(xi); ax.set_xticklabels(["DMTFA", "solvent", "+LiPF₆", "C0", "S", "C1"], fontsize=7.5)
ax.set_ylim(0, 0.75); ax.set_ylabel("Area ratio"); ax.legend(fontsize=7, frameon=False, loc="upper left")
ax.set_title("(d) Coordination markers: S ≈ C0", loc="left", fontsize=10, fontweight="bold")
ax.text(5.4, m1[3] + e1[3] + 0.015, "C0 ± σ", fontsize=6.5, color="#555", ha="right")

fig.suptitle("Solvent-side Raman probes: PMBA gelation leaves the Li⁺–DMTFA coordination unchanged", fontsize=12, fontweight="bold")
fig.savefig("figures/Raman_Solvation_Preserved.png", facecolor="white"); fig.savefig("figures/Raman_Solvation_Preserved.svg", facecolor="white")
print("saved")

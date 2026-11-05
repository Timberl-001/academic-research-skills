"""Raman spectral decomposition with pure-component references (DMTFA, TTE).
Each electrolyte spectrum = a*DMTFA + b*TTE + residual. Residual isolates salt-/polymer-induced features;
coefficient ratio a/b tracks the DMTFA:TTE composition actually probed. Run from gpe_scientific_questions/.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.optimize import nnls

files = {"DMTFA": "DMTFA", "TTE": "TTE", "Solvent": "DMTFA+TTE", "LE_PF6": "LiPF6+DMTFA+TTE",
         "LE": "LiDFOB+LiPF6+DMTFA+TTE", "PMBA": "PMBA+LE", "PEGDA": "PEGDA+LE"}
lab = {"Solvent": "DMTFA:TTE (no salt)", "LE_PF6": "+1.0 M LiPF₆", "LE": "Liquid C0", "PMBA": "PMBA gel (S)", "PEGDA": "PEGDA gel (C1)"}
col = {"Solvent": "#B5A400", "LE_PF6": "#2E8B57", "LE": "#1f1f1f", "PMBA": "#d62728", "PEGDA": "#1f77b4", "DMTFA": "#9E9E9E", "TTE": "#5BA8A0"}


def als(y, lam=1e6, p=0.005, n=10):
    L = len(y); D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2), format="csc"); w = np.ones(L)
    for _ in range(n):
        W = sparse.spdiags(w, 0, L, L, format="csc"); z = spsolve(W + lam * D.dot(D.T), w * y); w = p * (y > z) + (1 - p) * (y < z)
    return z


B = {}
for k, f in files.items():
    x, y = np.loadtxt(f"data/Raman_v2/raw/{f}.txt", comments="#", encoding="latin-1").T; B[k] = y - als(y)
X = x
m = (X > 300) & (X < 1800); xm = X[m]
A = np.c_[B["DMTFA"][m], B["TTE"][m]]
coef, resid = {}, {}
for k in ["Solvent", "LE_PF6", "LE", "PMBA", "PEGDA"]:
    y = B[k][m]; c, _ = nnls(A, y); coef[k] = c; resid[k] = y - A @ c
    print(f"{k:8s} a(DMTFA)={c[0]:.3f} b(TTE)={c[1]:.3f} a/b={c[0]/c[1]:.2f}  resid RMS = {np.sqrt((resid[k]**2).mean())/y.max()*100:.1f}% of max")
# TTE band centroids (non-coordinating check)
cent = {}
for k in ["TTE", "Solvent", "LE", "PMBA", "PEGDA"]:
    yy = B[k]; row = []
    for lo, hi in [(840, 870), (1110, 1135), (1275, 1300)]:
        w = (X > lo) & (X < hi); row.append((X[w] * np.clip(yy[w], 0, None)).sum() / np.clip(yy[w], 0, None).sum())
    cent[k] = row
with open("data/Raman_v2/processed/decomposition_summary.txt", "w") as f:
    f.write("sample\ta_DMTFA\tb_TTE\ta/b\tTTE855\tTTE1123\tTTE1287\n")
    for k in ["Solvent", "LE_PF6", "LE", "PMBA", "PEGDA"]:
        c = coef[k]; cc = cent.get(k, [np.nan] * 3)
        f.write(f"{k}\t{c[0]:.3f}\t{c[1]:.3f}\t{c[0]/c[1]:.2f}\t" + "\t".join(f"{v:.1f}" for v in cc) + "\n")

# ------------------------------------------------------------------ figure
plt.rcParams.update({"font.size": 9.5, "font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(12.5, 7.4), dpi=250)
gs = fig.add_gridspec(2, 3, width_ratios=[1.3, 1, 0.9], wspace=0.3, hspace=0.42, left=0.05, right=0.985, top=0.92, bottom=0.08)
norm = B["DMTFA"][m].max()

# (a) decomposition of C0
ax = fig.add_subplot(gs[0, :2])
y = B["LE"][m]; c = coef["LE"]
ax.plot(xm, y / norm, color="#1f1f1f", lw=1.2, label="Liquid C0 (data)")
ax.plot(xm, (A @ c) / norm, color="#E67E22", lw=0.9, ls="--", label=f"{c[0]:.2f}·DMTFA + {c[1]:.2f}·TTE")
ax.plot(xm, c[0] * A[:, 0] / norm - 0.55, color=col["DMTFA"], lw=0.9, label="DMTFA component")
ax.plot(xm, c[1] * A[:, 1] / norm - 0.55, color=col["TTE"], lw=0.9, label="TTE component")
ax.plot(xm, resid["LE"] / norm - 0.95, color="#8E44AD", lw=1.0, label="residual = salt-induced features")
ax.axhline(-0.95, color="#BBB", lw=0.5)
for v in (1410, 1435, 1526, 1690, 760):
    ax.axvline(v, color="#DDD", lw=0.5, zorder=0)
ax.set_xlim(300, 1800); ax.set_yticks([]); ax.set_xlabel("Raman shift (cm$^{-1}$)")
ax.legend(fontsize=7.5, frameon=False, ncol=3, loc="upper left")
ax.set_title("(a) Spectral decomposition with pure-solvent references (C0 shown)", loc="left", fontsize=10, fontweight="bold")
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)

# (b) a/b composition ratio
ax = fig.add_subplot(gs[0, 2])
ks = ["Solvent", "LE_PF6", "LE", "PMBA", "PEGDA"]; r = [coef[k][0] / coef[k][1] for k in ks]
ax.bar(range(len(ks)), r, color=[col[k] for k in ks])
for i, v in enumerate(r): ax.text(i, v + 0.15, f"{v:.1f}", ha="center", fontsize=8)
ax.axhline(r[2], color="#1f1f1f", ls=":", lw=0.8)
ax.set_xticks(range(len(ks))); ax.set_xticklabels(["solv.", "+LiPF₆", "C0", "S", "C1"], fontsize=8)
ax.set_ylabel("DMTFA / TTE intensity ratio (a/b)"); ax.set_ylim(0, max(r) * 1.45)
ax.set_title("(b) TTE depleted in gels", loc="left", fontsize=10, fontweight="bold", color="#C0392B")
ax.text(0.04, 0.93, "liquid ≈ 1.6\nPMBA gel ≈ 10\nTTE loss during curing\nor phase segregation?", transform=ax.transAxes, ha="left", va="top", fontsize=7.3, color="#C0392B")

# (c) residual differences: salt vs network
ax = fig.add_subplot(gs[1, :2])
w = (xm > 1350) & (xm < 1800)
ax.plot(xm[w], resid["LE"][w] / norm, color="#1f1f1f", lw=1.3, label="C0 residual  (what 1.2 M salt does to DMTFA)")
ax.plot(xm[w], (resid["PMBA"] - resid["LE"])[w] / norm, color="#d62728", lw=1.3, label="S residual − C0 residual  (what PMBA network adds)")
ax.plot(xm[w], (resid["PEGDA"] - resid["LE"])[w] / norm, color="#1f77b4", lw=1.3, label="C1 residual − C0 residual  (what PEGDA network adds)")
ax.axhline(0, color="#999", lw=0.6)
for lo, hi in ((1400, 1445), (1500, 1550), (1650, 1750)): ax.axvspan(lo, hi, color="#999", alpha=0.08)
ax.text(1422, 0.17, "δ(CH₃) shift", ha="center", fontsize=7.5); ax.text(1526, 0.16, "1526 ↑", ha="center", fontsize=7.5)
ax.text(1690, -0.14, "ν(C=O) 1690 ↓", ha="center", fontsize=7.5)
ax.text(1629, (resid["PMBA"] - resid["LE"])[(xm > 1625) & (xm < 1633)].max() / norm + 0.01, "1629 residual C=C", ha="center", fontsize=7.5, color="#d62728")
ax.set_xlim(1350, 1800); ax.set_xlabel("Raman shift (cm$^{-1}$)"); ax.set_ylabel("Δ (norm. to DMTFA max)")
ax.legend(fontsize=7.5, frameon=False, loc="lower left")
ax.set_title("(c) Salt-induced DMTFA features identical in liquid and gels; networks add nothing in these bands", loc="left", fontsize=10, fontweight="bold")

# (d) TTE band positions
ax = fig.add_subplot(gs[1, 2])
ks2 = ["TTE", "Solvent", "LE", "PMBA", "PEGDA"]; names = ["TTE", "solv.", "C0", "S", "C1"]
for j, (lo, c0) in enumerate([(855, "#5BA8A0"), (1123, "#3C7F78"), (1287, "#245550")]):
    vals = [cent[k][j] - cent["TTE"][j] for k in ks2]
    ax.plot(range(len(ks2)), vals, "o-", color=c0, ms=4, lw=1, label=f"TTE {lo} cm$^{{-1}}$")
ax.axhspan(-1.1, 1.1, color="#999", alpha=0.1); ax.axhline(0, color="#999", lw=0.6)
ax.set_xticks(range(len(ks2))); ax.set_xticklabels(names, fontsize=8); ax.set_ylim(-3, 3)
ax.set_ylabel("Δ centroid vs pure TTE (cm$^{-1}$)"); ax.legend(fontsize=7, frameon=False)
ax.set_title("(d) TTE bands unshifted\n(non-coordinating diluent)", loc="left", fontsize=10, fontweight="bold")
ax.text(0.5, 0.06, "grey band = ±1 pt (1.08 cm$^{-1}$)", transform=ax.transAxes, ha="center", fontsize=7, color="#666")

fig.suptitle("Raman decomposition: salt reshapes DMTFA bands, gelation does not — but TTE content differs between liquid and gels", fontsize=11.5, fontweight="bold")
fig.savefig("figures/Raman_Decomposition.png", facecolor="white"); fig.savefig("figures/Raman_Decomposition.svg", facecolor="white")
print("saved")

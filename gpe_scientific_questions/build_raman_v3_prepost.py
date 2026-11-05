"""Raman batch 3 (Raman20260914XY, 1200 gr, 2.44 cm-1 step): monomer, precursor (聚合前), gel (聚合后).
Checks: residual C=C (1634) before/after, monomer-specific bands, TTE ratio, solvation markers."""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import sparse; from scipy.sparse.linalg import spsolve; from scipy.optimize import nnls
def als(y, lam=1e5, p=0.005, n=10):
    L = len(y); D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2), format="csc"); w = np.ones(L)
    for _ in range(n):
        W = sparse.spdiags(w, 0, L, L, format="csc"); z = spsolve(W + lam * D.dot(D.T), w * y); w = p * (y > z) + (1 - p) * (y < z)
    return z
names = ["DMTFA", "TTE", "LE", "MBA_monomer", "PEGDA_monomer", "PMBA_precursor", "PMBA_gel", "PEGDA_precursor", "PEGDA_gel"]
R = {}
for n in names:
    x, y = np.loadtxt(f"data/Raman_v3/raw/{n}.txt", comments="#", encoding="latin-1").T; R[n] = y - als(y)
    np.savetxt(f"data/Raman_v3/processed/{n}_baseline_corrected.txt", np.c_[x, R[n]], fmt="%.3f", header="shift_cm-1\tintensity_ALS_corrected")
def A(y, lo, hi): w = (x > lo) & (x < hi); return np.trapezoid(np.clip(y[w], 0, None), x[w])
m = (x > 300) & (x < 1800)
rows = []
for n in ["LE", "PMBA_precursor", "PMBA_gel", "PEGDA_precursor", "PEGDA_gel"]:
    c, _ = nnls(np.c_[R["DMTFA"][m], R["TTE"][m]], R[n][m]); a = A(R[n], 1400, 1445)
    rows.append((n, A(R[n], 1615, 1650) / a, A(R[n], 1500, 1550) / a, A(R[n], 1650, 1750) / a, c[0] / c[1]))
with open("data/Raman_v3/processed/summary.txt", "w") as f:
    f.write("sample\tA(C=C 1615-1650)/A1430\tA1526/A1430\tA(C=O)/A1430\tDMTFA:TTE(a/b)\n")
    for r in rows: f.write(f"{r[0]}\t" + "\t".join(f"{v:.3f}" for v in r[1:]) + "\n"); print(r)
plt.rcParams.update({"font.size": 9.5})
fig, axs = plt.subplots(1, 3, figsize=(14, 4.6), dpi=220, gridspec_kw=dict(width_ratios=[1.2, 1, 0.8], wspace=0.28))
ax = axs[0]
for n, c, lab in [("LE", "k", "Liquid C0"), ("PMBA_precursor", "#E67E22", "MBA precursor (before curing)"), ("PMBA_gel", "#d62728", "PMBA gel (after curing)")]:
    w = (x > 1350) & (x < 1800); ax.plot(x[w], R[n][w] / A(R[n], 1400, 1445), color=c, lw=1.1, label=lab)
w = (x > 1350) & (x < 1800); ax.plot(x[w], R["MBA_monomer"][w] / R["MBA_monomer"][w].max() * 0.03, color="#8E44AD", lw=1, ls="--", label="MBA monomer (solid, scaled)")
ax.axvspan(1615, 1650, color="#999", alpha=0.1); ax.set_xlim(1350, 1800); ax.set_yticks([]); ax.set_xlabel("Raman shift (cm$^{-1}$)")
ax.set_title("(a) C=C 1634 not reduced after curing\n(probed spot)", loc="left", fontsize=9.5, fontweight="bold")
ax.legend(fontsize=7.5, frameon=False, loc="upper right", bbox_to_anchor=(1, 0.86)); ax.text(1700, 0.04, "← C=C 1634\n    + amide I 1666", fontsize=7.5)
ax = axs[1]
for n, c, lab in [("PMBA_gel", "#d62728", "PMBA gel"), ("MBA_monomer", "#8E44AD", "MBA monomer")]:
    w = (x > 850) & (x < 1350); ax.plot(x[w], R[n][w] / R[n][(x > 1230) & (x < 1260)].max(), color=c, lw=1.1, label=lab)
for v in (912, 1075, 1245, 1309): ax.axvline(v, color="#DDD", lw=0.8, zorder=0); ax.text(v, 1.05, str(v), ha="center", fontsize=7)
ax.set_xlim(850, 1350); ax.set_ylim(-0.1, 1.15); ax.set_yticks([]); ax.set_xlabel("Raman shift (cm$^{-1}$)"); ax.legend(fontsize=7.5, frameon=False)
ax.set_title("(b) Monomer-specific 912 / 1245 bands\nalso present in cured sample", loc="left", fontsize=9.5, fontweight="bold")
ax = axs[2]
labs = ["C0", "MBA\npre", "PMBA\ngel", "PEGDA\npre", "PEGDA\ngel"]; cols = ["k", "#E67E22", "#d62728", "#85C1E9", "#1f77b4"]
ax.bar(range(5), [r[1] for r in rows], color=cols)
for i, r in enumerate(rows): ax.text(i, r[1] + 0.01, f"{r[1]:.2f}", ha="center", fontsize=7.5)
ax.set_xticks(range(5)); ax.set_xticklabels(labs, fontsize=7.5); ax.set_ylabel("A(C=C 1615–1650) / A1430")
ax.set_title("(c) Residual C=C index\n", loc="left", fontsize=9.5, fontweight="bold")
fig.suptitle("Raman batch 3 (2026-09-14): precursor vs cured — heterogeneous white sample; single-spot spectra cannot give conversion", fontsize=10.5, fontweight="bold", y=1.04)
fig.savefig("figures/Raman_v3_prepost.png", bbox_inches="tight", facecolor="white"); fig.savefig("figures/Raman_v3_prepost.svg", bbox_inches="tight", facecolor="white")

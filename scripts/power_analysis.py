"""Power analýza pro hypotézy H1–H4 (kolik pacientů je potřeba).

Spuštění:  python scripts/power_analysis.py
Volitelně: python scripts/power_analysis.py --n-available 44 --power 0.8

Vše je na úrovni pacienta (jeden řádek = jeden pacient), protože report
i testy se dělají po pacientech (dohoda s vedoucím 10. 11. 2026).

Dva typy testů:
  * korelace (Spearman): spojitý marker, např. % plazmocytů v dřeni (H2),
    počet CTCs (H1, pokud bude číslo)
  * dvě skupiny (Mann–Whitney): marker ano/ne, např. paraskeletální ložisko (H3),
    vysoce riziková cytogenetika (H4), CTCs nad hranicí (H1)

Vzorce (normální aproximace, běžně v učebnicích):
  * korelace: Fisherova z-transformace, n = ((z_a + z_b) / atanh(r))^2 + 3;
    pro Spearmana se rozptyl násobí (1 + r^2 / 2) (Bonett & Wright 2000)
  * dvě skupiny: N = (z_a + z_b)^2 / (d^2 * p * (1 - p)), p = podíl menší skupiny;
    pro Mann–Whitney se dělí asymptotickou relativní eficiencí 0.864 (nejhorší případ
    pro spojitá rozdělení je 0.864, pro normální rozdělení 0.955)
  * více příznaků najednou: hladina alfa se dělí počtem testovaných příznaků
    (Bonferroni). Je to přísnější než FDR v pipeline, takže čísla jsou "na jistotu".
"""
import argparse
import math

from scipy.stats import norm

ARE_MANN_WHITNEY = 0.864


def z_sum(alpha, power):
    return norm.ppf(1 - alpha / 2) + norm.ppf(power)


def n_correlation(r, alpha=0.05, power=0.8, spearman=True):
    """Potřebný počet pacientů pro korelaci o síle r (oboustranný test)."""
    n = (z_sum(alpha, power) / math.atanh(abs(r))) ** 2
    if spearman:
        n *= 1 + r ** 2 / 2
    return math.ceil(n + 3)


def min_detectable_r(n, alpha=0.05, power=0.8, spearman=True):
    """Nejslabší korelace, kterou při n pacientech ještě spolehlivě zachytím."""
    lo, hi = 0.001, 0.999
    for _ in range(60):
        mid = (lo + hi) / 2
        if n_correlation(mid, alpha, power, spearman) > n:
            lo = mid
        else:
            hi = mid
    return hi


def n_two_groups(d, p_minor, alpha=0.05, power=0.8, mann_whitney=True):
    """Potřebný celkový počet pacientů pro rozdíl dvou skupin (Cohenovo d)."""
    n = z_sum(alpha, power) ** 2 / (d ** 2 * p_minor * (1 - p_minor))
    if mann_whitney:
        n /= ARE_MANN_WHITNEY
    return math.ceil(n)


def d_from_r(r):
    """Převod korelace na Cohenovo d (Cohen 1988), jen pro orientační srovnání."""
    return 2 * r / math.sqrt(1 - r ** 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n-available", type=int, nargs="*", default=[67, 48, 44],
                    help="dostupné počty pacientů (vše / 1. linie / 1. linie s %% plazmocytů)")
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--features", type=int, nargs="*", default=[1, 10, 30],
                    help="kolik příznaků testuji (1 = jeden předem vybraný)")
    args = ap.parse_args()
    pw = args.power

    print(f"Síla testu (power) = {pw}, alfa = 0.05 dělená počtem příznaků\n")

    print("KORELACE (H2, H1 jako číslo) – potřebný počet pacientů")
    scen = [(0.54, "Reinert 2021, difference entropy"),
            (0.49, "Reinert 2021, uniformity"),
            (0.50, "Rišian 2026, nejsilnější příznak vs. beta2M"),
            (0.30, "Rišian 2026, průměr vs. % plazmocytů"),
            (0.40, "střed")]
    print(f"{'r':>5} " + " ".join(f"{k:>4} příz." for k in args.features) + "  zdroj")
    for r, src in scen:
        row = " ".join(f"{n_correlation(r, 0.05 / k, pw):>9}" for k in args.features)
        print(f"{r:>5.2f} {row}  {src}")

    print("\nNejslabší zachytitelná korelace při dostupném počtu pacientů")
    for n in args.n_available:
        row = ", ".join(f"{k} příz.: |r| >= {min_detectable_r(n, 0.05 / k, pw):.2f}"
                        for k in args.features)
        print(f"  N = {n:>3}: {row}")

    print("\nDVĚ SKUPINY (H3 paraskelet., H4 cytogenetika, H1 CTCs nad hranicí)")
    print("potřebný CELKOVÝ počet pacientů, Mann–Whitney")
    print(f"{'d':>5} {'menší skup.':>11} " + " ".join(f"{k:>4} příz." for k in args.features))
    for d in (0.8, 1.1):
        for p in (0.15, 0.25, 0.40):
            row = " ".join(f"{n_two_groups(d, p, 0.05 / k, pw):>9}" for k in args.features)
            print(f"{d:>5.1f} {p:>10.0%} {row}")
    print(f"\n(pro srovnání: r = 0.49 odpovídá d = {d_from_r(0.49):.2f})")


if __name__ == "__main__":
    main()

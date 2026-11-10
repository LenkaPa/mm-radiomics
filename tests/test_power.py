import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "power_analysis", Path(__file__).parents[1] / "scripts" / "power_analysis.py")
pa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pa)


def test_pearson_textbook_value():
    # učebnicová hodnota: r = 0.3, alfa 0.05, power 0.8 -> 85 pacientů
    assert pa.n_correlation(0.3, spearman=False) == 85


def test_min_detectable_r_is_inverse():
    r = pa.min_detectable_r(44)
    assert pa.n_correlation(r) <= 44 < pa.n_correlation(r - 0.01)


def test_two_groups_equal_split():
    # d = 0.8, skupiny 50/50, t-test ~ 50 celkem; Mann–Whitney o něco víc
    assert 49 <= pa.n_two_groups(0.8, 0.5, mann_whitney=False) <= 52

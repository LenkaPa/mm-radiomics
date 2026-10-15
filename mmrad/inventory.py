"""Krok 1: najde vyšetření, spáruje masky (a později DICOM a kliniku)."""
from pathlib import Path


def find_mask_exams(masks_dir):
    """Vrátí {Myel_ID: (spine_mask, lesion_mask)} pro vyšetření, která mají obě masky."""
    exams = {}
    for spine in sorted(Path(masks_dir).rglob("*_spine_segmentation.nii.gz")):
        exam_id = spine.name.replace("_spine_segmentation.nii.gz", "")
        lesions = spine.with_name(f"{exam_id}_lesions_segmentation.nii.gz")
        if lesions.exists():
            exams[exam_id] = (spine, lesions)
    return exams


def select_patients(exams, patients):
    if patients in (None, "all"):
        return exams
    return {k: v for k, v in exams.items() if k in set(patients)}


def run(cfg, check_only=False):
    paths = cfg["paths"]
    exams = select_patients(find_mask_exams(paths["masks"]), cfg.get("patients", "all"))
    print(f"Nalezeno vyšetření s maskami: {len(exams)}")
    for name in ("images", "clinical"):
        if not Path(paths[name]).exists():
            print(f"VAROVÁNÍ: {name} ({paths[name]}) neexistuje")
    # TODO: najít DICOM série podle SeriesDescription, ověřit geometrii vůči maskám,
    #       napojit klinickou tabulku, uložit results/inventory.csv
    return exams

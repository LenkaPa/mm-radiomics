"""Krok 2: regiony zájmu – léze a zdravá kost."""
import numpy as np
from scipy import ndimage


def lesion_masks(lesion_labels, min_voxels=1):
    """Rozdělí masku lézí (každá léze má své ID) na {id: binární maska}."""
    out = {}
    for lesion_id in np.unique(lesion_labels):
        if lesion_id == 0:
            continue
        mask = lesion_labels == lesion_id
        if mask.sum() >= min_voxels:
            out[int(lesion_id)] = mask
    return out


def healthy_bone(spine_labels, lesion_labels, spacing_mm, dilation_mm=3.0, exclude_labels=()):
    """Zdravá kost = obratle minus léze dilatované o dilation_mm.

    spacing_mm je ve stejném pořadí os jako pole (z, y, x).
    """
    bone = (spine_labels > 0) & ~np.isin(spine_labels, list(exclude_labels))
    lesions = lesion_labels > 0
    if dilation_mm > 0 and lesions.any():
        # elipsoidní strukturní element podle velikosti voxelu
        radius = [max(1, int(round(dilation_mm / s))) for s in spacing_mm]
        grid = np.ogrid[tuple(slice(-r, r + 1) for r in radius)]
        element = sum((g * s / dilation_mm) ** 2 for g, s in zip(grid, spacing_mm)) <= 1
        lesions = ndimage.binary_dilation(lesions, structure=element)
    return bone & ~lesions

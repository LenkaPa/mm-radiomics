import numpy as np

from mmrad.roi import healthy_bone, lesion_masks


def test_healthy_bone_excludes_dilated_lesion():
    spine = np.ones((11, 11, 11), dtype=np.uint16)
    lesions = np.zeros_like(spine)
    lesions[5, 5, 5] = 1
    bone = healthy_bone(spine, lesions, spacing_mm=(1, 1, 1), dilation_mm=2)
    assert not bone[5, 5, 5]
    assert not bone[5, 5, 7]       # 2 mm od léze -> vyřazeno
    assert bone[5, 5, 8]           # 3 mm od léze -> zůstává
    assert bone[0, 0, 0]


def test_excluded_vertebra_removed():
    spine = np.zeros((4, 4, 4), dtype=np.uint16)
    spine[:2] = 20
    spine[2:] = 21
    bone = healthy_bone(spine, np.zeros_like(spine), (1, 1, 1), dilation_mm=0, exclude_labels=[21])
    assert bone[:2].all() and not bone[2:].any()


def test_lesion_masks_split_by_id():
    labels = np.zeros((5, 5, 5), dtype=np.uint16)
    labels[0, 0, 0] = 3
    labels[4, 4, 4] = 7
    masks = lesion_masks(labels)
    assert set(masks) == {3, 7}
    assert masks[3].sum() == 1

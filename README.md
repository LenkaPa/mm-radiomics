# mm-radiomics

Radiomic feature extraction pipeline for the Spinal-Multiple-Myeloma-SEG dataset (master's thesis, Brno University of Technology).

The pipeline extracts radiomic features from lesions and healthy vertebral bone in dual-energy CT
(virtual monoenergetic images at 40 keV and calcium-suppressed images), evaluates their robustness
and relates them to clinical markers of multiple myeloma. Results are summarised in an interactive HTML report.

> Work in progress.

## Data

Data are not part of this repository.

- Images and masks: Spinal-Multiple-Myeloma-SEG on TCIA, DOI [10.7937/k4qv-hh78](https://doi.org/10.7937/k4qv-hh78)
- Trabecular masks: Zenodo, DOI [10.5281/zenodo.21628232](https://doi.org/10.5281/zenodo.21628232)

Expected layout:

```
data/
├── dicom/   # DICOM series (searched recursively)
├── masks/   # MM_NIfTI_Segmentation/Myel_XXX/*.nii.gz
└── Spinal-Multiple-Myeloma-SEG_Table_clinical_data.tsv
```

## Installation

The code is plain Python and runs the same on macOS, Linux and Windows. Only the one-time setup differs.

### 1. Install Miniforge (conda)

Follow <https://github.com/conda-forge/miniforge>.

### 2. Install a C compiler (needed once to build PyRadiomics)

| System | What to do |
|---|---|
| macOS | in Terminal: `xcode-select --install` |
| Linux | usually already present; otherwise e.g. `sudo apt install build-essential` |
| Windows | install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with the *Desktop development with C++* workload |

### 3. Create the environment

Open a terminal (on Windows: *Miniforge Prompt* from the Start menu), go to the repository folder and run:

```bash
conda env create -f environment.yml
conda activate mmrad
```

After that, every command below is the same on all systems.

## Usage

```bash
python run.py --config config.yaml            # full run
python run.py --config config.yaml --check    # check inputs only
python run.py --config config.yaml --step report
```

All settings are in `config.yaml`. Outputs are written to `results/`.

## Tests

```bash
pytest
```

## Citation

If you use this code, please cite the dataset (Nohel et al., *Scientific Data*, 2026) and PyRadiomics
(van Griethuysen et al., *Cancer Research*, 2017).

## License

MIT

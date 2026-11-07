# Before AI tells patients what to eat, it needs to know where they live

Code and data for the preprint:

> Chitipolu SS. *Before AI tells patients what to eat, it needs to know where they live: a cross-sectional ecological study of diabetes and food access in California and Michigan census tracts, with a spotlight on Metro Detroit and Metro Los Angeles.* medRxiv, 2026 doi:[10.64898/2026.11.03.26367208](https://doi.org/10.64898/2026.11.03.26367208).

Author: Sri Sudheera Chitipolu, PhD student in Information Technology (Artificial Intelligence specialty), School of Computer and Information Sciences, University of the Cumberlands, Williamsburg, Kentucky, USA · ORCID [0009-0006-9665-6195](https://orcid.org/0009-0006-9665-6195)

**Code and data archive:** Zenodo v1.1, doi:[10.5281/zenodo.23889080](https://doi.org/10.5281/zenodo.23889080)

## What is in this repository

| Folder | Contents |
|---|---|
| `notebooks/01_double_burden.ipynb` | Aims 1 and 2: builds the tract dataset, double-burden counts, regression and spatial models, hidden food deserts, Figures 1–2 |
| `notebooks/02_ai_pilot.ipynb` | Aim 3: re-runs the AI-pilot scoring, Table 4, test, Figures 3–4, address check, and the USDA SNAP retailer check (section 6) |
| `data/clean/` | Tract-level analysis files (11,974 California and Michigan tracts) and the 20 AI-pilot tracts |
| `data/raw/` | Empty — see `data/raw/README.md` for download links to the public source files |
| `ai_pilot/` | The 60 chatbot answers (`P2_AI_Pilot_Answers.docx`), profiles and food-to-store table (`P2_AI_Pilot_Audit.xlsx`), scoring script (`score_pilot.py`), scores, address check files, SNAP retailer match (`snap_match.py`, `addresses_final_with_snap.csv`) and the full scoring log (`SCORING_LOG.md`) |
| `revision/` | v1.2 journal-revision analyses: six scripts and Supplementary Tables S1–S6 (`P2_Supplementary_Tables_S1-S6.xlsx` plus one CSV per table). See `revision/README.md` for what each script does and the run order |
| `figures/` | Figures 1–4 as used in the paper |

## How to reproduce

```bash
conda create -n diabetes-food --override-channels -c conda-forge python=3.11 pandas numpy scipy statsmodels geopandas libpysal esda spreg matplotlib openpyxl jupyterlab
conda activate diabetes-food
pip install python-docx
jupyter lab
```
1. Download the raw files listed in `data/raw/README.md` into `data/raw/`.
2. Run `notebooks/01_double_burden.ipynb` (Run All).
3. Run `notebooks/02_ai_pilot.ipynb` (Run All); it should print `scored 60`, and section 6 should print `Grocery stores named: 20 | found in SNAP list at that address: 20 | an active SNAP store at that address: 20` and `Verified 45 of 55 (82%) | problems 7 (13%) | unclear 3`.
4. Optional (journal revision, v1.2): run the scripts in `revision/` in the order given in `revision/README.md`. They read `data/clean/`, `data/raw/` and `ai_pilot/` from this repository and write their tables into `revision/`.

Versions used: Python 3.11.18, pandas 3.1.0, NumPy 2.4.6, SciPy 1.17.1, statsmodels 0.15.0, geopandas 1.2.0, libpysal 4.14.1, esda 2.9.0, spreg 1.9.0, matplotlib 3.11.2.

## Key definitions
- **Double burden:** tract diabetes prevalence (CDC PLACES 2025, crude) in the top 25% within its state **and** low income/low access on the USDA SNAP-authorized Retailer Access Map (2025), 1 mile urban / 10 miles rural.
- **Hidden food desert:** low access on the USDA Large Retailer Access Map (2019, large grocery stores only; 2010 tracts assigned to 2020 tracts by land area) but not on the SNAP-authorized map.
- **AI pilot:** 20 high-diabetes tracts (5 hidden + 5 comparison per metro, seed 2026); same synthetic person; ChatGPT, Gemini and Claude; Score A (healthy, ADA Standards of Care 2026) and Score B (share of foods sold at nearby store types). Rules and all changes are documented in `ai_pilot/SCORING_LOG.md`.

## Notes
- Chatbot answers were collected on October 28 and 30, 2026; chatbot outputs change over time.
- The food-to-store table is an assumption about what store types usually sell, not a shelf audit.
- Address check: Census geocoder, web listings, a 5-place hand check, and (for grocery stores) the USDA FNS SNAP Retailer Locator list. All 20 grocery stores named were active SNAP stores at the stated address; all 7 clear errors were food pantries or community programs.
- No human participants or private data were used.

## Versions
- v1.0 (Nov 2026): first release.
- v1.1 (Nov 2, 2026): adds the USDA SNAP retailer check (`ai_pilot/snap_match.py`, notebook 02 section 6), updated address codes (45/55 verified), table numbering matching the paper (AI pilot = Table 4), and author affiliation.
- v1.2 (Nov 2026): adds `revision/` with the journal-revision analyses and Supplementary Tables S1–S6 (2019–2025 large-store opening check, full regression and spatial diagnostics, Score B sensitivity, tract-level test of fresh-food share, all 55 chatbot-named places). No change to v1.1 data, notebooks or the medRxiv preprint results. See `CHANGELOG.md`.

## License
Code: MIT License. Data and text files created for this study: CC BY 4.0. Source data belong to their public providers (CDC, USDA ERS, USDA FNS, US Census Bureau, OMB).

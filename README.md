# Before AI tells patients what to eat, it needs to know where they live

Code and data for the preprint:

> Chitipolu SS. *Before AI tells patients what to eat, it needs to know where they live: a cross-sectional ecological study of diabetes and food access in California and Michigan census tracts, with a spotlight on Metro Detroit and Metro Los Angeles.* medRxiv, 2026 [link to be added].

Author: Sri Sudheera Chitipolu, PhD Candidate in AI, University of the Cumberlands · ORCID [0009-0006-9665-6195](https://orcid.org/0009-0006-9665-6195)

## What is in this repository

| Folder | Contents |
|---|---|
| `notebooks/01_double_burden.ipynb` | Aims 1 and 2: builds the tract dataset, double-burden counts, regression and spatial models, hidden food deserts, Figures 1–2 |
| `notebooks/02_ai_pilot.ipynb` | Aim 3: re-runs the AI-pilot scoring, Table 3, test, Figures 3–4, address check |
| `data/clean/` | Tract-level analysis files (11,974 California and Michigan tracts) and the 20 AI-pilot tracts |
| `data/raw/` | Empty — see `data/raw/README.md` for download links to the public source files |
| `ai_pilot/` | The 60 chatbot answers (`P2_AI_Pilot_Answers.docx`), profiles and food-to-store table (`P2_AI_Pilot_Audit.xlsx`), scoring script (`score_pilot.py`), scores, address check files and the full scoring log (`SCORING_LOG.md`) |
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
3. Run `notebooks/02_ai_pilot.ipynb` (Run All); it should print `scored 60`.

Versions used: Python 3.11.18, pandas 3.1.0, NumPy 2.4.6, SciPy 1.17.1, statsmodels 0.15.0, geopandas 1.2.0, libpysal 4.14.1, esda 2.9.0, spreg 1.9.0, matplotlib 3.11.2.

## Key definitions
- **Double burden:** tract diabetes prevalence (CDC PLACES 2025, crude) in the top 25% within its state **and** low income/low access on the USDA SNAP-authorized Retailer Access Map (2025), 1 mile urban / 10 miles rural.
- **Hidden food desert:** low access on the USDA Large Retailer Access Map (2019, large grocery stores only; 2010 tracts assigned to 2020 tracts by land area) but not on the SNAP-authorized map.
- **AI pilot:** 20 high-diabetes tracts (5 hidden + 5 comparison per metro, seed 2026); same synthetic person; ChatGPT, Gemini and Claude; Score A (healthy, ADA Standards of Care 2026) and Score B (share of foods sold at nearby store types). Rules and all changes are documented in `ai_pilot/SCORING_LOG.md`.

## Notes
- Chatbot answers were collected on October 28 and 30, 2026; chatbot outputs change over time.
- The food-to-store table is an assumption about what store types usually sell, not a shelf audit.
- No human participants or private data were used.

## License
Code: MIT License. Data and text files created for this study: CC BY 4.0. Source data belong to their public providers (CDC, USDA ERS, US Census Bureau, OMB).

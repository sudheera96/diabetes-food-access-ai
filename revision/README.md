# revision/ — journal-revision analyses (v1.2, November 2026)

These scripts and tables support the journal version of:
Chitipolu SS. Before AI tells patients what to eat, it needs to know where they live (medRxiv preprint
doi:10.64898/2026.11.03.26367208). The posted preprint is unchanged; these files add the checks made for journal review.

| Script | What it does | Output |
|---|---|---|
| s1_regression_table.py | Full OLS (HC1) and spatial lag (GM_Lag, spatially lagged X as instruments) results; Moran's I of residuals | S1_regression_table.csv, S1_model_fit.csv |
| ai_pilot_revision_checks.py | Score B sensitivity rules; fresh-food share tested at tract level (exact permutation + mixed model) | S3_scoreB_sensitivity.csv, S4_fresh_share_clustered_test.csv |
| detroit_store_opening_check.py | Large SNAP stores first authorized 2019–2025 within 1 mile of hidden tracts (tract edge); store mix near pilot tracts | S5_store_opening_check.csv, S5_new_large_stores_detail.csv, S6_pilot_tract_store_mix_1mi.csv |
| centroid_check.py | Same check from tract centroids; nearest large store for pilot tracts | S5b_store_opening_check_centroid.csv, S6b_pilot_nearest_large_store_2025.csv |
| reauth_check_and_workbook.py | Flags "new" stores at addresses already in the SNAP list (likely ownership change); builds the workbook | S5_new_large_stores_detail.csv (updated), workbook |
| truly_new_check.py | Repeats the opening check with truly new store addresses only | S5c_truly_new_stores_only.csv |

S2_all_55_named_places.csv lists all 55 places named by the chatbots with status and source.
P2_Supplementary_Tables_S1-S6.xlsx combines all tables (sheet "S5d" = new-store detail).

Run the scripts from inside this folder (`cd revision`), because they write their tables to the current folder and two of them load `detroit_store_opening_check.py` by name.

Run order: s1_regression_table.py → detroit_store_opening_check.py → centroid_check.py → ai_pilot_revision_checks.py → reauth_check_and_workbook.py (builds the workbook from all CSVs, so it must run after the others) → truly_new_check.py (adds sheet S5c).
S2_all_55_named_places.csv is an input (from the v1.1 address checks), not produced by these scripts; keep it in this folder.
Inputs: data/clean/ and data/raw/ as in v1.1 (USDA FNS Historical SNAP Retailer Locator 2005–2025; Census 2020 cartographic tract files).
ai_pilot_revision_checks.py reads the frozen scoring table (ai_pilot/score_pilot.py) and ai_pilot/scores.csv from v1.1; no setup needed.
Environment: Python 3.11, pandas, statsmodels, geopandas, libpysal, esda, spreg, scipy, openpyxl.

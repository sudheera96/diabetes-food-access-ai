# Supplementary Table S1: full OLS and spatial lag results (journal revision, Nov 5 2026).
# Reproduces notebook 01 cells 15-18 exactly, and reports every term.
import pandas as pd, numpy as np, geopandas as gpd, libpysal, esda, warnings
import statsmodels.formula.api as smf
from spreg import GM_Lag
from pathlib import Path
warnings.filterwarnings('ignore')
BASE = Path(__file__).resolve().parent.parent; RAW = BASE/'data'/'raw'; CLEAN = BASE/'data'/'clean'
df = pd.read_csv(CLEAN/'tracts_ca_mi.csv', dtype={'GEOID':str})
m = smf.ols('diab ~ lila_1_10 + pct_no_vehicle + C(area) + C(state)', data=df).fit(cov_type='HC1')
ci = m.conf_int()
ols = pd.DataFrame({'Model':'OLS (HC1 robust SE)','Term':m.params.index,'Coef':m.params,'SE':m.bse,
                    'CI_low':ci[0],'CI_high':ci[1],'p':m.pvalues})
tr = pd.concat([gpd.read_file(RAW/'cb_2020_06_tract_500k.zip'), gpd.read_file(RAW/'cb_2020_26_tract_500k.zip')])
g = tr[['GEOID','geometry']].merge(df.loc[m.resid.index].assign(resid=m.resid), on='GEOID')
w = libpysal.weights.Queen.from_dataframe(g, use_index=False); w.transform = 'r'
np.random.seed(2026)
mi = esda.Moran(g['resid'], w, permutations=999)
X = pd.get_dummies(g[['lila_1_10','pct_no_vehicle','area','state']], drop_first=True).astype(float)
lag = GM_Lag(g[['diab']].values, X.values, w=w, w_lags=1, name_y='diab', name_x=list(X.columns), robust='white')
b = lag.betas.flatten(); se = np.array(lag.std_err)
from scipy import stats
z = b/se
names = ['Intercept']+list(X.columns)+['rho (W_diab, neighbours)']
sl = pd.DataFrame({'Model':'Spatial lag, S2SLS (White robust SE)','Term':names,'Coef':b,'SE':se,
                   'CI_low':b-1.96*se,'CI_high':b+1.96*se,'p':2*(1-stats.norm.cdf(abs(z)))})
out = pd.concat([ols, sl]).round(4)
out.to_csv('S1_regression_table.csv', index=False)
fit = {'OLS_n':int(m.nobs),'OLS_R2':round(m.rsquared,4),'OLS_adjR2':round(m.rsquared_adj,4),'OLS_AIC':round(m.aic,1),
       'Moran_I_resid':round(mi.I,4),'Moran_p_sim':mi.p_sim,'Spatial_n':int(lag.n),
       'Spatial_pseudoR2':round(lag.pr2,4),'Spatial_pseudoR2_e':round(lag.pr2_e,4),
       'Islands_in_W':len(w.islands),'Mean_neighbours':round(w.mean_neighbors,2),
       'Instruments':'spatially lagged X (W*X), first-order (w_lags=1)'}
pd.Series(fit).to_csv('S1_model_fit.csv', header=['value'])
print(out.to_string()); print(pd.Series(fit).to_string())

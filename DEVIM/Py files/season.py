import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from dailygraph import daily_overdues 
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
from statsmodels.tsa.api import STL
from statsmodels.graphics.tsaplots import plot_acf
from pandas.plotting import lag_plot

decomposition = seasonal_decompose(daily_overdues, model='additive', period=30)#365
decomposition.plot()
# plt.show()


def seasonal_strength(series: pd.Series) -> float:
    # time series decomposition
    series_decomp = STL(series, period=30).fit()
    
    # variance of residuals + seasonality
    resid_seas_var = (series_decomp.resid + series_decomp.seasonal).var()
    # variance of residuals
    resid_var = series_decomp.resid.var()

    # seasonal strength
    result = 1 - (resid_var / resid_seas_var)

    return result

ans = seasonal_strength(daily_overdues)
print(ans)

series = daily_overdues

# Лаговый график для проверки сезонности с лагом 6 месяцев
plt.figure(figsize=(5, 5))
lag_plot(series, lag=30)
plt.title("Лаговый график (lag=6)")
plt.show()

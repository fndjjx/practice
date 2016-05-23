import statsmodels.api as sm
import numpy as np
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample


    

def arma(data,p,q,n):
    result = []
    for i in range(p):
        for j in range(q):
            try:
                arma_mod = sm.tsa.ARMA(data, (i,j)).fit()
                arma_predict = arma_mod.predict(n,dynamic=True)
                error = arma_predict - np.array(data[n:])
                error = sum(error**2)
                result.append((i,j,error))
            except:
                pass

    result.sort(key=lambda x:x[2])
    select_p = result[0][0]
    select_q = result[0][1]
    print result
    print select_p
    print select_q
    arma_mod = sm.tsa.ARMA(data, (select_p,select_q)).fit()

    params = arma_mod.params
    residuals = arma_mod.resid
    p = arma_mod.k_ar
    q = arma_mod.k_ma
    k_exog = arma_mod.k_exog
    k_trend = arma_mod.k_trend
    steps = 1
    result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=data, exog=None, start=len(data))
    return result[0]

if __name__=="__main__":
    data = [94.859145 ,46.860952 ,11.242657 ,-4.721209 ,-1.166825 ,16.185768 ,39.021942 ,59.449910 ,72.170164 ,75.376796 ,70.436470 ,60.731607 ,50.201830 ,42.076074 ,38.114345 ,38.454705 ,41.963875 ,46.869339 ,51.423303 ,54.399752 ,55.321720]
    data = data[:-1]
    print data[-1]
    r = arma(data,4,4,19)
    print "final"
    print r

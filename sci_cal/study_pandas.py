import pandas as pd
import numpy as np
import tushare as ts

def get_tushare_data(code):
    return ts.get_h_data(code)

def df_create_modify():
    df = pd.DataFrame([10,20,30,40],columns=['num'],index=['a','b','c','d'])

    print df
    print df.index
    print df.columns
    print df.ix[2]
    print df.ix[df.index[0:2]]
    print df.sum()
    print df.describe()
    print df.apply(lambda x:x**2)
    print df**2
    df["fl"] = (2.2,2,5.8,4)
    print df
    df['name'] = pd.DataFrame(['h','r','z','c'],index=['a','b','d','c'])
    print df
    df_tmp = df.append({'num':50,'fl':3.3,'name':'w'},ignore_index=True)
    print df
    print df_tmp
    df_tmp = df.append(pd.DataFrame({'num':50,'fl':3.3,'name':'w'},index=['z']))
    print df_tmp
    df_tmp = df.join(pd.DataFrame([12,4,6,88],index=['a','b','c','e'],columns=['tt']))
    print df_tmp
    df_tmp = df.join(pd.DataFrame([12,4,6,88],index=['a','b','c','e'],columns=['tt']),how='outer')
    print df_tmp
    print df[['num','fl']].mean()
    del df['fl']
    print df


def df_index():
    arr = np.array(np.random.randn(3,5))
    print arr
    df = pd.DataFrame(arr)
    print df
    df.columns = ['c1','c2','c3','c4','c5']
    print df
    print df['c1'][1]
    dates = pd.date_range('2015-1-1',periods=3,freq='M')
    print dates
    df.index = dates
    print df


def df_calc():
    arr = np.array(np.random.randn(3,5))
    print arr
    df = pd.DataFrame(arr)
    print df
    print df.mean(0)
    print df.mean(1)
    print df.cumsum(1)
    print np.exp(df)


def df_group():
    arr = np.array(np.random.randn(4,5))
    df = pd.DataFrame(arr)
    df.columns = ['c1','c2','c3','c4','c5']
    df = df.join(pd.DataFrame(['q1','q2','q1','q2'],index=[0,1,2,3],columns=['s']))
    print df
    group = df.groupby('s')
    print group.mean()



def df_ols():
    s1 = get_tushare_data('601601')
    s2 = get_tushare_data('000166')
    s1.columns = ['s1open','s1high','s1close','s1low','s1vol','s1amount']
    s2.columns = ['s2open','s2high','s2close','s2low','s2vol','s2amount']
    s = s1.join(s2,how='inner')
    s.fillna(method='ffill')
    s = s[['s1close','s2close']]
    s = np.log(s/s.shift(1))
    print s
    x = s['s1close']
    y = s['s2close']
    model = pd.ols(x=x,y=y)
    print model.beta
    print s.corr()
  
   








if __name__=="__main__":
    df_ols()



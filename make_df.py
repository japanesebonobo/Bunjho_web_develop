<<<<<<< HEAD
import asyncio
from pyppeteer import launch
import pandas as pd

def make_df(a,b,c):
        a_b=[0]*len(a)
        for i in range(len(a)):
            a_b[i]=a[i]
            a_b[i].append(b[i])
        df_ab=pd.DataFrame(a_b)
        df_c=pd.DataFrame(c)
        df=pd.merge(df_ab,df_c,right_index=True,left_index=True)
        df.columns=["code","type","faculty","teacher","place","units","url","people","A","B","C","D","F","other","mean"]
        return df
#






=======
import asyncio
from pyppeteer import launch
import pandas as pd

def make_df(a,b,c):
        a_b=[0]*len(a)
        for i in range(len(a)):
            a_b[i]=a[i]
            a_b[i].append(b[i])
        df_ab=pd.DataFrame(a_b)
        df_c=pd.DataFrame(c)
        df=pd.merge(df_ab,df_c,right_index=True,left_index=True)
        df.columns=["code","type","faculty","teacher","place","units","url","people","A","B","C","D","F","other","mean"]
        return df
>>>>>>> origin/master

<<<<<<< HEAD
import asyncio
from pyppeteer import launch
import pandas as pd

def my_make_pre_score(df):
        for i in range(len(df)-1,0,-1):
            try:
                spam=int(df[i])
                pre_score=[0]*8
                pre_score[0]=spam
                #print(i,df[i],spam)
                print("ok")
                for l in range(1,8):
                    pre_score[l]=float(df[i+l])
                return pre_score
            except:
                pass
        print("なし")
=======
import asyncio
from pyppeteer import launch
import pandas as pd

def my_make_pre_score(df):
        for i in range(len(df)-1,0,-1):
            try:
                spam=int(df[i])
                pre_score=[0]*8
                pre_score[0]=spam
                #print(i,df[i],spam)
                print("ok")
                for l in range(1,8):
                    pre_score[l]=float(df[i+l])
                return pre_score
            except:
                pass
        print("なし")
>>>>>>> origin/master
        return [None,None,None,None,None,None,None,None]
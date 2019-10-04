import asyncio
from pyppeteer import launch
import pandas as pd
import my_make_pre_score

def my_make_score(sd):
    #     my_score=[0]*len(scoreData)
    #     for i in range(len(scoreData)):
        bool_int=False
        bool_per=False
        bool_start=False
        bool_ins=False
        pre_score=[]
        cnt=0
        ins=0
        for i in range(len(sd)):
            if bool_int:
                if bool_per:
                    if bool_start:
                        pre_score.append(float(sd[i]))
                        cnt+=1
                        if cnt==7:
                            break
                    else:
                        try:
                            pre_score.append(int(sd[i]))
                            bool_start=True
                        except:
                            continue
                else:
                    if len(sd[i])!=0:
                        if sd[i][-1]=="%":
                            bool_per=True
            else:
                try:
                    if int(sd[i])==15:
                        bool_int=True
                except:
                    try:
                        spam=float(sd[i])
                        ins+=1
                    except:
                        if ins >=7:
                            bool_ins=True
                        ins=0
        if cnt==0:
            if bool_ins:
                pre_score=my_make_pre_score.my_make_pre_score(sd)
            else:
                pre_score=[None,None,None,None,None,None,None,None]
    #             print(f"""
    #             {i}個目
    #             bool_int : {bool_int}
    #             bool_per : {bool_per}
    #             bool_start : {bool_start}
    #             bool_ins : {bool_ins}
    #             """)
    #     my_score[i]=pre_score
        return pre_score
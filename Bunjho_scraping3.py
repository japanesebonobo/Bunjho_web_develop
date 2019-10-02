import asyncio
from pyppeteer import launch
import pandas as pd
import time

async def main():
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
        return [None,None,None,None,None,None,None,None]

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
                pre_score=my_make_pre_score(sd)
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

    """
    メインの処理
    """
    browser = await launch(autoClose=False,headless=False)

    page = await browser.newPage()
    await page.goto('https://syllabus.doshisha.ac.jp/')

    await page.select('select[name="select_bussinessyear"]', '2018')
    await page.select('select[name="subjectcd"]', '9')

    await asyncio.wait([
        page.click('input[value="検索/Search"]'),
        page.waitForNavigation(),
    ])

    subjectData = []
    linkData = []

    for i in range(20):
        await page.select('select[name="selectNum"]', str(i+1))
        await asyncio.wait([
            page.click('input[value="指定結果一覧/Specified page"]'),
            page.waitForNavigation(),
        ])
        bool_text=False
        subjectData_pre=[]
        for td in await page.querySelectorAll('body > table > tbody > tr > td > table > tbody > tr > td'):
            #print("-------------------------------------------")
            text = await page.evaluate('(e) => e.innerText',td)
            text = text.strip()
            #print(text)
            if bool_text:
                if len(str(text))>=3:
                    if str(text)[-2:]=="単位":
                        #print(1,text)
                        subjectData_pre.append(text)
                        bool_text=False
                        subjectData.append(subjectData_pre)
                        subjectData_pre=[]
                    else:
                        #print(2,text)
                        subjectData_pre.append(text)
                else:
                    #print(3,text)
                    subjectData_pre.append(text)
            else:
                if len(str(text))>=8:
                    try:
                        #print(4,text)
                        spam=int(str(text[:8]))
                        bool_text=True
                        subjectData_pre.append(text)
                    except:
                        #print(5,text)
                        continue
                else:
                    #print(6,text)
                    continue
        
        for a in await page.querySelectorAll('body > table > tbody > tr > td > table > tbody > tr > td > a[class="link03"]'):
            link = await page.evaluate('(e) => e.href',a)
            linkData.append(link)
            #print(link)
        

    # subjectData = pd.DataFrame(subjectData)
    # linkData = pd.DataFrame(linkData)
    #print(subjectData)
    #print(linkData)
    #subjectData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/subjectData.csv')
    #linkData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/linkData.csv')
    #print("中間")
    scoreData = [0]*len(linkData)
    cnt=0
    for i in linkData:
        await page.goto(i)
        sd=[]
        for td in await page.querySelectorAll('body > div > table > tbody > tr > td > table > tbody > tr > td'):
            #time.sleep(1)
            score = await page.evaluate('(e) => e.innerText',td)
            score = score.strip()
            sd.append(score)
            #print(score)
        #print(sd)
        scoreData[cnt]=my_make_score(sd)
        print(subjectData[cnt][2])
        print(scoreData[cnt])
        print("-----------------------------------------------------------------------")
        cnt+=1
        time.sleep(1)

    #scoreData = pd.DataFrame(scoreData)
    #print(scoreData)
    #scoreData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/scoreData.csv')
    print("succes")
    await browser.close()
    print("DataFrame作成")
    df=make_df(subjectData,linkData,scoreData)
    df.to_csv("scraping_doshisha.tsv",index=False,sep="\t")
    #return df

if __name__=='__main__':
    asyncio.run(main())
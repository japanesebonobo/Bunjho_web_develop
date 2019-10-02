import asyncio
from pyppeteer import launch
import pandas as pd
import time
import make_df
import my_make_score
import my_make_pre_score

async def main():

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
        scoreData[cnt]= my_make_score.my_make_score(sd)
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
    df.to_csv("scraping_doshisha.tsv",index=False,sep="\t")
    #return df

if __name__=='__main__':
    asyncio.run(main())
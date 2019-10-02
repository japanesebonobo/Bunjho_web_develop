import asyncio
from pyppeteer import launch
import pandas as pd
import time

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
        
        for td in await page.querySelectorAll('body > table > tbody > tr > td > table > tbody > tr > td'):
            # time.sleep(1)
            text = await page.evaluate('(e) => e.innerText',td)
            text = text.strip()
            subjectData.append(text)
            print(text)

        for a in await page.querySelectorAll('body > table > tbody > tr > td > table > tbody > tr > td > a[class="link03"]'):
            link = await page.evaluate('(e) => e.href',a)
            linkData.append(link)
            print(link)

    subjectData = pd.DataFrame(subjectData)
    linkData = pd.DataFrame(linkData)
    print(subjectData)
    print(linkData)
    subjectData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/subjectData.csv')
    linkData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/linkData.csv')

    scoreData = []

    for i, row in linkData.iterrows():
        await page.goto(str(row[0]))

        for td in await page.querySelectorAll('body > div > table > tbody > tr > td > table > tbody > tr > td'):
            time.sleep(1)
            score = await page.evaluate('(e) => e.innerText',td)
            score = score.strip()
            scoreData.append(score)
            print(score)
        time.sleep(0.1)

    scoreData = pd.DataFrame(scoreData)
    print(scoreData)
    scoreData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/scoreData.csv')

    await browser.close()

if __name__=='__main__':
    asyncio.run(main())

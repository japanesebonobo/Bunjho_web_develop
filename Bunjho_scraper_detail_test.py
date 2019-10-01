import asyncio
from pyppeteer import launch
import pandas as pd
import time

async def main():
    browser = await launch(autoClose=False,headless=False,args=['--no-sandbox'])
    page = await browser.newPage()

    linkData = pd.read_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/linkData.csv',usecols=[1])
    scoreData = []

    for i, row in linkData.iterrows():
        await page.goto(str(row[0]))

        for td in await page.querySelectorAll('body > div > table > tbody > tr > td > table > tbody > tr > td'):
            time.sleep(1)
            score = await page.evaluate('(e) => e.innerText',td)
            score = score.strip()
            scoreData.append(score)
            print(score)
        time.sleep(1)

    await browser.close()


if __name__=='__main__':
    asyncio.run(main())
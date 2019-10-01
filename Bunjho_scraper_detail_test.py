import asyncio
from pyppeteer import launch
import pandas as pd
import time

async def main():
    browser = await launch(autoClose=False,headless=False,args=['--no-sandbox'])
    page = await browser.newPage()

    linkData = pd.read_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/linkData.csv',usecols=[1])
    print(linkData)

    for i, row in linkData.iterrows():
        await page.
        goto(str(row[0]))
        time.sleep(1)

    await browser.close()


if __name__=='__main__':
    asyncio.run(main())
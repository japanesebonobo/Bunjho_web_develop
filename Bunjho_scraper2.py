import asyncio
from pyppeteer import launch
import pandas as pd
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

async def main():
    """
    メインの処理
    """
    browser = await launch(autoClose=False,headless=False)

    page = await browser.newPage()
    await page.goto('https://syllabus.doshisha.ac.jp/')

    await page.select('select[name="select_bussinessyear"]', '2018')
    await page.select('select[name="subjectcd"]', '9')
    # await input_element.type('Python')

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

    # await page.screenshot({'path':'search_results.png'})

    # assert 'Python' in (await page.title())

    # await page.screenshot({'path':'search_results.png'})

    # for h3 in await page.querySelectorAll('a > h3'):
    #     text = await page.evaluate('(e) => e.textContent',h3)
    #     print(text)
    #     a = await page.evaluateHandle('(e) => e.parentElement',h3)
    #     url = await page.evaluate('(e) => e.href',a)
    #     print(url)

    await browser.close()

if __name__=='__main__':
    asyncio.run(main())

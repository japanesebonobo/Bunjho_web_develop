import asyncio
from pyppeteer import launch

async def main():
    """
    メインの処理
    """
    browser = await launch()

    page = await browser.newPage()
    await page.goto('https://syllabus.doshisha.ac.jp/')

    await page.select('select[name="select_bussinessyear"]', '2018')
    await page.select('select[name="subjectcd"]', '9')
    # await input_element.type('Python')

    await asyncio.wait([
        page.click('input[value="検索/Search"]'),
        page.waitForNavigation(),
    ])

    await page.screenshot({'path':'search_results.png'})

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

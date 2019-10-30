import logging
from typing import List
import time

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.common.exceptions import NoSuchElementException

def main():
    """
    メインの処理
    """
    options = ChromeOptions()
    driver = Chrome(options=options,executable_path='/Users/yoshitomiyuuta/Bunjho_web_develop/chromedriver')

    navigate(driver)
    contents = scrape_contents(driver)
    logging.info(f'Found{len(contents)}contents.')

    for content in contents:
        print(content)

    driver.quit()

def navigate(driver: Remote):
    """
    目的のページに遷移する。
    """
    logging.info('Navigating...')
    driver.get('https://note.mu/')
    assert 'note' in driver.title

    for _ in range(3):
        driver.execute_script('scroll(0,document.body.scrollHeight)')
        logging.info('Waiting for contents to be loaded...')
        time.sleep(2)

def scrape_contents(driver: Remote) -> List[dict]:
    """
    文章コンテンツのURL、タイトル、概要、スキの数を含むdictのリストを取得する。
    """
    contents = []

    for div in driver.find_elements_by_css_selector('.o-timeline__item'):
        a = div.find_element_by_css_selector('a')
        try:
            description = div.find_element_by_css_selector('p').text
        except NoSuchElementException:
            description = ''

        contents.append({
            'url': a.get_attribute('href'),
            'title':div.find_element_by_css_selector('h3').text,
            'description':description,
            'like':int(div.find_element_by_css_selector('.o-noteStatus__item--like .o-noteStatus__label').text),
        })

    return contents

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

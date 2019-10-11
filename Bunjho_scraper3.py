import asyncio
from pyppeteer import launch
import pandas as pd
import time
import make_df
import my_make_score
import my_make_pre_score
import sqlalchemy as sa
import MySQLdb

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

    subjectData = pd.DataFrame(subjectData)
    linkData = pd.DataFrame(linkData)
    scoreData = pd.DataFrame(scoreData)
    #print(scoreData)
    #scoreData.to_csv('/Users/yoshitomiyuuta/Bunjho_web_develop/scoreData.csv')

    print("succes")
    await browser.close()

    print("DataFrame作成")
    url = 'mysql+pymysql://root:@localhost/bunjho_web_database?charset=utf8mb4'
    engine = sa.create_engine(url, echo=True)

    df1 = pd.concat([subjectData,linkData],axis=1)
    df2 = pd.concat([df1,scoreData],axis=1)
    print(df1)
    print(df2)
    df2 = pd.DataFrame(df2)
    linkData.to_sql('linkData', engine, index=True, if_exists='replace')
    subjectData.to_sql('subjectData', engine, index=True, if_exists='replace')
    scoreData.to_sql('scoreData', engine, index=True, if_exists='replace')

    db_config = {
    'host': 'localhost',
    'db': 'bunjho_web_database',  # Database Name
    'user': 'root',
    'charset': 'utf8mb4',
    }
 
    try:
        # 接続
        conn = MySQLdb.connect(host=db_config['host'], db=db_config['db'], user=db_config['user'], charset=db_config['charset'])
    except MySQLdb.Error as ex:
        print('MySQL Error: ', ex)

    cursor = conn.cursor()
 
    # テーブルが存在する場合には削除
    cursor.execute('DROP TABLE IF EXISTS `AllSubjectData`')
    
    # 各テーブルの列名を設定
    cursor.execute('''ALTER TABLE `subjectData`
        CHANGE COLUMN `index` `subjectData_index` int,
        CHANGE COLUMN `0` `subjectNo` text,
        CHANGE COLUMN `1` `faculty` text,
        CHANGE COLUMN `2` `subjectName` text,
        CHANGE COLUMN `3` `teacher` text,
        CHANGE COLUMN `4` `place` text,
        CHANGE COLUMN `5` `units` text
    ''')

    cursor.execute('''ALTER TABLE `linkData`
        CHANGE COLUMN `index` `linkData_index` int,
        CHANGE COLUMN `0` `link` text
    ''')

    cursor.execute('''ALTER TABLE `scoreData`
        CHANGE COLUMN `index` `scoreData_index` int,
        CHANGE COLUMN `0` `member` int,
        CHANGE COLUMN `1` `A` float,
        CHANGE COLUMN `2` `B` float,
        CHANGE COLUMN `3` `C` float,
        CHANGE COLUMN `4` `D` float,
        CHANGE COLUMN `5` `F` float,
        CHANGE COLUMN `6` `other` int,
        CHANGE COLUMN `7` `averageGPA` float
    ''')

    cursor.execute('''ALTER TABLE `linkData`
        CHANGE COLUMN `index` `linkData_index` int,
        CHANGE COLUMN `0` `link` text
    ''')

    # AllSubjectDataテーブルの作成 
    cursor.execute('''CREATE TABLE AllSubjectData
    SELECT *
    FROM subjectData
    JOIN scoreData
    ON
    subjectData.subjectData_index = scoreData.scoreData_index
    JOIN linkData
    ON
    scoreData.scoreData_index = linkData.linkData_index''')
    print('Create Table successful.')

    #科目名の英語削除
    cursor.execute('''UPDATE AllSubjectData SET AllSubjectData.subjectName = SUBSTRING(subjectName, 1, INSTR(subjectName,'\n')) 
    WHERE AllSubjectData.subjectNo = AllSubjectData.subjectNo
    ''')

if __name__=='__main__':
    asyncio.run(main())
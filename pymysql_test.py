import MySQLdb

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

# それぞれのテーブルの列名を設定
cursor.execute('''ALTER TABLE `subjectData`
    CHANGE COLUMN `index` `subjectData_index` int,
    CHANGE COLUMN `0` `subjectNo` text,
    CHANGE COLUMN `1` `faculty` text,
    CHANGE COLUMN `2` `subjectName` text,
    CHANGE COLUMN `3` `teacher` text,
    CHANGE COLUMN `4` `place` text,
    CHANGE COLUMN `5` `units` text
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
    scoreData.scoreData_index = linkData.linkData_index
''')

print('Create Table successful.')

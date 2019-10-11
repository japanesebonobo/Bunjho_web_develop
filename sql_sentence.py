import MySQLdb

def my_sql_sentence(cursor):
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

    #科目名の英語削除
    cursor.execute('''UPDATE AllSubjectData SET AllSubjectData.subjectName = SUBSTRING(subjectName, 1, INSTR(subjectName,'\n')) 
    WHERE AllSubjectData.subjectNo = AllSubjectData.subjectNo
    ''')

    #科目名の重複削除
    cursor.execute('''DELETE FROM AllSubjectData 
    WHERE subjectNo NOT IN (SELECT min_subjectNo FROM (SELECT MIN(subjectNo) min_subjectNo FROM AllSubjectData GROUP BY subjectName) tmp)
    ''')

    #科目名の記号削除
    cursor.execute('''UPDATE AllSubjectData SET subjectName = REPLACE(subjectName, '○', '')''')
    cursor.execute('''UPDATE AllSubjectData SET subjectName = REPLACE(subjectName, '△', '')''')
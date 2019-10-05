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
cursor.execute('DROP TABLE IF EXISTS `students`')

# テーブルの作成 
cursor.execute('''CREATE TABLE IF NOT EXISTS `students` (
    `id` int(11) NOT NULL,
    `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci''')
print('Create Table successful.')

<<<<<<< HEAD
import pandas as pd
import sqlalchemy as sa

df = pd.DataFrame({'point': [100]})
print(df)
url = 'mysql+pymysql://root:@localhost/test_db?charset=utf8'
engine = sa.create_engine(url, echo=True)

=======
import pandas as pd
import sqlalchemy as sa

df = pd.DataFrame({'point': [100]})
print(df)
url = 'mysql+pymysql://root:@localhost/test_db?charset=utf8'
engine = sa.create_engine(url, echo=True)

>>>>>>> origin/master
df.to_sql('test1', engine, index=False, if_existcs='append')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

data = {
    'name': 'mysql+pymysql',
    'user': 'admin',
    'pwd': 'apzk1234',
    'host': 'database-1.crjx3ubi7qng.ap-northeast-2.rds.amazonaws.com',
    'port': '3306',
    'feat_db': 'featdb',
    'user_db': 'userdb'
}

feat_db_conn_string = f'{data["name"]}://' \
               f'{data["user"]}:{data["pwd"]}' \
               f'@{data["host"]}:{data["port"]}' \
               f'/{data["feat_db"]}' \
               f'?charset=utf8'

user_db_conn_string = f'{data["name"]}://' \
               f'{data["user"]}:{data["pwd"]}' \
               f'@{data["host"]}:{data["port"]}' \
               f'/{data["user_db"]}' \
               f'?charset=utf8'

class engine_feat_db_conn:

    def __init__(self):
        self.engine = create_engine(feat_db_conn_string, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

class engine_user_db_conn:

    def __init__(self):
        self.engine = create_engine(user_db_conn_string, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

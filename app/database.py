from sqlmodel import create_engine, Session

# データベースのファイル名（このファイルにデータが保存されます）
sqlite_file_name = "shift_sim.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# エンジン（DBと通信するための機能）の作成
# echo=True にすると、裏で実行されているSQL文がターミナルに表示されて学習に便利です
engine = create_engine(
    sqlite_url, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

# 各APIでデータベースを操作するためのセッション（窓口）を用意する関数
def get_session():
    with Session(engine) as session:
        yield session
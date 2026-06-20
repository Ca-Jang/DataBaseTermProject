import duckdb
import pandas as pd
from . import Interfaces as i

class HeroRepository(i.IHeroRepository):

    def __init__(self, db_path : str):
        self.db_path = db_path

    def create_table(self) : 
        """테이블 만들기"""
        with duckdb.connect(self.db_path) as con :
            con.execute("""
            -- auto increment 를 위한 SEQUENCE 생성
            CREATE SEQUENCE IF NOT EXISTS seq_hero_id START 1;
                       
                -- hero 테이블
                -- 영웅의 기본 정보 저장
                CREATE TABLE IF NOT EXISTS hero (
                    hero_id INT DEFAULT nextval('seq_hero_id') NOT NULL,
                    name VARCHAR NOT NULL,
                    role VARCHAR NOT NULL,
                    subrole VARCHAR NOT NULL,
                    health INT NULL,
                    armor INT NULL,
                    shields INT NULL,
                    portrait_url VARCHAR NULL,
                    PRIMARY KEY (hero_id)
                );
            """)

    def reset_table_and_sequence(self):
        """테이블 초기화 및 시퀀스 재설정 (테스트 용)"""
        with duckdb.connect(self.db_path) as con:
            con.execute("DELETE FROM hero")
            con.execute("DROP SEQUENCE IF EXISTS seq_hero_id")
            con.execute("CREATE SEQUENCE seq_hero_id START 1")

    def insert_batch(self, df: pd.DataFrame):
        """일괄 영웅 삽입"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_all_heroes', df)
            con.execute("""
                INSERT INTO hero (name, role, subrole, health, armor, shields, portrait_url)
                SELECT name, role, subrole, health, armor, shields, portrait_url FROM v_all_heroes
            """)

    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """영웅 삽입"""
        with duckdb.connect(self.db_path) as con :
            con.register('v_input', row)
            result_df = con.execute("""
                INSERT INTO hero (name, role, subrole, health, armor, shields)
                SELECT name, role, subrole, health, armor, shields FROM v_input
                RETURNING *;
            """).df()
            return result_df

    def find_by_id(self, hero_id: int) -> pd.DataFrame:
        """hero_id으로 영웅 조회"""
        with duckdb.connect(self.db_path) as con :
            return con.execute("""SELECT * FROM hero
                              WHERE hero_id = ?""", [hero_id]).df()
        
    def find_heroes_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        """키워드가 있으면 해당 영웅 검색, 키워드 없으면 전체 영웅 반환"""
        with duckdb.connect(self.db_path) as con:
            if keyword:
                query = "SELECT name, role, subrole, portrait_url FROM hero WHERE name LIKE ?"
                return con.execute(query, [f"%{keyword}%"]).df()
            else:
                query = "SELECT name, role, subrole, portrait_url FROM hero"
                return con.execute(query).df()

    def find_all(self) -> pd.DataFrame:
        """모든 영웅 반환"""
        with duckdb.connect(self.db_path) as con :
            return con.execute("SELECT * FROM hero").df()

    def update(self, row: pd.DataFrame) -> bool:
        """영웅 정보 수정"""
        if row.empty or 'hero_id' not in row.columns :
            return False
        
        try :
            with duckdb.connect(self.db_path) as con :
                con.register('v_update', row)
                con.execute("""
                            UPDATE hero
                            SET name = v.name,
                            role = v.role,
                            subrole = v.subrole,
                            health = v.health,
                            armor = v.armor,
                            shields = v.shields
                            FROM v_update v
                            WHERE hero.hero_id = v.hero_id;
                            """)
                return True
        except Exception as e:
            print(f"Hero Update Error : {e}")
            return False

    def delete(self, hero_id: int) -> bool:
        """영웅 삭제"""
        try:
            with duckdb.connect(self.db_path) as con:
                con.execute("DELETE FROM hero WHERE hero_id = ?", [hero_id])
            return True
        except Exception as e:
            print(f"Hero Delete Error {e}")
            return False
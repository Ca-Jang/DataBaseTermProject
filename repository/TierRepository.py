import duckdb
import pandas as pd
from . import Interfaces as i

class TierRepository(i.ITierRepository):
    def __init__(self, db_path : str):
        self.db_path = db_path

    def create_table(self):
        """테이블 만들기"""
        with duckdb.connect(self.db_path) as con:
            con.execute("""
                -- auto increment 를 위한 SEQUENCE 생성
                CREATE SEQUENCE IF NOT EXISTS seq_tier_id START 1;
                
                -- tier 테이블
                -- 티어 정보 저장
                CREATE TABLE IF NOT EXISTS tier (
                    tier_id INT DEFAULT nextval('seq_tier_id') NOT NULL,
                    tier_name VARCHAR NOT NULL,
                    tier_order INT NOT NULL,
                    icon_url VARCHAR NULL,
                    PRIMARY KEY (tier_id)
                );
            """)

    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """티어 삽입"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_input', row)
            result_df = con.execute("""
                INSERT INTO tier (tier_name, tier_order, icon_url)
                SELECT tier_name, tier_order, icon_url FROM v_input
                RETURNING *;
            """).df()
            return result_df

    def find_by_id(self, tier_id: int) -> pd.DataFrame:
        """tier_id로 티어 조회"""
        with duckdb.connect(self.db_path) as con:
            return con.execute("SELECT * FROM tier WHERE tier_id = ?", [tier_id]).df()

    def find_all(self) -> pd.DataFrame:
        """모든 티어를 tier_order 오름차순으로 반환"""
        with duckdb.connect(self.db_path) as con:
            # 요구사항에 맞게 tier_order를 기준으로 오름차순(ASC) 정렬합니다.
            return con.execute("SELECT * FROM tier ORDER BY tier_order ASC").df()

    def update(self, row: pd.DataFrame) -> bool:
        """티어 정보 수정"""
        if row.empty or 'tier_id' not in row.columns:
            return False
            
        try:
            with duckdb.connect(self.db_path) as con:
                con.register('v_update', row)
                con.execute("""
                    UPDATE tier
                    SET tier_name = v.tier_name,
                        tier_order = v.tier_order
                        icon_url = v.icon_url
                    FROM v_update v
                    WHERE tier.tier_id = v.tier_id;
                """)
            return True
        except Exception as e:
            print(f"Tier Update Error {e}")
            return False

    def delete(self, tier_id: int) -> bool:
        """티어 삭제"""
        try:
            with duckdb.connect(self.db_path) as con:
                con.execute("DELETE FROM tier WHERE tier_id = ?", [tier_id])
            return True
        except Exception as e:
            print(f"Tier Delete Error {e}")
            return False
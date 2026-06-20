import duckdb
import pandas as pd
from . import Interfaces as i

class PerkRepository(i.IPerkRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_table(self):
        """테이블 만들기"""
        with duckdb.connect(self.db_path) as con:
            con.execute("""
                -- perk 테이블
                -- 각 영웅의 특전 저장
                CREATE TABLE IF NOT EXISTS perk (
                    perk_id INT NOT NULL,
                    hero_id INT NOT NULL,
                    perk_name VARCHAR NOT NULL,
                    perk_type VARCHAR NOT NULL,
                    description VARCHAR NOT NULL,
                    icon_url VARCHAR NULL,
                    PRIMARY KEY (perk_id, hero_id),
                    CONSTRAINT FK_hero_TO_perk FOREIGN KEY (hero_id) REFERENCES hero (hero_id)
                );
            """)

    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """특전 삽입"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_input', row)
            
            result_df = con.execute("""
                INSERT INTO perk (perk_id, hero_id, perk_name, perk_type, description, icon_url)
                    SELECT perk_id, hero_id, perk_name, perk_type, description, icon_url FROM v_input
                    RETURNING *;
            """).df()
            return result_df

    def find_by_hero(self, hero_id: int) -> pd.DataFrame:
        """hero_id에 해당하는 모든 특전 반환"""
        with duckdb.connect(self.db_path) as con:
            return con.execute("""
                SELECT * FROM perk 
                    WHERE hero_id = ? 
                    ORDER BY perk_id ASC
            """, [hero_id]).df()

    def update(self, row: pd.DataFrame) -> bool:
        """특전 정보 수정"""
        if row.empty or 'perk_id' not in row.columns or 'hero_id' not in row.columns:
            return False
            
        try:
            with duckdb.connect(self.db_path) as con:
                con.register('v_update', row)
                # WHERE 절에 복합키 두 개를 모두 명시하여 정확한 행만 업데이트합니다.
                con.execute("""
                    UPDATE perk
                    SET perk_name = v.perk_name,
                        perk_type = v.perk_type,
                        description = v.description,
                        icon_url = v.icon_url
                    FROM v_update v
                    WHERE perk.perk_id = v.perk_id 
                      AND perk.hero_id = v.hero_id;
                """)
            return True
        except Exception as e:
            print(f"Perk Update Error {e}")
            return False

    def delete(self, perk_id: int, hero_id: int) -> bool:
        """(perk_id, hero_id) 복합키로 특전 삭제"""
        try:
            with duckdb.connect(self.db_path) as con:
                con.execute("""
                    DELETE FROM perk 
                    WHERE perk_id = ? AND hero_id = ?
                """, [perk_id, hero_id])
            return True
        except Exception as e:
            print(f"Perk Delete Error {e}")
            return False
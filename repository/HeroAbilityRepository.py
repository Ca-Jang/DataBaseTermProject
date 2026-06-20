import duckdb
import pandas as pd
from . import Interfaces as i

class HeroAbilityRepository(i.IHeroAbilityRepository):

    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_table(self):
        """테이블 만들기"""
        with duckdb.connect(self.db_path) as con:
            con.execute("""
                -- hero_abilities 테이블
                -- 영웅의 상세 정보 저장
                CREATE TABLE IF NOT EXISTS hero_abilities (
                    skill_id INT NOT NULL,
                    hero_id INT NOT NULL,
                    skill_name VARCHAR NULL,
                    description VARCHAR NULL,
                    icon_url VARCHAR NULL,
                    PRIMARY KEY (skill_id, hero_id),
                    CONSTRAINT FK_hero_TO_hero_abilities FOREIGN KEY (hero_id) REFERENCES hero (hero_id)
                );
            """)

    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """스킬 삽입"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_input', row)
            result_df = con.execute("""
                INSERT INTO hero_abilities (skill_id, hero_id, skill_name, description, icon_url)
                SELECT skill_id, hero_id, skill_name, description, icon_url FROM v_input
                RETURNING *;
            """).df()
            return result_df

    def find_by_hero(self, hero_id: int) -> pd.DataFrame:
        """hero_id에 해당하는 모든 스킬 반환"""
        with duckdb.connect(self.db_path) as con:
            return con.execute("""
                SELECT * FROM hero_abilities 
                WHERE hero_id = ? 
                ORDER BY skill_id ASC
            """, [hero_id]).df()

    def update(self, row: pd.DataFrame) -> bool:
        """스킬 정보 수정"""
        if row.empty or 'skill_id' not in row.columns or 'hero_id' not in row.columns:
            return False
            
        try:
            with duckdb.connect(self.db_path) as con:
                con.register('v_update', row)
                con.execute("""
                    UPDATE hero_abilities
                    SET skill_name = v.skill_name,
                        description = v.description,
                        icon_url = v.icon_url
                    FROM v_update v
                    WHERE hero_abilities.skill_id = v.skill_id 
                        AND hero_abilities.hero_id = v.hero_id;
                """)
            return True
        except Exception as e:
            print(f"Ability Update Error {e}")
            return False

    def delete(self, skill_id: int, hero_id: int) -> bool:
        """(skill_id, hero_id) 복합키로 스킬 삭제."""
        try:
            with duckdb.connect(self.db_path) as con:
                con.execute("""
                    DELETE FROM hero_abilities 
                    WHERE skill_id = ? AND hero_id = ?
                """, [skill_id, hero_id])
            return True
        except Exception as e:
            print(f"Ability Delete Error {e}")
            return False
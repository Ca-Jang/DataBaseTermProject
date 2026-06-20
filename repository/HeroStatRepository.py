import duckdb
import pandas as pd
from . import Interfaces as i

class HeroStatRepository(i.IHeroStatRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_table(self):
        """테이블 만들기"""
        with duckdb.connect(self.db_path) as con:
            # 3개의 외래키를 참조하며, 어느 하나라도 삭제되면 통계도 같이 날아가도록 CASCADE를 걸어줍니다.
            con.execute("""
                -- hero_stat 테이블
                -- 각 영웅의 맵, 티어별 승률, 픽률, 밴률 저장
                CREATE TABLE IF NOT EXISTS hero_stat (
                    hero_id INT NOT NULL,
                    map_id INT NOT NULL,
                    tier_id INT NOT NULL,
                    winrate DOUBLE NOT NULL DEFAULT 0.0,
                    pickrate DOUBLE NOT NULL DEFAULT 0.0,
                    banrate DOUBLE NOT NULL DEFAULT 0.0,
                    PRIMARY KEY (hero_id, map_id, tier_id),
                    CONSTRAINT FK_hero_TO_hero_stat FOREIGN KEY (hero_id) REFERENCES hero (hero_id),
                    CONSTRAINT FK_map_TO_hero_stat FOREIGN KEY (map_id) REFERENCES map (map_id),
                    CONSTRAINT FK_tier_TO_hero_stat FOREIGN KEY (tier_id) REFERENCES tier (tier_id)
                );
            """)
        
    def insert_batch(self, df: pd.DataFrame):
        """데이터프레임을 통한 일괄 통계 삽입"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_stats', df)
            con.execute("""
                INSERT INTO hero_stat (hero_id, map_id, tier_id, winrate, pickrate, banrate)
                SELECT hero_id, map_id, tier_id, winrate, pickrate, banrate FROM v_stats
            """)

    def find_by_hero(self, hero_id: int) -> pd.DataFrame:
        """특정 영웅의 모든 맵, 티어 통계 반환"""
        with duckdb.connect(self.db_path) as con:
            return con.execute("""
                SELECT * FROM hero_stat 
                WHERE hero_id = ?
            """, [hero_id]).df()

    def delete(self, hero_id: int, map_id: int, tier_id: int) -> bool:
        """(hero_id, map_id, tier_id) 복합키로 통계 삭제"""
        try:
            with duckdb.connect(self.db_path) as con:
                con.execute("""
                    DELETE FROM hero_stat 
                    WHERE hero_id = ? 
                      AND map_id = ? 
                      AND tier_id = ?
                """, [hero_id, map_id, tier_id])
            return True
        except Exception as e:
            print(f"Stat Delete Error {e}")
            return False
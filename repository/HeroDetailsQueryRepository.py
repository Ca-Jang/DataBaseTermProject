import duckdb
import pandas as pd
from . import Interfaces as i

class HeroDetailsQueryRepository(i.IHeroDetailsQueryRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

        # {'키': 값} 구조체, LIST() 함수 사용
        self.base_query = """
            WITH skill_agg AS (
                SELECT 
                    hero_id, 
                    LIST({'skill_name': skill_name, 'description': description, 'icon_url': icon_url}) AS skills
                FROM hero_abilities 
                GROUP BY hero_id
            ),
            perk_agg AS (
                SELECT 
                    hero_id, 
                    LIST({'perk_name': perk_name, 'perk_type': perk_type, 'description': description, 'icon_url': icon_url}) AS perks
                FROM perk 
                GROUP BY hero_id
            )
            SELECT 
                h.name AS hero_name, 
                h.role, 
                h.subrole, 
                h.health, 
                h.armor, 
                h.shields,
                portrait_url,
                s.skills AS skills,
                p.perks AS perks
            FROM hero h
            LEFT JOIN skill_agg s ON h.hero_id = s.hero_id
            LEFT JOIN perk_agg p ON h.hero_id = p.hero_id
        """

    def find_hero_detail_by_id(self, hero_id: int) -> pd.DataFrame:
        """특정 ID 영웅으로 3개 테이블 조인 후 반환"""
        with duckdb.connect(self.db_path) as con:
            query = self.base_query + " WHERE h.hero_id = ?"
            return con.execute(query, [hero_id]).df()

    def find_hero_detail_by_name(self, hero_name: str) -> pd.DataFrame:
        """특정 영웅 이름으로 3개 테이블 조인 후 반환"""
        with duckdb.connect(self.db_path) as con:
            query = self.base_query + " WHERE h.name = ?"
            return con.execute(query, [hero_name]).df()

    def find_all_hero_details(self) -> pd.DataFrame:
        """모든 영웅의 상세 정보를 조인 후 반환"""
        with duckdb.connect(self.db_path) as con:
            query = self.base_query + " ORDER BY h.hero_id ASC"
            return con.execute(query).df()
import duckdb
import pandas as pd
from . import Interfaces as i

class HeroStatsQueryRepository(i.IHeroStatsQueryRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        
        # 조인 string
        self.base_join = """
            FROM hero_stat s
            JOIN hero h ON s.hero_id = h.hero_id
            JOIN map m ON s.map_id = m.map_id
            JOIN tier t ON s.tier_id = t.tier_id
        """

        # 모든 데이터
        # SELECT 
        #         h.hero_id, h.name AS hero_name, h.role, h.subrole,
        #         m.map_id, m.map_name, m.mod AS map_mode,
        #         t.tier_id, t.tier_name, t.tier_order,
        #         s.winrate, s.pickrate, s.banrate

        # 전체 데이터 SELECT srtring
        self.base_select = """
            SELECT 
                h.name AS hero_name, h.role, h.subrole, h.portrait_url,
                m.map_id, m.map_name, m.mod AS map_mode,
                t.tier_name,
                s.winrate, s.pickrate, s.banrate
        """
        # 요약 SELECT srtring
        # name winrate pickrate banrate
        self.summary_select = """
            SELECT
                h.name AS hero_name, h.portrait_url,
                s.winrate, s.pickrate, s.banrate
        """

    def _get_order_clause(self, sort_by: str, ascending: bool) -> str:
        """
        정렬 기준과 순서를 SQL 문자열로 변환합니다.
        SQL 인젝션을 방지하기 위해 허용된 컬럼명만 통과시킵니다.
        """
        valid_columns = {'winrate', 'pickrate', 'banrate'}
        
        # 허용되지 않은 문자열이 들어오면 기본값인 'winrate'로 강제 고정합니다.
        safe_col = sort_by.lower() if sort_by.lower() in valid_columns else 'winrate'
        
        # ascending이 True면 오름차순(ASC), False면 내림차순(DESC)
        direction = 'ASC' if ascending else 'DESC'
        
        return f"ORDER BY s.{safe_col} {direction}"

    def find_hero_stat_by_id(self, hero_id: int, map_id: int, tier_id: int) -> pd.DataFrame:
        with duckdb.connect(self.db_path) as con:
            query = self.base_query + " WHERE s.hero_id = ? AND s.map_id = ? AND s.tier_id = ?"
            return con.execute(query, [hero_id, map_id, tier_id]).df()

    def find_stat_by_map_tier(self, map_id: int, tier_id: int, sort_by: str = 'winrate', ascending: bool = False, limit : int = 5, is_summary: bool = True) -> pd.DataFrame:
        with duckdb.connect(self.db_path) as con:
            order_clause = self._get_order_clause(sort_by, ascending)
            
            # 요약인지 아닌지
            select_clause = self.summary_select if is_summary else self.base_select

            query = select_clause + self.base_join + f" WHERE s.map_id = ? AND s.tier_id = ? {order_clause} LIMIT ?"
            return con.execute(query, [map_id, tier_id, limit]).df()

    def find_hero_trend_by_map(self, hero_id: int, tier_id: int) -> pd.DataFrame:
        with duckdb.connect(self.db_path) as con:
            # 더미 맵(map_id = 0)을 제외하고 해당 티어에서 영웅의 승률이 높은 맵 순으로 정렬
            query = self.base_query + " WHERE s.hero_id = ? AND s.tier_id = ? AND s.map_id != 0 ORDER BY s.winrate DESC"
            return con.execute(query, [hero_id, tier_id]).df()
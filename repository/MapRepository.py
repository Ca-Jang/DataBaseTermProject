import duckdb
import pandas as pd
from . import Interfaces as i

class MapRepository(i.IMapRepository):
    def __init__(self, db_path :str):
        self.db_path = db_path

    def create_table(self) : 
        """테이블 만들기"""
        with duckdb.connect(self.db_path) as con :
            con.execute("""
                        -- auto increment 를 위한 SEQUENCE 생성
                        CREATE SEQUENCE IF NOT EXISTS seq_map_id START 1;
                        
                        -- map 테이블
                        -- 맵의 기본 정보 저장
                        CREATE TABLE IF NOT EXISTS map (
                            map_id INT DEFAULT nextval('seq_map_id') NOT NULL,
                            map_name VARCHAR NOT NULL,
                            mod VARCHAR NOT NULL,
                            screenshot_url VARCHAR NULL,
                            PRIMARY KEY (map_id)
                            );
                        """)

    def insert_dummy_map(self):
        """'전체 맵'(map_id = 0) 추가"""
        with duckdb.connect(self.db_path) as con:
            dummy_check = con.execute("SELECT COUNT(*) FROM map WHERE map_id = 0").fetchone()[0]
            if dummy_check == 0:
                con.execute("INSERT INTO map (map_id, map_name, mod) VALUES (0, '전체 맵', '전체')")
                print("-> [알림] 0번 '전체 맵' 더미 데이터 추가 완료!")

    def insert_batch(self, df: pd.DataFrame):
        """맵 일괄 삽입 (중복 제외)"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_maps', df)
            con.execute("""
                INSERT INTO map (map_name, mod, screenshot_url)
                SELECT map_name, mod, screenshot_url FROM v_maps
                WHERE map_name NOT IN (SELECT map_name FROM map)
            """)

    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """맵 삽입"""
        with duckdb.connect(self.db_path) as con:
            con.register('v_input', row)
            result_df = con.execute("""
                        INSERT INTO map (map_name, mod, screenshot_url)
                        SELECT map_name, mod, screenshot_url FROM v_input
                        RETURNING *;
                        """).df()
            return result_df

    def find_by_id(self, map_id: int) -> pd.DataFrame:
        """map_id으로 맵 조회"""
        with duckdb.connect(self.db_path) as con :
            return con.execute("SELECT * FROM map WHERE map_id = ?", [map_id]).df()
        
    def find_map_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        """keyword로 이름조회, 디폴트는 전체 반환"""
        with duckdb.connect(self.db_path) as con :
            if keyword :
                query = "SELECT * FROM map WHERE map_name LIKE ?"
                return con.execute(query, [f"%{keyword}%"]).df()
            else :
                query = "SELECT * FROM map"
                return con.execute(query).df()

    def find_all(self) -> pd.DataFrame:
        """모든 맵 반환"""
        with duckdb.connect(self.db_path) as con :
            return con.execute("SELECT * FROM map").df()

    def update(self, row: pd.DataFrame) -> bool:
        """맵 정보 수정"""
        if row.empty or 'map_id' not in row.columns :
            return False
        
        try:
            with duckdb.connect(self.db_path) as con:
                con.register('v_update', row)
                con.execute("""
                            UPDATE map
                            SET map_id = v.map_id,
                                map_name = v.map_name,
                                mod = v.mod,
                                screenshot_url = v.screenshot_url
                            FROM v_update v
                            WHERE map.map_id = v.map_id;
                            """)
            return True
        except Exception as e:
            print(f"Map Update Error {e}")
            return False

    def delete(self, map_id: int) -> bool:
        """맵 삭제"""
        try :
            with duckdb.connect(self.db_path) as con:
                con.execute("DELETE FROM map WHERE map_id = ?", [map_id])
                return True
        except Exception as e:
            print(f"Delete Error {e}")
            return False
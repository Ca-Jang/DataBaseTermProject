import sys
import os
import duckdb

# 현재 파일(tools)의 상위 폴더(프로젝트 루트) 경로를 찾아서 시스템 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)              
sys.path.append(project_root)

from repository import HeroRepository
from repository import HeroStatRepository
from service import Fetch_HeroStat_Service

def main():
    # 1. 의존성 설정 (DB 연결 및 객체 생성)
    db_path = r'Code\Databasec\TermProject\data\hero_stats.db'
    
    hero_repo = HeroRepository(db_path)
    stat_repo = HeroStatRepository(db_path)
    
    # 서비스 객체에 2개의 저장소(Hero: 읽기용, Stat: 저장용)를 넘겨줍니다.
    service = Fetch_HeroStat_Service(hero_repo, stat_repo)
    print("0. 데이터베이스 저장소 객체 생성 완료")

    # 2. 서비스 실행 (통계 크롤링 및 DB 저장)
    success = service.fetch_and_save_stats()

    # 3. 결과 확인 (JOIN 테스트)
    if success:
        print("\n[저장된 통계 데이터 예시 확인 (서킷 로얄, 전체 티어의 승률 TOP 5)]")
        with duckdb.connect(db_path) as con:
            test_query = """
                SELECT h.name AS '영웅', m.map_name AS '맵', t.tier_name AS '티어', 
                       ROUND(s.winrate, 2) AS '승률(%)', ROUND(s.pickrate, 2) AS '픽률(%)'
                FROM hero_stat s
                JOIN hero h ON s.hero_id = h.hero_id
                JOIN map m ON s.map_id = m.map_id
                JOIN tier t ON s.tier_id = t.tier_id
                WHERE m.map_name = '서킷 로얄' AND t.tier_name = '전체'
                ORDER BY s.winrate DESC
                LIMIT 5;
            """
            print(con.query(test_query).df())

if __name__ == "__main__":
    main()
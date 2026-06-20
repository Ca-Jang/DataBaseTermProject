import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)              
sys.path.append(project_root)

from repository import MapRepository
from service import Fetch_Map_Service

def main():
    db_path = r'Code\Databasec\TermProject\data\hero_stats.db' 
    repository = MapRepository(db_path)
    service = Fetch_Map_Service(repository)
    
    print("1. 데이터베이스 저장소 객체 생성 완료")

    # 테이블이 없으면 생성
    repository.create_table()

    # 2. 서비스 실행 (더미 삽입 -> API 수집 -> 필터링 -> 저장)
    success = service.fetch_and_save_maps()

    # 3. 결과 확인
    if success:
        result_df = repository.find_all()
        print("\n[DuckDB map 테이블 전체 조회 결과]")
        print(result_df)

if __name__ == "__main__":
    main()
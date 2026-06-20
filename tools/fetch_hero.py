import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from repository import HeroRepository
from service import Hero_Fetch_Service

def main():
    # 1. 의존성 설정 (DB 연결 및 객체 생성)
    db_path = r'Code\Databasec\TermProject\data\hero_stats.db'
    repository = HeroRepository(db_path)
    service = Hero_Fetch_Service(repository)
    
    print("1. 데이터베이스 저장소 객체 생성 완료")

    # 테이블이 없으면 생성
    repository.create_table()

    # 2. 서비스 실행 (API 수집 및 저장)
    success = service.fetch_and_save_heroes()

    # 3. 결과 확인 (저장된 데이터 조회)
    if success:
        result_df = repository.find_all()
        print("\n[DuckDB hero 테이블 전체 조회 결과 (상위 10개)]")
        print(result_df.head(10))
        print(f"... 총 {len(result_df)}건 저장됨")

if __name__ == "__main__":
    main()
import duckdb
import pandas as pd

# 1. 기존 DuckDB 데이터베이스 파일 연결
db_path = 'Code\Databasec\TermProject\data\hero_stats.db'
con = duckdb.connect(db_path)

print("1. 데이터베이스 연결 완료")

# 2. Pandas 데이터프레임으로 티어 리스트 준비
# tier_id는 시퀀스로 자동 생성되므로, 이름과 정렬 순서만 정의합니다.
df_tier_input = pd.DataFrame({
    'tier_name': ['전체', '브론즈', '실버', '골드', '플래티넘', '다이아', '마스터', '그랜드마스터'],
    'tier_order': [0, 1, 2, 3, 4, 5, 6, 7]  # 정렬 기준용 숫자
})

# 3. DuckDB에 임시 뷰로 등록
con.register('v_tier_input', df_tier_input)

# 4. INSERT INTO ... SELECT 문으로 삽입
existing_count = con.execute("SELECT COUNT(*) FROM tier").fetchone()[0]

if existing_count == 0:
    print("3. 티어 데이터 삽입 중...")
    con.execute("""
        INSERT INTO tier (tier_name, tier_order)
        SELECT tier_name, tier_order FROM v_tier_input
    """)
    print("   -> 티어 데이터 삽입 완료!")
else:
    print(f"3. 이미 {existing_count}개의 데이터 존재")

# 5. 저장된 결과 확인 (순서대로 정렬)
result_df = con.query("SELECT * FROM tier ORDER BY tier_order ASC").df()
print("\n[현재 tier 테이블 전체 조회 결과]")
print(result_df)

con.close()
print("\n4. 데이터베이스 연결 종료")
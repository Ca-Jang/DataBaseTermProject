import pandas as pd
import requests
import time
from repository import HeroRepository

class Hero_Fetch_Service:
    def __init__(self, repository: HeroRepository):
        self.repository = repository
        # 역할군 번역 매핑
        self.role_mapping = {
            'tank': '돌격군', 'damage': '공격군', 'support': '지원가'
        }
        # 세부 역할군 번역 매핑
        self.subrole_mapping = {
            'flanker': '측면공격가', 'recon': '수색가', 'sharpshooter': '명사수',
            'specialist': '전문가', 'stalwart': '강건한 자', 'initiator': '개시자',
            'bruiser': '투사', 'medic': '의무관', 'survivor': '생존왕', 'tactician': '전술가'
        }

    def fetch_and_save_heroes(self):
        """API에서 영웅 목록을 가져와 파싱 후 DB에 저장합니다."""
        list_api_url = "https://overfast-api.tekrop.fr/heroes?locale=ko-kr"
        print(f"2. 전체 영웅 목록 가져오는 중... ({list_api_url})")
        list_response = requests.get(list_api_url)

        if list_response.status_code != 200:
            print(f"전체 영웅 리스트 요청 실패 (상태 코드: {list_response.status_code})")
            return False

        heroes_list = list_response.json()
        total_heroes = len(heroes_list)
        print(f"   -> 총 {total_heroes}명의 영웅을 찾았습니다!\n")
        
        collected_data = [] 
        
        print("3. 영웅 상세 정보 순차 수집 시작...")
        for index, hero_basic in enumerate(heroes_list, start=1):
            hero_key = hero_basic.get('key')
            detail_url = f"https://overfast-api.tekrop.fr/heroes/{hero_key}?locale=ko-kr"
            detail_res = requests.get(detail_url)
            
            if detail_res.status_code == 200:
                detail_data = detail_res.json()
                
                # 정보 가공
                hitpoints = detail_data.get('hitpoints', {})
                
                collected_data.append({
                    'name': detail_data.get('name'),
                    'role': self.role_mapping.get(detail_data.get('role'), '미분류'),
                    'subrole': self.subrole_mapping.get(detail_data.get('subrole'), '미분류'),
                    'health': hitpoints.get('health', 0),
                    'armor': hitpoints.get('armor', 0),
                    'shields': hitpoints.get('shields', 0),
                    'portrait_url': detail_data.get('portrait')
                })
                print(f"   [{index}/{total_heroes}] {detail_data.get('name')} 데이터 수집 완료")
            else:
                print(f"   [{index}/{total_heroes}] {hero_key} 데이터 수집 실패 (에러코드: {detail_res.status_code})")
            
            time.sleep(0.2)
            
        print("\n모든 영웅 데이터 수집 완료!")
        
        # Pandas 변환 및 Repository에 저장 위임
        df_all_heroes = pd.DataFrame(collected_data)
        
        print("\n4. DuckDB 테이블 초기화 및 일괄 저장 중...")
        self.repository.reset_table_and_sequence()
        self.repository.insert_batch(df_all_heroes)
        
        return True
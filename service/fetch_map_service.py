import pandas as pd
import requests

class Fetch_Map_Service:
    def __init__(self, repository):
        self.repository = repository
        # 🌟 핵심 모드 딕셔너리 매핑
        self.mode_mapping = {
            'escort': '호위',
            'control': '쟁탈',
            'hybrid': '점령/호위',
            'push': '밀기',
            'flashpoint': '플래시포인트'
        }

    def fetch_and_save_maps(self):
        """API에서 맵 데이터를 가져와 필터링 후 DB에 저장합니다."""
        
        # 1. 더미 데이터 추가 확인
        self.repository.insert_dummy_map()

        # 2. API 호출
        api_url = "https://overfast-api.tekrop.fr/maps"
        print(f"\n2. 맵 데이터 API 호출 중... ({api_url})")

        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"API 요청 실패 (상태 코드: {response.status_code})")
            return False

        maps_list = response.json()
        collected_maps = []
        
        # 3. 데이터 가공 및 필터링
        for m in maps_list:
            map_name = m.get('name')
            gamemodes = m.get('gamemodes', [])
            first_mode_eng = gamemodes[0] if gamemodes else '기타'
            screenshot_url = m.get('screenshot')
            
            # API에서 가져온 모드가 정의한 5개 모드 안에 있을 때만 저장
            if first_mode_eng in self.mode_mapping:
                mod_kor = self.mode_mapping[first_mode_eng]
                
                collected_maps.append({
                    'map_name': map_name,
                    'mod': mod_kor,
                    'screenshot_url': screenshot_url
                })

        print(f"   -> 전체 맵 중 조건에 맞는 {len(collected_maps)}개의 경쟁전 맵을 필터링했습니다.")

        # 4. Pandas 변환 및 Repository에 저장 위임
        df_maps = pd.DataFrame(collected_maps)
        
        print("\n3. 필터링된 맵 데이터를 DuckDB에 삽입하는 중...")
        self.repository.insert_batch(df_maps)
        print("   -> 맵 데이터 삽입 완료!")
        
        return True
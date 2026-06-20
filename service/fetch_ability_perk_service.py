import pandas as pd
import requests
import time

class Fetch_Ability_Perk_Service:
    def __init__(self, hero_repo, ability_repo, perk_repo):
        self.hero_repo = hero_repo
        self.ability_repo = ability_repo
        self.perk_repo = perk_repo

    def fetch_and_save_data(self):
        # 1. Repo를 통해 영웅 정보 가져오기
        db_heroes = self.hero_repo.get_all_heroes()
        
        # 2. API용 영문 키값 딕셔너리 생성
        list_api_url = "https://overfast-api.tekrop.fr/heroes?locale=ko-kr"
        api_list = requests.get(list_api_url).json()
        name_to_key = {h['name']: h['key'] for h in api_list}
        
        print(f"DB에서 {len(db_heroes)}명의 영웅을 불러왔습니다. 상세 정보 수집을 시작합니다...")

        collected_abilities = []
        collected_perks = []

        # 3. 기존 로직 그대로 유지: 영웅별 상세 API 호출 및 데이터 짝짓기
        for index, row in db_heroes.iterrows():
            skill_id_counter = 1
            perk_id_counter = 1
            hero_id = row['hero_id']
            hero_name = row['name']
            
            hero_key = name_to_key.get(hero_name)
            if not hero_key:
                continue
                
            detail_url = f"https://overfast-api.tekrop.fr/heroes/{hero_key}?locale=ko-kr"
            res = requests.get(detail_url)
            
            if res.status_code == 200:
                data = res.json()
                
                # [1] 스킬 데이터 파싱
                for ab in data.get('abilities', []):
                    collected_abilities.append({
                        'skill_id': skill_id_counter,
                        'hero_id': hero_id,
                        'skill_name': ab.get('name'),
                        'description': ab.get('description'),
                        'icon_url': ab.get('icon')
                    })
                    skill_id_counter += 1
                    
                # [2] 특성 데이터 파싱
                perks = data.get('perks', {})
                for pe in perks.get('minor', []):
                    collected_perks.append({
                        'perk_id': perk_id_counter,
                        'hero_id': hero_id,
                        'perk_name': pe.get('name'),
                        'perk_type': 'minor',
                        'description': pe.get('description'),
                        'icon_url': pe.get('icon')
                    })
                    perk_id_counter += 1

                perk_id_counter = 1
                for pe in perks.get('major', []):
                    collected_perks.append({
                        'perk_id': perk_id_counter,
                        'hero_id': hero_id,
                        'perk_name': pe.get('name'),
                        'perk_type': 'major',
                        'description': pe.get('description'),
                        'icon_url': pe.get('icon')
                    })
                    perk_id_counter += 1
                
                print(f"   [{index+1}/{len(db_heroes)}] {hero_name} 스킬 및 특성 매핑 완료")
                
            time.sleep(0.2) # 서버 과부하 방지

        # 4. DataFrame 변환
        df_abilities = pd.DataFrame(collected_abilities)
        df_perks = pd.DataFrame(collected_perks)

        # self.ability_repo.delete_all()
        # self.perk_repo.delete_all()

        print("\nDB에 데이터를 밀어넣는 중...")
        # 6. 데이터 삽입 (Service -> Repo 호출)
        self.ability_repo.insert(df_abilities)
        self.perk_repo.insert(df_perks)
        print("   -> 성공적으로 저장되었습니다!")
import pandas as pd
import requests
import json
import time
from bs4 import BeautifulSoup

class Fetch_HeroStat_Service:
    def __init__(self, hero_repo, stat_repo):
        self.hero_repo = hero_repo
        self.stat_repo = stat_repo
        self.hero_id_mapping = {}
        self.collected_stats = []

    def crawl_overwatch_stats(self, map_slug, tier_slug, map_id, tier_id):
        """Overbuff 사이트에서 특정 맵과 티어의 영웅 통계를 크롤링합니다."""
        url = f"https://www.overbuff.com/heroes?platform=pc&gameMode=competitive&map={map_slug}&tier={tier_slug}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')

            if not script_tag:
                print(f"      [실패] 데이터를 찾을 수 없습니다. ({url})")
                return False

            json_data = json.loads(script_tag.string)
            heroes_data = json_data.get('props', {}).get('pageProps', {}).get('heroes', [])

            if not heroes_data:
                print("      [실패] 영웅 통계 리스트가 비어있습니다.")
                return False

            for hero in heroes_data:
                kor_name = hero.get('name')
                if kor_name not in self.hero_id_mapping:
                    continue

                self.collected_stats.append({
                    'hero_id': self.hero_id_mapping[kor_name],
                    'map_id': map_id,
                    'tier_id': tier_id,
                    'winrate': float(hero.get('winRate', 0)) * 100,
                    'pickrate': float(hero.get('pickRate', 0)) * 100,
                    'banrate': float(hero.get('tieRate', 0)) * 100 
                })

            return True

        except Exception as e:
            print(f"      [에러 발생] {e}")
            return False

    def fetch_and_save_stats(self):
        """크롤링 전체 흐름을 제어하고 DB에 저장합니다."""
        
        # 1. DB에서 영웅 ID 매핑 정보 가져오기
        df_heroes = self.hero_repo.find_all()
        self.hero_id_mapping = dict(zip(df_heroes['name'], df_heroes['hero_id']))
        
        print("1. 영웅 ID 매핑 정보 로드 완료")

        # ==========================================
        # 2. URL 슬러그 <-> DB ID 매핑 딕셔너리 정의
        # ==========================================
        # (1) 티어 매핑 (DB 이름 : (DB ID, URL 슬러그))
        tier_mapping = {
            '전체': (1, 'all-tiers'),
            '브론즈': (2, 'Bronze'),
            '실버': (3, 'Silver'),
            '골드': (4, 'Gold'),
            '플래티넘': (5, 'Platinum'),
            '다이아': (6, 'Diamond'),
            '마스터': (7, 'Master'),
            '그랜드마스터': (8, 'Grandmaster')
        }

        # (2) 맵 매핑 (DB 이름 : (DB ID, URL 슬러그))
        # 이전 단계에서 수집된 맵들의 정확한 영문 슬러그를 지정합니다. (핵심 경쟁전 맵 예시)
        map_mapping = {
            '전체 맵': (0, 'all-maps'),
            'Aatlis': (1, 'aatlis'),
            'Antarctic Peninsula': (2, 'antarctic-peninsula'),
            'Arena Victoriae': (3, 'arena-victoriae'),
            'Blizzard World': (4, 'blizzard-world'),
            'Busan': (5, 'busan'),
            'Circuit Royal': (6, 'circuit-royal'),
            'Colosseo': (7, 'colosseo'),
            'Dorado': (8, 'dorado'),
            'Eichenwalde': (9, 'eichenwalde'),
            'Esperança': (10, 'esperanca'),
            'Gogadoro': (11, 'gogadoro'),
            'Havana': (12, 'havana'),
            'Hollywood': (13, 'hollywood'),
            'Ilios': (14, 'ilios'),
            'Junkertown': (15, 'junkertown'),
            'Lijiang Tower': (16, 'lijiang-tower'),
            'Kings Row': (17, 'kings-row'),
            'Midtown': (18, 'midtown'),
            'Nepal': (19, 'nepal'),
            'New Junk City': (20, 'new-junk-city'),
            'New Queen Street': (21, 'new-queen-street'),
            'Numbani': (22, 'numbani'),
            'Oasis': (23, 'oasis'),
            'Paraíso': (24, 'paraiso'),
            'Place Lacroix': (25, 'place-lacroix'),
            'Redwood Dam': (26, 'redwood-dam'),
            'Rialto': (27, 'rialto'),
            'Route 66': (28, 'route-66'),
            'Runasapi': (29, 'runasapi'),
            'Samoa': (30, 'samoa'),
            'Shambali Monastery': (31, 'shambali-monastery'),
            'Suravasa': (32, 'suravasa'),
            'Watchpoint: Gibraltar': (33, 'watchpoint-gibraltar'),
            'Wuxing University': (34, 'wuxing-university')
    }

        # 3. 크롤링 진행
        print("\n[작업 1] 전체 맵 기준, 모든 개별 티어 통계 수집 시작...")
        map_all_id, map_all_slug = map_mapping['전체 맵']

        for tier_name, (tier_id, tier_slug) in tier_mapping.items():
            print(f"   -> [전체 맵]의 '{tier_name}' 티어 통계 가져오는 중...")
            success = self.crawl_overwatch_stats(map_all_slug, tier_slug, map_all_id, tier_id)
            if success:
                print(f"      완료 (현재 누적 데이터: {len(self.collected_stats)}건)")
            time.sleep(1.5) 

        print("\n[작업 2] 개별 맵 기준 전체 티어 통합 통계 수집 시작...")
        tier_all_id, tier_all_slug = tier_mapping['전체']

        for map_name, (map_id, map_slug) in map_mapping.items():
            if map_name == '전체 맵': 
                continue 
                
            print(f"   -> [{map_name}]의 '전체 티어' 통합 통계 가져오는 중...")
            success = self.crawl_overwatch_stats(map_slug, tier_all_slug, map_id, tier_all_id)
            if success:
                print(f"      완료 (현재 누적 데이터: {len(self.collected_stats)}건)")
            time.sleep(1.5)

        # 4. 데이터 저장
        if self.collected_stats:
            df_stats = pd.DataFrame(self.collected_stats)
            
            print("\n4. 전방위 통계 데이터를 DuckDB에 일괄 저장 중...")
            self.stat_repo.reset_table()
            self.stat_repo.insert_batch(df_stats)
            print("   -> 데이터 저장 완료!")
            return True
        else:
            print("\n저장할 데이터가 수집되지 않았습니다.")
            return False
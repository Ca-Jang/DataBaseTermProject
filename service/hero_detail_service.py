from repository import HeroDetailsQueryRepository

class Hero_Detail_Service() :
    def __init__(self, hero_repo: HeroDetailsQueryRepository):
        self.hero_repo = hero_repo

    def get_hero_detail(self, name: str):
        df = self.hero_repo.find_hero_detail_by_name(name)
        if df.empty:
            return None
            
        # 데이터프레임을 파이썬 딕셔너리로
        # 데이터를 꺼내기 쉽게 하기 위해 익숙한 딕션어리로 바꾸었습니다.
        data = df.iloc[0].to_dict()
            
        return data
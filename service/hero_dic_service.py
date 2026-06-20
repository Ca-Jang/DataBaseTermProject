from repository import HeroRepository

class Hero_Dic_Service:
    def __init__(self, hero_repo: HeroRepository):
        self.hero_repo = hero_repo
    
    def search_heroes(self, keyword: str = None):
        return self.hero_repo.find_heroes_by_keyword(keyword)
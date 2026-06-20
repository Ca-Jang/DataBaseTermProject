from repository import MapRepository

class Map_Dic_Service:
    def __init__(self, repo: MapRepository):
        self.repo = repo
    
    def search_map(self, keyword: str = None):
        return self.repo.find_map_by_keyword(keyword)
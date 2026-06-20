from abc import ABC, abstractmethod
import pandas as pd


# ══════════════════════════════════════════════════════════
#  IHeroRepository
# ══════════════════════════════════════════════════════════
class IHeroRepository(ABC):

    @abstractmethod
    def create_table(self): 
        """테이블 만들기"""
        ...

    @abstractmethod
    def reset_table_and_sequence(self):
        """테이블 초기화 및 시퀀스 재설정 (테스트 용)"""
        ...

    @abstractmethod
    def insert_batch(self, df: pd.DataFrame):
        """일괄 영웅 삽입"""
        ...

    @abstractmethod
    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """영웅 삽입"""
        ...

    @abstractmethod
    def find_by_id(self, hero_id: int) -> pd.DataFrame:
        """hero_id으로 영웅 조회"""
        ...

    @abstractmethod
    def find_heroes_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        """키워드가 있으면 해당 영웅 검색, 키워드 없으면 전체 영웅 반환"""
        ...

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        """모든 영웅 반환"""
        ...

    @abstractmethod
    def update(self, row: pd.DataFrame) -> bool:
        """영웅 정보 수정"""
        ...

    @abstractmethod
    def delete(self, hero_id: int) -> bool:
        """영웅 삭제"""
        ...


# ══════════════════════════════════════════════════════════
#  IMapRepository
# ══════════════════════════════════════════════════════════
class IMapRepository(ABC):

    @abstractmethod
    def create_table(self): 
        """테이블 만들기"""
        ...

    @abstractmethod
    def insert_dummy_map(self):
        """'전체 맵'(map_id = 0) 추가"""
        ...

    @abstractmethod
    def insert_batch(self, df: pd.DataFrame):
        """맵 일괄 삽입 (중복 제외)"""
        ...

    @abstractmethod
    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """맵 삽입"""
        ...

    @abstractmethod
    def find_by_id(self, map_id: int) -> pd.DataFrame:
        """map_id으로 맵 조회"""
        ...

    @abstractmethod
    def find_map_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        """keyword로 이름조회, 디폴트는 전체 반환"""
        ...

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        """모든 맵 반환"""
        ...

    @abstractmethod
    def update(self, row: pd.DataFrame) -> bool:
        """맵 정보 수정"""
        ...

    @abstractmethod
    def delete(self, map_id: int) -> bool:
        """맵 삭제"""
        ...


# ══════════════════════════════════════════════════════════
#  ITierRepository
# ══════════════════════════════════════════════════════════
class ITierRepository(ABC):

    @abstractmethod
    def create_table(self): 
        """테이블 만들기"""
        ...

    @abstractmethod
    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """티어 삽입"""
        ...

    @abstractmethod
    def find_by_id(self, tier_id: int) -> pd.DataFrame:
        """tier_id로 티어 조회"""
        ...

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        """모든 티어를 tier_order 오름차순으로 반환"""
        ...

    @abstractmethod
    def update(self, row: pd.DataFrame) -> bool:
        """티어 정보 수정"""
        ...

    @abstractmethod
    def delete(self, tier_id: int) -> bool:
        """티어 삭제"""
        ...


# ══════════════════════════════════════════════════════════
#  IHeroAbilityRepository
# ══════════════════════════════════════════════════════════
class IHeroAbilityRepository(ABC):

    @abstractmethod
    def create_table(self): 
        """테이블 만들기"""
        ...

    @abstractmethod
    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """스킬 삽입"""
        ...

    @abstractmethod
    def find_by_hero(self, hero_id: int) -> pd.DataFrame:
        """hero_id에 해당하는 모든 스킬 반환"""
        ...

    @abstractmethod
    def update(self, row: pd.DataFrame) -> bool:
        """스킬 정보 수정"""
        ...

    @abstractmethod
    def delete(self, skill_id: int, hero_id: int) -> bool:
        """(skill_id, hero_id) 복합키로 스킬 삭제."""
        ...


# ══════════════════════════════════════════════════════════
#  IPerkRepository
# ══════════════════════════════════════════════════════════
class IPerkRepository(ABC):

    @abstractmethod
    def create_table(self): 
        """테이블 만들기"""
        ...

    @abstractmethod
    def insert(self, row: pd.DataFrame) -> pd.DataFrame:
        """특전 삽입"""
        ...

    @abstractmethod
    def find_by_hero(self, hero_id: int) -> pd.DataFrame:
        """hero_id에 해당하는 모든 특전 반환"""
        ...

    @abstractmethod
    def update(self, row: pd.DataFrame) -> bool:
        """특전 정보 수정"""
        ...

    @abstractmethod
    def delete(self, perk_id: int, hero_id: int) -> bool:
        """(perk_id, hero_id) 복합키로 특전 삭제"""
        ...


# ══════════════════════════════════════════════════════════
#  IHeroStatRepository
# ══════════════════════════════════════════════════════════
class IHeroStatRepository(ABC):

    @abstractmethod
    def create_table(self): 
        """테이블 만들기"""
        ...

    @abstractmethod
    def insert_batch(self, df: pd.DataFrame):
        """데이터프레임을 통한 일괄 통계 삽입"""
        ...

    @abstractmethod
    def find_by_hero(self, hero_id: int) -> pd.DataFrame:
        """특정 영웅의 모든 맵, 티어 통계 반환"""
        ...

    @abstractmethod
    def delete(self, hero_id: int, map_id: int, tier_id: int) -> bool:
        """(hero_id, map_id, tier_id) 복합키로 통계 삭제"""
        ...



# ══════════════════════════════════════════════════════════
#  IHeroDetailsQueryRepository
# ══════════════════════════════════════════════════════════
class IHeroDetailsQueryRepository(ABC):

    @abstractmethod
    def find_hero_detail_by_id(self, hero_id: int) -> pd.DataFrame:
        """특정 ID 영웅으로 hero, hero_ability, perk 3개 테이블 조인후 반환"""
        ...

    @abstractmethod
    def find_hero_detail_by_name(self, hero_name: str) -> pd.DataFrame:
        """특정 영웅 이름으로 hero, hero_ability, perk 3개 테이블 조인후 반환"""
        ...

    @abstractmethod
    def find_all_hero_details(self) -> pd.DataFrame:
        """모든 영웅의 상세 정보를 hero, hero_ability, perk 3개 테이블 조인후 반환"""
        ...


# ══════════════════════════════════════════════════════════
#  IHeroStatsQueryRepository
# ══════════════════════════════════════════════════════════
class IHeroStatsQueryRepository(ABC):

    @abstractmethod
    def find_hero_stat_by_id(self, hero_id: int, map_id: int, tier_id: int) -> pd.DataFrame:
        """특정 영웅의 hero, hero_stat, map, tier 4개 테이블 조인"""
        ...

    @abstractmethod
    def find_stat_by_map_tier(self, map_id: int, tier_id: int, sort_by: str = 'winrate', ascending: bool = False, limit: int = 5, is_summary: bool = True) -> pd.DataFrame:
        """특정 맵, 티어의 영웅을 정렬기준에 따라 hero, hero_stat, map, tier 4개 테이블 조인후 반환"""
        ...

    @abstractmethod
    def find_hero_trend_by_map(self, hero_id: int, tier_id: int) -> pd.DataFrame:
        """특정 영웅, 티어의 통계를 승률 내림차순으로 맵과 조인하여 반환 (특정 영웅의 좋은 맵)"""
        ...
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from repository import HeroRepository
from repository import HeroAbilityRepository
from repository import PerkRepository
from service import Fetch_Ability_Perk_Service

def main():
    db_path = 'Code\Databasec\TermProject\data\hero_stats.db'
    
    # 1. Repository 인스턴스 생성
    hero_repo = HeroRepository(db_path)
    ability_repo = HeroAbilityRepository(db_path)
    perk_repo = PerkRepository(db_path)
    print("1. Repository 초기화 완료")

    # 2. Service에 Repository 주입 및 인스턴스 생성
    service = Fetch_Ability_Perk_Service(hero_repo, ability_repo, perk_repo)
    
    # 3. 비즈니스 로직 실행
    service.fetch_and_save_data()

if __name__ == "__main__":
    main()
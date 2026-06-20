from repository import HeroStatsQueryRepository

class DashboardService:
    def __init__(self, stat_repo: HeroStatsQueryRepository):
        self.stat_repo = stat_repo

    def get_dashboard_stats(self, map_id, tier_id, limit=5):
        return {
            "pick_top": self.stat_repo.find_stat_by_map_tier(
                map_id, tier_id, sort_by='pickrate', ascending = False, limit=limit
            ),
            "meta_top": self.stat_repo.find_stat_by_map_tier(
                map_id, tier_id, limit=limit, sort_by='winrate'
            )
        }
    
    def get_all_hero_stats(self, map_id, tier_id, ascending = 0, limit = 51):
        return self.stat_repo.find_stat_by_map_tier(map_id, tier_id, ascending = ascending, limit = limit, is_summary = False)
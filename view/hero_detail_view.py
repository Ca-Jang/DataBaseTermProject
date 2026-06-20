import flet as ft

def get_hero_detail_tab():
    detail_container = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
    
    def update_detail(hero_data):
        detail_container.controls.clear()
        
        if not hero_data:
            detail_container.controls.append(ft.Text("영웅 정보를 불러올 수 없습니다."))
            detail_container.update()
            return

        # 1. ⚔️ 스킬 리스트 UI 생성
        skills_ui = []
        for skill in hero_data.get('skills', []):
            skills_ui.append(
                ft.ListTile(
                    leading=ft.Image(src=skill['icon_url'], width=50, height=50, border_radius=5),
                    title=ft.Text(skill['skill_name'], weight="bold", size=18),
                    subtitle=ft.Text(skill['description']),
                )
            )

        # 2. ✨ 패시브/특성 리스트 UI 생성
        perks_ui = []
        for perk in hero_data.get('perks', []):
            perks_ui.append(
                ft.ListTile(
                    leading=ft.Image(src=perk['icon_url'], width=50, height=50, border_radius=5),
                    title=ft.Text(f"{perk['perk_name']} ({perk['perk_type']})", weight="bold", size=18),
                    subtitle=ft.Text(perk['description']),
                )
            )

        # 3. 🌟 최종 화면 조립
        detail_container.controls.extend([
            # --- 상단: 영웅 프로필 & 기본 스탯 ---
            ft.Row([
                # 초상화
                ft.Image(src=hero_data.get('portrait_url', ''), width=120, height=120, border_radius=15),
                ft.Column([
                    # 이름과 역할군
                    ft.Text(hero_data.get('hero_name', '이름 없음'), size=40, weight="bold"),
                    ft.Text(f"{hero_data.get('role', '')} - {hero_data.get('subrole', '')}", size=20, color=ft.Colors.GREY_700),
                    
                    # 체력/방어력/쉴드 배지 (칩 위젯 사용)
                    ft.Row([
                        ft.Chip(label=ft.Text(f"❤️ 체력: {hero_data.get('health', 0)}"), bgcolor=ft.Colors.RED_50),
                        ft.Chip(label=ft.Text(f"🛡️ 방어: {hero_data.get('armor', 0)}"), bgcolor=ft.Colors.ORANGE_50),
                        ft.Chip(label=ft.Text(f"🔵 쉴드: {hero_data.get('shields', 0)}"), bgcolor=ft.Colors.BLUE_50),
                    ])
                ])
            ], alignment=ft.MainAxisAlignment.START),
            
            ft.Divider(height=40),
            
            # --- 중단: 스킬 목록 ---
            ft.Text("⚔️ 스킬 (Abilities)", size=25, weight="bold"),
            ft.Card(content=ft.Column(skills_ui, spacing=0)),
            
            # --- 하단: 패시브 및 특성 ---
            ft.Text("✨ 특전 (Perks)", size=25, weight="bold"),
            ft.Card(content=ft.Column(perks_ui, spacing=0)),
            
            # 아래쪽 여백 추가
            ft.Container(height=40)
        ])
        
        detail_container.update()

    detail_container.update_detail = update_detail
    
    # 맨 처음 탭에 들어갔을 때 보이는 화면
    detail_container.controls.append(
        ft.Container(
            content=ft.Text("도감, 통계에서 영웅을 클릭하면 상세 정보가 표시됩니다.", size=20, color=ft.Colors.GREY_500),
            # alignment=ft.alignment.center,
            expand=True
        )
    )
    
    return detail_container
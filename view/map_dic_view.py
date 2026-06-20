import flet as ft
import pandas as pd

def get_map_list(page: ft.Page, service, on_map_click):
    
    # 카드 리스트 만들기
    def create_cards(df: pd.DataFrame):
        if df is None or df.empty:
            return [ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY)]
            
        cards = []
        for _, row in df.iterrows():
            # 전체 맵 스킵
            if row["map_name"] == '전체 맵' : continue

            card = ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=20,
                    ink=True,
                    # on_click=lambda e, name=row["map_id"]: print(f"{name} 클릭됨!"),
                    on_click=lambda e, map_id=str(row["map_id"]): on_map_click(map_id),
                    content=ft.Column([
                        ft.Image(src=row["screenshot_url"], width=300, height=150, border_radius=5),
                        ft.Text(str(row["map_name"]), weight="bold", size=18, text_align=ft.TextAlign.CENTER),
                        ft.Text(str(row.get("mod", "")), color=ft.Colors.GREY_500, size=14),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )
            cards.append(card)
        return cards

    # 맵 그리드
    map_grid = ft.GridView(
        expand=True,
        max_extent=300,
        child_aspect_ratio=1.0,
        spacing=15,
        run_spacing=15,
    )

    # 검색 이벤트 핸들러
    def apply_filters(e=None):
        keyword = filter_textField.value
        mod = mod_dropdown.value
        
        # DB에서 키워드로 먼저 검색
        filtered_df = service.search_map(keyword)

        # 가져온 데이터를 topdown바의 value로 한 번 더 필터링
        if mod != "전체" and filtered_df is not None and not filtered_df.empty:
            filtered_df = filtered_df[filtered_df['mod'].str.contains(mod, na=False)]

        map_grid.controls.clear()
        map_grid.controls.extend(create_cards(filtered_df))
        page.update()

    # 모드 드롭다운
    mod_dropdown = ft.Dropdown(
        width=130,
        value="전체",
        options=[
            ft.dropdown.Option("전체"),
            ft.dropdown.Option('쟁탈'),
            ft.dropdown.Option('점령/호위'),
            ft.dropdown.Option('호위'),
            ft.dropdown.Option('밀기'),
            ft.dropdown.Option('플래시포인트'),
        ],
        on_select=apply_filters,
        dense=True,
    )

    # TextField의 value Property 사용하기 위해 Container와 따로 적음
    filter_textField = ft.TextField(
        label="맵 검색",
        hint_text="맵 이름을 입력하고 엔터를 누르세요",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
        # margin=16,
        expand=True,
        on_change=apply_filters,
    )
    # 검색 ui wrapper
    filter_wrapper = ft.Container(filter_textField,)

    initial_df = service.search_map(None)
    map_grid.controls.extend(create_cards(initial_df))

    return ft.Column([
        ft.Row([
            ft.Text("맵별 통계", size=30, weight="bold", expand=True),
            ft.Column([
                ft.Text("모드", size=15, weight="bold"),
                mod_dropdown
                ])
            ]),
        ft.Row([filter_wrapper]),
        ft.Divider(),
        map_grid
    ], expand=True)
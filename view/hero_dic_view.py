import flet as ft
import pandas as pd

def get_hero_list(page: ft.Page, service, on_hero_click):
    
    # 카드 리스트 만들기
    def create_cards(df: pd.DataFrame):
        if df is None or df.empty:
            return [ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY)]
            
        cards = []
        for _, row in df.iterrows():
            card = ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=20,
                    ink=True,
                    # on_click=lambda e, name=row["name"]: print(f"{name} 클릭됨!"),
                    on_click=lambda e, name=str(row["name"]): on_hero_click(name),
                    content=ft.Column([
                        ft.Text(str(row["name"]), weight="bold", size=18, text_align=ft.TextAlign.CENTER),
                        ft.Text(str(row["role"]), color=ft.Colors.GREY_500, size=14),
                        ft.Text(str(row["subrole"]), color=ft.Colors.GREY_500, size=11),
                        ft.Image(src=row["portrait_url"], width=50, height=50, border_radius=5),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )
            cards.append(card)
        return cards

    # 영웅 카드가 담길 그리드
    hero_grid = ft.GridView(
        expand=True,
        max_extent=180,
        child_aspect_ratio=0.8,
        spacing=15,
        run_spacing=15,
    )

    # 검색 이벤트 핸들러
    def apply_filters(e=None):
        keyword = filter_textField.value
        role = role_dropdown.value
        subrole = subrole_dropdown.value
        
        # DB에서 키워드로 먼저 검색
        filtered_df = service.search_heroes(keyword)

        # 가져온 데이터를 topdown바의 value로 한 번 더 걸러줌
        if role != "전체" and filtered_df is not None and not filtered_df.empty:
            filtered_df = filtered_df[filtered_df['role'].str.contains(role, na=False)]
        
        # 가져온 데이터를 topdown바의 value로 한 번 더 걸러줌
        if subrole != "전체" and filtered_df is not None and not filtered_df.empty:
            filtered_df = filtered_df[filtered_df['subrole'].str.contains(subrole, na=False)]

        hero_grid.controls.clear()
        hero_grid.controls.extend(create_cards(filtered_df))
        page.update()

    # 역할군 드롭다운
    role_dropdown = ft.Dropdown(
        width=130,
        value="전체",
        options=[
            ft.dropdown.Option("전체"),
            ft.dropdown.Option("돌격군"),
            ft.dropdown.Option("공격군"),
            ft.dropdown.Option("지원가"),
        ],
        on_select=apply_filters,
        dense=True,
    )

    # 세부 역할군 드롭다운
    subrole_dropdown = ft.Dropdown(
        width=130,
        value="전체",
        options=[
            ft.dropdown.Option("전체"),
            # 딜러
            ft.dropdown.Option('측면공격가'),
            ft.dropdown.Option('수색가'),
            ft.dropdown.Option('명사수'),
            ft.dropdown.Option('전문가'),
            # 탱
            ft.dropdown.Option('강건한 자'),
            ft.dropdown.Option('개시자'),
            ft.dropdown.Option('투사'),
            # 힐
            ft.dropdown.Option('의무관'),
            ft.dropdown.Option('생존왕'),
            ft.dropdown.Option('전술가')
        ],
        on_select=apply_filters,
        dense=True,
    )

    # TextField의 value Properties 사용하기 위해 Container와 따로 적음
    filter_textField = ft.TextField(
        label="영웅 검색",
        hint_text="영웅 이름을 입력하고 엔터를 누르세요",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
        # margin=16,
        expand=True,
        on_change=apply_filters,
    )
    # 검색 ui wrapper
    filter_wrapper = ft.Container(filter_textField,)

    initial_df = service.search_heroes(None)
    hero_grid.controls.extend(create_cards(initial_df))

    return ft.Column([
        ft.Row([
            ft.Text("영웅 도감", size=30, weight="bold", expand=True),
            ft.Column([
                ft.Text("세부 역할군", size=15, weight="bold"),
                subrole_dropdown,
                ft.Text("역할군", size=15, weight="bold"),
                role_dropdown
                ])
            ]),
        ft.Row([filter_wrapper]),
        ft.Divider(),
        hero_grid
    ], expand=True)
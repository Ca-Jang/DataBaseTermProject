import flet as ft
import pandas as pd

def get_dashboard(page: ft.Page, dashboard_service, change_tab) -> ft.View:

        # 표 헤더 번역
    kor_headers = {
        "hero_name": "이름",
        "winrate": "승률",
        "pickrate": "픽률",
        "banrate": "밴률",
        "role": "역할군",
        "subrole": "세부 역할",
        "map_name": "맵 이름",
        "tier_name": "티어"
    }

    # 대시보드 데이터
    def build_dashboard(service, limit=5):
        data = service.get_dashboard_stats(map_id=0, tier_id=8, limit=limit)
        
        # 표 생성
        pick_table = data["pick_top"]
        meta_table = data["meta_top"]
        return {'pick_table' : pick_table, 'meta_table' : meta_table}

    # 데이터 df 가공해서 반환
    def create_table_from_df(df: pd.DataFrame):
        # 빈 데이터 처리
        if df is None or df.empty:
            return ft.Text("데이터가 없습니다.")
            
        rows = []
        for _, row in df.iterrows():
            cells = []
            for col in df.columns:
                # 이름 옆에 이미지 넣기
                if col == "hero_name": 
                    cell_content = ft.Row([
                        ft.Image(src=row["portrait_url"], width=30, height=30, border_radius=5),
                        ft.Text(str(row[col]), weight="bold")
                    ])
                    cells.append(ft.DataCell(cell_content))
                    
                # 이미 넣은 데이터인 이미지 스킵
                elif col == "portrait_url":
                    continue 
                    
                # 나머지 데이터 append 하기
                else:
                    cells.append(ft.DataCell(ft.Text(str(row[col]))))
                    
            rows.append(ft.DataRow(cells=cells))
            
        return ft.DataTable(
            # 헤더를 그릴 때 kor_headers 사전을 참조
            # .get(col, col) : 사전에 있으면 한글로, 없으면 원래 영문명 그대로 출력
            columns=[
                ft.DataColumn(ft.Text(kor_headers.get(col, col), weight="bold")) 
                for col in df.columns if col != "portrait_url"
            ],
            rows=rows,
        )
    
    # 대시보드 레이어 생성
    def create_layer(title : str, sub_title: str, df: pd.DataFrame, target_tab_index : int):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(title, size=30, weight="bold"),
                    ft.Divider(),
                    ft.Text(sub_title, size=20, weight="bold"),
                    ft.Divider(),
                    create_table_from_df(df)
                ], 
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                # 카드 전체 영역 클릭 시 change_tab 호출하여 화면 전환
                on_click=lambda _: change_tab(target_tab_index),
                ink=True
            ),
            expand=True,
        )

    # 데이터 가져오기 상위 5개만 요청
    dashboard_data = build_dashboard(dashboard_service, 5)

    # 데이터 flet row로 조립
    top_section = ft.Row(
        [
            create_layer("영웅 목록", "현재 픽률 Top 5", dashboard_data.get('pick_table'), 1),
            create_layer("맵 목록","현재 승률 Top 5", dashboard_data.get('meta_table'), 4),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # 뷰 반환
    return ft.Column([
        ft.Text("Overwatch 시즌 요약", size=30, weight="bold"),
        ft.Text("원하는 창 클릭", size=15, weight="bold"),
        top_section
    ], scroll=ft.ScrollMode.ADAPTIVE)
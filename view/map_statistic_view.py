import flet as ft
import pandas as pd


def get_map_tab(page: ft.Page, service, on_hero_click):
    
    # 기본값
    map_id = 0
    tier_id = 1
    map_name = "맵을 선택 해주세요"

    # 1. 원본 데이터 로드
    raw_df = service.get_all_hero_stats(map_id, tier_id)
    
    # 2. 정렬 상태를 관리할 변수들
    current_sort_col = 1     # 기본 정렬 기준 (1: 승률)
    current_sort_asc = False # 기본 정렬 방향 (False: 내림차순, 높은 게 위로)

    # 컬럼 인덱스와 DataFrame 컬럼명을 매칭해주는 딕셔너리
    col_map = {
        1: 'winrate',
        2: 'pickrate',
        3: 'banrate'
    }

    # 3. 데이터테이블 (뼈대) 생성
    data_table = ft.DataTable(
        expand=True, # 🌟 테이블 컨테이너 자체를 확장
        horizontal_margin=30, # 양옆 여백 설정
        column_spacing=50, # 컬럼 사이의 간격
        columns=[
            # ft.Container 로 감싸서 강제로 폭을 늘려줍니다!
            # 영웅 이름과 사진이 들어가는 곳은 조금 더 넓게(250), 나머지는 균일하게(150)
            ft.DataColumn(ft.Container(ft.Text("영웅"), width=250)), 
            ft.DataColumn(ft.Container(ft.Text("승률"), width=150), on_sort=lambda e: on_sort(e)), 
            ft.DataColumn(ft.Container(ft.Text("픽률"), width=150), on_sort=lambda e: on_sort(e)), 
            ft.DataColumn(ft.Container(ft.Text("밴률"), width=150), on_sort=lambda e: on_sort(e)), 
        ],
        sort_column_index=current_sort_col,
        sort_ascending=current_sort_asc,
        heading_row_color=ft.Colors.BLACK_12, 
        show_checkbox_column=False,
    )

    # 4. 표 안의 데이터를 채우는 함수
    def update_table(df: pd.DataFrame):
        data_table.rows.clear()
        
        for _, row in df.iterrows():
            data_table.rows.append(
                ft.DataRow(
                    # DataRow를 클릭했을 때 상세 페이지로 넘어가도록 설정!
                    on_select_change=lambda e, name=str(row["hero_name"]): on_hero_click(name),
                    cells=[
                        ft.DataCell(
                            ft.Row([
                                ft.Image(src=row.get("portrait_url", ""), width=30, height=30, border_radius=5),
                                ft.Text(str(row["hero_name"]), weight="bold")
                            ], tight=True)
                        ),
                        # 텍스트 오른쪽에 % 기호를 붙여서 출력 (DB에 %가 안 붙어있다고 가정)
                        ft.DataCell(ft.Text(f"{row['winrate']}%")),
                        ft.DataCell(ft.Text(f"{row['pickrate']}%")),
                        ft.DataCell(ft.Text(f"{row['banrate']}%")),
                    ]
                )
            )
        page.update()

    # 5. 컬럼 제목 클릭 시 실행되는 정렬 로직
    def on_sort(e):
        nonlocal current_sort_col, current_sort_asc
        
        # 같은 컬럼을 또 클릭하면? 오름차순/내림차순 토글
        if current_sort_col == e.column_index:
            current_sort_asc = not current_sort_asc
        # 다른 컬럼을 클릭하면? 해당 컬럼 기준으로 내림차순(False)부터 시작
        else:
            current_sort_col = e.column_index
            current_sort_asc = False 

        # UI 위젯에 화살표 방향(상태) 업데이트
        data_table.sort_column_index = current_sort_col
        data_table.sort_ascending = current_sort_asc
        
        # Pandas를 이용해 데이터프레임 실제 정렬
        col_name = col_map[current_sort_col]
        sorted_df = raw_df.sort_values(by=col_name, ascending=current_sort_asc)
        
        # 표 다시 그리기
        update_table(sorted_df)

    map_title = ft.Text(f"맵 : {map_name}", size=20, weight="bold", expand=True)

    def update_data(new_df: pd.DataFrame):
        nonlocal raw_df, map_name
        raw_df = new_df # 화면의 근본 데이터를 새로운 맵 데이터로 교체!
        map_name = new_df['map_name'].iloc[0]
        
        # 데이터가 바뀌었으니, 현재 유지 중인 정렬(예: 픽률순) 상태 그대로 다시 정렬해서 그려줌
        map_title.value = f"맵 : {map_name}"
        map_title.update() 
        col_name = col_map[current_sort_col]
        sorted_df = raw_df.sort_values(by=col_name, ascending=current_sort_asc)
        update_table(sorted_df)

    # 6. 처음 화면을 켤 때 기본값(승률 내림차순)으로 한 번 그려주기
    initial_sorted_df = raw_df.sort_values(by=col_map[current_sort_col], ascending=current_sort_asc)
    update_table(initial_sorted_df)

    # 최종 화면 조립
    map_stat_container = ft.Container(
        padding=30,
        expand=True,
        content=ft.Column([
            ft.Row([
                ft.Text("영웅 통계", size=30, weight="bold", expand=True),
                map_title,
                # ft.Container(height=20),
                ]),
            # 영웅이 많아지면 스크롤이 되도록 Column(scroll) 또는 ListView 로 감싸줍니다.
            ft.Column(
                [data_table], 
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        ], expand=True)
    )

    map_stat_container.update_data = update_data

    return map_stat_container
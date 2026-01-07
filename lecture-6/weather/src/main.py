import flet as ft
import requests
from datetime import datetime
import sqlite3
import os

print("--- スクリプトを開始しました ---")

url = 'http://www.jma.go.jp/bosai/common/const/area.json'
data_json = requests.get(url).json()

#天気コードから天気情報を取得
def get_weather_info(weather_code):
    weather_dict = {
        "100": {"text": "晴れ", "icon": "☀️", "color": ft.Colors.ORANGE_400},
        "101": {"text": "晴れ時々曇り", "icon": "🌤️", "color": ft.Colors.ORANGE_300},
        "102": {"text": "晴れ一時雨", "icon": "🌦️", "color": ft.Colors.ORANGE_300},
        "103": {"text": "晴れ時々雨", "icon": "🌦️", "color": ft.Colors.ORANGE_300},
        "104": {"text": "晴れ一時雪", "icon": "🌤️", "color": ft.Colors.ORANGE_300},
        "110": {"text": "晴れのち曇り", "icon": "🌤️", "color": ft.Colors.ORANGE_300},
        "112": {"text": "晴れのち雨", "icon": "🌦️", "color": ft.Colors.ORANGE_300},
        "200": {"text": "曇り", "icon": "☁️", "color": ft.Colors.GREY_500},
        "201": {"text": "曇り時々晴れ", "icon": "⛅", "color": ft.Colors.GREY_400},
        "202": {"text": "曇り一時雨", "icon": "🌧️", "color": ft.Colors.GREY_500},
        "203": {"text": "曇り時々雨", "icon": "🌧️", "color": ft.Colors.GREY_500},
        "204": {"text": "曇り一時雪", "icon": "🌨️", "color": ft.Colors.GREY_500},
        "210": {"text": "曇りのち晴れ", "icon": "⛅", "color": ft.Colors.GREY_400},
        "212": {"text": "曇りのち雨", "icon": "🌧️", "color": ft.Colors.GREY_500},
        "300": {"text": "雨", "icon": "🌧️", "color": ft.Colors.BLUE_400},
        "301": {"text": "雨時々晴れ", "icon": "🌦️", "color": ft.Colors.BLUE_400},
        "302": {"text": "雨時々曇り", "icon": "🌧️", "color": ft.Colors.BLUE_400},
        "400": {"text": "雪", "icon": "❄️", "color": ft.Colors.LIGHT_BLUE_200},
        "401": {"text": "雪時々晴れ", "icon": "🌨️", "color": ft.Colors.LIGHT_BLUE_200},
        "402": {"text": "雪時々曇り", "icon": "🌨️", "color": ft.Colors.LIGHT_BLUE_200},
    }
    return weather_dict.get(weather_code, {"text": "情報なし", "icon": "❓", "color": ft.Colors.GREY_400})


def main(page: ft.Page):
    init_db() #アプリ起動時にテーブルを作る
    page.title = "☀︎ 天気予報"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = None

    # 画面右側の設定（天気予報表示エリア）
    display_context = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=60, color=ft.Colors.GREY_400),
                    ft.Text("都道府県を選択してください", size=18, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=50,
                alignment=ft.alignment.center,
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    #都道府県がクリックされたときの操作
    def on_area_click(e):
        #クリックされた都道府県の名前とコードを取得
        area_name = e.control.title.value
        area_code = e.control.subtitle.value

        # ローディング表示
        display_context.controls.clear()
        display_context.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.ProgressRing(),
                    ft.Text("天気予報を取得中...", size=16, color=ft.Colors.GREY_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=50,
                alignment=ft.alignment.center,
            )
        )
        page.update()

        # 気象庁APIから天気予報を取得
        try:
            weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
            weather_data = requests.get(weather_url).json()
            
            # 予報データの取得
            time_series = weather_data[0]["timeSeries"]
            areas = time_series[0]["areas"][0]
            
            # 日付と天気コード
            dates = time_series[0]["timeDefines"]
            weather_codes = areas["weatherCodes"]
            weathers = areas["weathers"]
            
            # 気温データ（別のtimeSeriesにある場合がある）
            temps_max = []
            temps_min = []

            if len(time_series) > 1:
                for idx, ts in enumerate(time_series):
                    if "areas" in ts and len(ts["areas"]) > 0:
                        area_data = ts["areas"][0]
                        
                        if "temps" in area_data:
                            temps_data = area_data["temps"]
                            temp_time_defines = ts.get("timeDefines", [])
                            
                            # 日付ごとに気温をグループ化
                            temp_by_date = {}
                            for j, temp_time in enumerate(temp_time_defines):
                                if j < len(temps_data) and temps_data[j] != "":
                                    date_part = temp_time.split('T')[0]  # YYYY-MM-DD
                                    time_part = temp_time.split('T')[1] if 'T' in temp_time else "00:00:00"
                                    hour = int(time_part.split(':')[0].replace('+', ''))
                                    
                                    if date_part not in temp_by_date:
                                        temp_by_date[date_part] = []
                                    
                                    temp_by_date[date_part].append({
                                        'hour': hour,
                                        'value': temps_data[j]
                                    })
                            
                            # 各予報日に対応する気温を設定
                            for date_str in dates:
                                date_part = date_str.split('T')[0]
                                
                                if date_part in temp_by_date:
                                    day_temps = temp_by_date[date_part]
                                    # 時刻順にソート
                                    day_temps.sort(key=lambda x: x['hour'])
                                    
                                    if len(day_temps) >= 2:
                                        # 最初の値=最低気温、2番目の値=最高気温
                                        temps_min.append(day_temps[0]['value'])
                                        temps_max.append(day_temps[1]['value'])
                                    elif len(day_temps) == 1:
                                        # 1つしかない場合、時刻で判定
                                        if day_temps[0]['hour'] <= 6:
                                            # 早朝の気温 = 最低気温
                                            temps_min.append(day_temps[0]['value'])
                                            temps_max.append("-")
                                        else:
                                            # 日中の気温 = 最高気温
                                            temps_min.append("-")
                                            temps_max.append(day_temps[0]['value'])
                                    else:
                                        temps_min.append("-")
                                        temps_max.append("-")
                                else:
                                    # この日付の気温データがない
                                    temps_min.append("-")
                                    temps_max.append("-")
                            break

            
            print(f"{'='*50}\n")
            # 画面右側の表示内容を更新
            display_context.controls.clear()
            
            # タイトル
            display_context.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, size=28, color=ft.Colors.BLUE_800),
                            ft.Text(area_name, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(f"地域コード: {area_code}", size=12, color=ft.Colors.GREY_600),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                )
            )

            # 天気予報カードを作成
            weather_cards = ft.Row(
                controls=[],
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            )

            for i, (date_str, weather_code, weather_text) in enumerate(zip(dates, weather_codes, weathers)):
                # 日付をフォーマット
                date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                formatted_date = date_obj.strftime("%Y-%m-%d")
                day_of_week = ["月", "火", "水", "木", "金", "土", "日"][date_obj.weekday()]
                
                # 天気情報を取得
                weather_info = get_weather_info(weather_code)
                
                # 気温データ
                temp_max = temps_max[i] if i < len(temps_max) else "-"
                temp_min = temps_min[i] if i < len(temps_min) else "-"

                # DBに保存
                save_weather_data(area_name, area_code, formatted_date, weather_text, str(temp_max), str(temp_min))
                print(f"{formatted_date}のデータの保存命令を出しました")
                
                # カード作成
                card = ft.Container(
                    content=ft.Column([
                        ft.Text(formatted_date, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Text(f"({day_of_week})", size=12, color=ft.Colors.GREY_600),
                        ft.Container(height=10),
                        ft.Text(weather_info["icon"], size=50),
                        ft.Container(height=5),
                        ft.Text(weather_info["text"], size=13, color=weather_info["color"], weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Text(f"{temp_max}°C", size=16, color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD),
                            ft.Text("/", size=14, color=ft.Colors.GREY_500),
                            ft.Text(f"{temp_min}°C", size=16, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=160,
                    padding=15,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=5,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                )
                weather_cards.controls.append(card)

            display_context.controls.append(
                ft.Container(
                    content=weather_cards,
                    padding=20,
                )
            )

        except Exception as ex:
            display_context.controls.clear()
            display_context.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=60, color=ft.Colors.RED_400),
                        ft.Text("天気予報の取得に失敗しました", size=16, color=ft.Colors.RED_600),
                        ft.Text(f"エラー: {str(ex)}", size=12, color=ft.Colors.GREY_600),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=50,
                    alignment=ft.alignment.center,
                )
            )

        page.update()

    #各ListTileにクリックイベントを追加
    def add_click_to_list_tiles(controls):
        for control in controls:
            if isinstance(control, ft.ExpansionTile):
                add_click_to_list_tiles(control.controls)
            elif isinstance(control, ft.ListTile):
                control.on_click = on_area_click

    def handle_expansion_tile_change(e):
        if e.control.trailing:
            e.control.trailing.name = (
                ft.Icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    area_selection = ft.Column(

        controls=[

        ft.ExpansionTile(
            title=ft.Text("地域を選択"),
            bgcolor=ft.Colors.BLUE_GREY_50,
            collapsed_bgcolor=ft.Colors.BLUE_GREY_50,
            affinity=ft.TileAffinity.PLATFORM,
            initially_expanded=True,
            collapsed_text_color=ft.Colors.BLACK,
            text_color=ft.Colors.BLACK,
            controls=[

                ft.ExpansionTile(
                    title=ft.Text("北海道地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("北海道（宗谷地方）"),subtitle = ft.Text("011000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("北海道（上川・留萌地方）"),subtitle = ft.Text("012000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("北海道（網走・北見・紋別地方）"),subtitle = ft.Text("013000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("北海道（釧路・根室地方）"),subtitle = ft.Text("014100", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("北海道（胆振・日高地方）"),subtitle = ft.Text("015000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("北海道（石狩・空知・後志地方）"),subtitle = ft.Text("016000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("北海道（渡島・檜山地方）"),subtitle = ft.Text("017000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("東北地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("青森県"),subtitle = ft.Text("020000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("岩手県"),subtitle = ft.Text("030000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("宮城県"),subtitle = ft.Text("040000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("秋田県"),subtitle = ft.Text("050000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("山形県"),subtitle = ft.Text("060000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("福島県"),subtitle = ft.Text("070000", size=12, color=ft.Colors.GREY_600)),
                    ],

                ),
                ft.ExpansionTile(
                    title=ft.Text("関東甲信地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("茨城県"),subtitle = ft.Text("080000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("栃木県"),subtitle = ft.Text("090000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("群馬県"),subtitle = ft.Text("100000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("埼玉県"),subtitle = ft.Text("110000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("千葉県"),subtitle = ft.Text("120000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("東京都"),subtitle = ft.Text("130000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("神奈川県"),subtitle = ft.Text("140000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("山梨県"),subtitle = ft.Text("190000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("長野県"),subtitle = ft.Text("200000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ), 
                ft.ExpansionTile(
                    title=ft.Text("北陸地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("新潟県"),subtitle = ft.Text("150000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("富山県"),subtitle = ft.Text("160000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("石川県"),subtitle = ft.Text("170000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("福井県"),subtitle = ft.Text("180000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("東海地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("岐阜県"),subtitle = ft.Text("210000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("静岡県"),subtitle = ft.Text("220000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("愛知県"),subtitle = ft.Text("230000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("三重県"),subtitle = ft.Text("240000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("近畿地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("滋賀県"),subtitle = ft.Text("250000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("京都府"),subtitle = ft.Text("260000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("大阪府"),subtitle = ft.Text("270000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("兵庫県"),subtitle = ft.Text("280000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("奈良県"),subtitle = ft.Text("290000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("和歌山県"),subtitle = ft.Text("300000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("中国地方(山口県を除く)"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("鳥取県"),subtitle = ft.Text("310000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("島根県"),subtitle = ft.Text("320000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("岡山県"),subtitle = ft.Text("330000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("広島県"),subtitle = ft.Text("340000", size=12, color=ft.Colors.GREY_600)),
                    ], 
                ),
                ft.ExpansionTile(
                    title=ft.Text("四国地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("香川県"),subtitle = ft.Text("370000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("愛媛県"),subtitle = ft.Text("380000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("高知県"),subtitle = ft.Text("390000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("徳島県"),subtitle = ft.Text("360000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("九州北部地方(山口県を含む)"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("山口県"),subtitle = ft.Text("350000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("福岡県"),subtitle = ft.Text("400000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("佐賀県"),subtitle = ft.Text("410000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("長崎県"),subtitle = ft.Text("420000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("熊本県"),subtitle = ft.Text("430000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("大分県"),subtitle = ft.Text("440000", size=12, color=ft.Colors.GREY_600)),
                    ], 
                ),
                ft.ExpansionTile(
                    title=ft.Text("九州南部地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("宮崎県"),subtitle = ft.Text("450000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("鹿児島県(奄美地方除く)"),subtitle = ft.Text("460100", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("鹿児島県(奄美地方)"),subtitle = ft.Text("460040", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("沖縄地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREY_800,
                    text_color=ft.Colors.GREY_800,
                    controls=[
                        ft.ListTile(title=ft.Text("沖縄県(沖縄本島地方)"),subtitle = ft.Text("471000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("沖縄県(大東島地方)"),subtitle = ft.Text("472000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("沖縄県(宮古島地方)"),subtitle = ft.Text("473000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("沖縄県(八重山地方)"),subtitle = ft.Text("474000", size=12, color=ft.Colors.GREY_600)),
                        ]
                ),
            ],
        ),
    ],
        scroll=ft.ScrollMode.ADAPTIVE,
        width=300,
    )
    #全てのListTileにクリックイベントを追加
    add_click_to_list_tiles(area_selection.controls)

    #レイアウト構成
    page.add(
        ft.ListTile(
            title=ft.Text("☀︎ 天気予報", size=24, weight=ft.FontWeight.BOLD),
            text_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_800,
        ),
        ft.Row(
            controls=[
                ft.Container(
                    content=area_selection,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    expand=False,
                ),
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=display_context,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    expand=True,
                ),
            ],
            expand=True,
        ),
    )

# --- DB設定 ---
# src/weather.db に保存されるように設定
DB_PATH = os.path.join(os.path.dirname(__file__), "weather.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # area_code, date を組み合わせて一意(UNIQUE)にすることで重複保存を防ぎます
    cur.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT,
            area_code TEXT,
            date TEXT,
            weather_text TEXT,
            temp_max TEXT,
            temp_min TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(area_code, date) 
        )
    ''')
    conn.commit()
    conn.close()

def save_weather_data(area_name, area_code, date, weather, t_max, t_min):
    print(f"DEBUG:保存を開始します -> {area_name},{date}") #実行されたかの確認
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT OR REPLACE INTO weather_history 
            (area_name, area_code, date, weather_text, temp_max, temp_min)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (area_name, area_code, date, weather, t_max, t_min))
        conn.commit()
        print(f"DEBUG:保存が完了しました")
    except Exception as e:
        print(f"DB保存エラー: {e}")
    finally:
        conn.close()



ft.app(target=main)
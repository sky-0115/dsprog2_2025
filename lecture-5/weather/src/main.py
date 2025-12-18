import flet as ft
import requests

url = 'http://www.jma.go.jp/bosai/common/const/area.json'
data_json = requests.get(url).json()


def main(page: ft.Page):
    page.title = "☀︎ 天気予報"
    page.theme_mode = ft.ThemeMode.LIGHT
    #画面からはみ出た時にスクロールできるように
    page.scroll = ft.ScrollMode.ADAPTIVE 

    def handle_expansion_tile_change(e):
        if e.control.trailing:
            e.control.trailing.name = (
                ft.Icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    page.add(

        ft.ExpansionTile(
            title=ft.Text("地域を選択"),
            subtitle=ft.Text("下から選んでください。"),
            bgcolor=ft.Colors.BLUE_GREY_50,
            collapsed_bgcolor=ft.Colors.BLUE_GREY_50,
            affinity=ft.TileAffinity.PLATFORM,
            initially_expanded=True,
            collapsed_text_color=ft.Colors.RED,
            text_color=ft.Colors.RED,
            controls=[

                ft.ExpansionTile(
                    title=ft.Text("北海道地方"),
                    collapsed_icon_color=ft.Colors.BLUE_800,
                    text_color=ft.Colors.BLUE_800,
                    controls=[ft.ListTile(title=ft.Text("北海道"),
                                          subtitle = ft.Text("010000", size=12, color=ft.Colors.GREY_600)
                            )]
                ),
                ft.ExpansionTile(
                    title=ft.Text("東北地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREEN,
                    text_color=ft.Colors.GREEN,
                    controls=[
                        ft.ListTile(title=ft.Text("青森県"), subtitle = ft.Text("020000", size=12, color=ft.Colors.GREY_600)),
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
                    collapsed_text_color=ft.Colors.PURPLE,
                    text_color=ft.Colors.PURPLE,
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
                    collapsed_text_color=ft.Colors.CYAN,
                    text_color=ft.Colors.CYAN,
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
                    collapsed_text_color=ft.Colors.BROWN,
                    text_color=ft.Colors.BROWN,
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
                    collapsed_text_color=ft.Colors.ORANGE,
                    text_color=ft.Colors.ORANGE,
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
                    collapsed_text_color=ft.Colors.TEAL,
                    text_color=ft.Colors.TEAL,
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
                    collapsed_text_color=ft.Colors.LIME,
                    text_color=ft.Colors.LIME,
                    controls=[
                        ft.ListTile(title=ft.Text("香川県"),subtitle = ft.Text("370000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("愛媛県"),subtitle = ft.Text("300000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("高知県"),subtitle = ft.Text("390000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("徳島県"),subtitle = ft.Text("360000", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("九州北部地方(山口県を含む)"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.INDIGO,
                    text_color=ft.Colors.INDIGO,
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
                    collapsed_text_color=ft.Colors.PINK,
                    text_color=ft.Colors.PINK,
                    controls=[
                        ft.ListTile(title=ft.Text("宮崎県"),subtitle = ft.Text("450000", size=12, color=ft.Colors.GREY_600)),
                        ft.ListTile(title=ft.Text("鹿児島県"),subtitle = ft.Text("460100", size=12, color=ft.Colors.GREY_600)),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("沖縄地方"),
                    collapsed_icon_color=ft.Colors.DEEP_ORANGE,
                    text_color=ft.Colors.DEEP_ORANGE,
                    controls=[ft.ListTile(title=ft.Text("沖縄県"),subtitle = ft.Text("471000", size=12, color=ft.Colors.GREY_600))]
                ),
            ],
        ),
    )

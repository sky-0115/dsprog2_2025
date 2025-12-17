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
                    collapse_icon_color=ft.Colors.BLUE_800,
                    text_color=ft.Colors.BLUE_800,
                ),
                ft.ExpansionTile(
                    title=ft.Text("東北地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.GREEN,
                    text_color=ft.Colors.GREEN,
                    controls=[
                        ft.ListTile(title=ft.Text("青森県")),
                        ft.ListTile(title=ft.Text("岩手県")),
                        ft.ListTile(title=ft.Text("宮城県")),
                        ft.ListTile(title=ft.Text("秋田県")),
                        ft.ListTile(title=ft.Text("山形県")),
                        ft.ListTile(title=ft.Text("福島県")),
                    ],

                ),
                ft.ExpansionTile(
                    title=ft.Text("関東甲信地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.PURPLE,
                    text_color=ft.Colors.PURPLE,
                    controls=[
                        ft.ListTile(title=ft.Text("茨城県")),
                        ft.ListTile(title=ft.Text("栃木県")),
                        ft.ListTile(title=ft.Text("群馬県")),
                        ft.ListTile(title=ft.Text("埼玉県")),
                        ft.ListTile(title=ft.Text("千葉県")),
                        ft.ListTile(title=ft.Text("東京都")),
                        ft.ListTile(title=ft.Text("神奈川県")),
                    ],
                ), 
                ft.ExpansionTile(
                    title=ft.Text("東海地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.BROWN,
                    text_color=ft.Colors.BROWN,
                    controls=[
                        ft.ListTile(title=ft.Text("岐阜県")),
                        ft.ListTile(title=ft.Text("静岡県")),
                        ft.ListTile(title=ft.Text("愛知県")),
                        ft.ListTile(title=ft.Text("三重県")),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("近畿地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.ORANGE,
                    text_color=ft.Colors.ORANGE,
                    controls=[
                        ft.ListTile(title=ft.Text("大阪府")),
                        ft.ListTile(title=ft.Text("京都府")),
                        ft.ListTile(title=ft.Text("兵庫県")),
                        ft.ListTile(title=ft.Text("滋賀県")),
                        ft.ListTile(title=ft.Text("奈良県")),
                        ft.ListTile(title=ft.Text("和歌山県")),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("中国地方(山口県を除く)"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.TEAL,
                    text_color=ft.Colors.TEAL,
                    controls=[
                        ft.ListTile(title=ft.Text("鳥取県")),
                        ft.ListTile(title=ft.Text("島根県")),
                        ft.ListTile(title=ft.Text("岡山県")),
                        ft.ListTile(title=ft.Text("広島県")),
                    ], 
                ),
                ft.ExpansionTile(
                    title=ft.Text("四国地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.LIME,
                    text_color=ft.Colors.LIME,
                    controls=[
                        ft.ListTile(title=ft.Text("香川県")),
                        ft.ListTile(title=ft.Text("愛媛県")),
                        ft.ListTile(title=ft.Text("高知県")),
                        ft.ListTile(title=ft.Text("徳島県")),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("九州北部地方(山口県を含む)"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.INDIGO,
                    text_color=ft.Colors.INDIGO,
                    controls=[
                        ft.ListTile(title=ft.Text("山口県")),
                        ft.ListTile(title=ft.Text("福岡県")),
                        ft.ListTile(title=ft.Text("佐賀県")),
                        ft.ListTile(title=ft.Text("長崎県")),
                        ft.ListTile(title=ft.Text("大分県")),
                    ], 
                ),
                ft.ExpansionTile(
                    title=ft.Text("九州南部地方"),
                    trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                    on_change=handle_expansion_tile_change,
                    collapsed_text_color=ft.Colors.PINK,
                    text_color=ft.Colors.PINK,
                    controls=[
                        ft.ListTile(title=ft.Text("熊本県")),
                        ft.ListTile(title=ft.Text("宮崎県")),
                        ft.ListTile(title=ft.Text("鹿児島県")),
                    ],
                ),
                ft.ListTile(title=ft.Text("沖縄地方")),
            ],
        ),
    )
